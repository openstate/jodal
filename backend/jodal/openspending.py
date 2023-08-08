import json
import logging
import csv
import os.path
import re
from pprint import pformat
import hashlib
from copy import deepcopy
from urllib.parse import urljoin
from time import sleep
import locale
import datetime

import requests

from jodal.es import setup_elasticsearch
from jodal.scrapers import (
    MemoryMixin, ElasticsearchMixin, ElasticsearchBulkMixin, BaseScraper,
    BaseWebScraper)


class BaseOpenSpendingScraper(MemoryMixin, BaseWebScraper):
        plan2openspendingplan = {
            'budget': 'begroting',
            'spending': 'realisatie'
        }
        gov_type2openspending = {
            'GM': '06',
            'PV': '03'
        }
        agg2openspending = {
            'main': 'hoofdfuncties',
            'sub': 'functies',
            'cat': 'categorieen'
        }
        agg2openspending_names = {
            'main': 'Hoofdfunctie',
            'sub': 'Functie',
            'cat': 'Categorie'
        }
        direction2openspending = {
            'in': 'baten',
            'out': 'lasten'
        }


class LabelsScraper(BaseOpenSpendingScraper):
    name = 'openspending'
    url = 'https://openspending.nl/api/v1/labels/'
    method = 'get'
    payload = None
    params = None
    headers = {
        'Content-type': 'application/json'
    }

    def __init__(self, *args, **kwargs):
        super(LabelsScraper, self).__init__(*args, **kwargs)
        self.params = deepcopy(kwargs)
        self.items = []

    def fetch(self):
        sleep(1)
        result = super(LabelsScraper, self).fetch()

        if result is None:
            return []

        return result['objects']

    def transform(self, item):
        names = getattr(self, 'names', None) or [self.name]
        result = []
        for n in names:
            result.append(item)
        return result

class AggregationsScraper(BaseOpenSpendingScraper):
    name = 'openspending'
    url = 'https://openspending.nl/api/v1/aggregations/all/'
    method = 'get'
    payload = None
    params = None
    headers = {
        'Content-type': 'application/json'
    }

    def __init__(self, *args, **kwargs):
        super(AggregationsScraper, self).__init__(*args, **kwargs)
        self.labels = kwargs['labels']
        self.item = kwargs['item']
        self.params = deepcopy(kwargs)
        del self.params['labels']
        del self.params['item']
        self.items = []

    def fetch(self):
        sleep(1)
        result = super(AggregationsScraper, self).fetch()

        if result is None:
            return []

        results = {}
        for f in ['main', 'sub', 'cat', 'total']:
            results[f] = result.get('facets', {}).get(f, {})
        return [results]

    def transform(self, item):
        names = getattr(self, 'names', None) or [self.name]
        result = []
        # '/api/v1/labels/33394-sub-6.6-out/'
        # logging.info(item)
        item_url = self.item['url'].replace(
            '/lasten/', '/%s/' % (
                self.direction2openspending[self.params['direction']])
        ).replace(
            '/baten/', '/%s/' % (
                self.direction2openspending[self.params['direction']])
        )
        for n in names:
            for a in ['main', 'sub', 'cat']:
                for p in item[a]['terms']:
                    p_id = '/api/v1/labels/%s-%s-%s-%s/' % (
                        self.params['document_id'], a, p['term'],
                        self.params['direction'],)
                    p_uri = urljoin('https://www.openspending.nl/', p_id)
                    if a == 'sub':
                        m_id = '/api/v1/labels/%s-%s-%s-%s/' % (
                            self.params['document_id'], 'main', int(p['term'][0:1]) + 1,
                            self.params['direction'],)
                        m_label = label = self.labels.get(m_id, {'slug': '-'})
                        p_url = item_url + '%s/%s/#l-%s' % (
                            m_label['slug'], self.agg2openspending[a],
                            p['term'],)
                    else:
                        p_url = item_url.replace(
                            '/%s/' % (self.agg2openspending['main'],),
                            '/%s/' % (self.agg2openspending[a],)) + '#l-%s' % (
                                p['term'],)
                    p_hash = hashlib.sha1()
                    p_hash.update(p_uri.encode('utf-8'))
                    label = self.labels.get(p_id, {'label': '-'})
                    result.append({
                        '_id': p_hash.hexdigest(),
                        '_index': 'jodal_documents',
                        'id': p_hash.hexdigest(),
                        'identifier': p_uri,
                        'url': p_url,
                        'title': label['label'],
                        'description': '%s - %s' % (
                            self.item['title'],
                            self.direction2openspending[self.params['direction']]),
                        'location': self.item['location'],
                        'created': self.item['created'],
                        'modified': self.item['modified'],
                        'published': self.item['published'],
                        'processed': datetime.datetime.now().isoformat(),
                        'source': self.name,
                        'type': [
                            self.direction2openspending[self.params['direction']],
                            self.agg2openspending_names[a],
                            self.item['type']
                        ],
                        'data': {
                            'openspending_document_id': self.params['document_id'],
                            'value': p['total'],
                            'label': label
                        }
                    })
        return result


class DocumentsScraper(ElasticsearchBulkMixin, BaseOpenSpendingScraper):
    name = 'openspending'
    url = 'https://openspending.nl/api/v1/documents/?order_by=-created_at&limit=10'
    payload = None
    headers = {
        'Content-type': 'application/json'
    }

    def __init__(self, *args, **kwargs):
        super(DocumentsScraper, self).__init__(*args, **kwargs)
        self.config = kwargs['config']
        self.date_from = kwargs['date_from']
        self.date_to = kwargs['date_to']
        logging.info('Scraper: fetch from %s to %s' % (self.date_from, self.date_to,))

    def next(self):
        next_url = self.result_json['meta']['next']
        if next_url is not None:
            self.url = urljoin('https://openspending.nl', next_url)
            return True

    def fetch(self):
        sleep(2)
        for cparam, dparam in {'created_at__gt': 'date_from', 'created_at__lt': 'date_to'}.items():
            if cparam not in self.url:
                self.url += '&' + cparam + '=' + getattr(self, dparam)
        result = super(DocumentsScraper, self).fetch()
        logging.info(
            'Scraper: in total %s results' % (result['meta']['total_count'],))
        if result is not None:
            return result['objects']
        else:
            return []

    def transform(self, item):
        # logging.info(item)
        names = getattr(self, 'names', None) or [self.name]
        result = []
        for n in names:
            r_uri = urljoin('https://www.openspending.nl/', item['resource_uri'])
            h_id = hashlib.sha1()
            h_id.update(r_uri.encode('utf-8'))
            # https://openspending.nl/zwijndrecht/begroting/2021/lasten/hoofdfuncties/

            openspending_url = 'https://www.openspending.nl/%s/%s/%s/lasten/hoofdfuncties/' % (
                item['government']['slug'], self.plan2openspendingplan[item['plan']],
                item['year'],)
            openspending_title = self.plan2openspendingplan[item['plan']].capitalize()
            if item['period'] > 0 and item['period'] < 5:
                openspending_title += ' %se kwartaal' % (item['period'])

            labels_options = {
                'document_id': item['id'],
                'limit': 10000
            }
            labels_scraper = LabelsScraper(**labels_options)
            labels_scraper.run()
            labels = {l['resource_uri']: l for l in labels_scraper.items}

            data = {
                'openspending_document_id': item['id']
            }

            openspending_title += ' %s' % (item['year'],)
            r = {
                '_id': h_id.hexdigest(),
                '_index': 'jodal_documents',
                'id': h_id.hexdigest(),
                'identifier': r_uri,
                'url': openspending_url,
                'location': item['government']['code'],
                'title': openspending_title,
                'created': item['created_at'],
                'modified': item['updated_at'],
                'published': item['parsed_at'],
                'source': self.name,
                'type': self.plan2openspendingplan[item['plan']].capitalize(),
                'data': data
            }
            result.append(r)

            for direction in ['in', 'out']:
                options = {
                    'document_id': item['id'],
                    'direction': direction,
                    'labels': labels,
                    'item': r
                }
                aggregation = AggregationsScraper(**options)
                aggregation.run()
                if aggregation.items is not None:
                    result += aggregation.items

        # logging.info(pformat(result))
        return result


class DocumentScraper(BaseOpenSpendingScraper):
    name = 'openspending'
    url = 'https://openspending.nl/api/v1/documents/'
    payload = None
    headers = {
        'Content-type': 'application/json'
    }

    def __init__(self, *args, **kwargs):
        super(DocumentScraper, self).__init__(*args, **kwargs)
        self.config = kwargs['config']
        self.document_id = kwargs['document_id']
        self.verbose = kwargs['verbose']
        logging.info('Fetching document %s' % (self.document_id,))

    def next(self):
        pass

    def fetch(self):
        sleep(2)
        self.url += '%s/' % (self.document_id,)
        result = super(DocumentScraper, self).fetch()
        return [result]

    def _convert_aggregation_item(self, item):
        result = {
            #'document': item['data']['label']['document_id'],
            'locatie': self.result_json['government']['name'],
            'jaar': self.result_json['year'],
            'plan': self.plan2openspendingplan[self.result_json['plan']],
            'periode': self.result_json['period'],
            'soort': self.direction2openspending[
                item['data']['label']['direction']],
            'type': self.agg2openspending_names[
                item['data']['label']['type']],
            'code': str(item['data']['label']['code']),
            'naam': item['title'],
            'bedrag': item['data']['value']
        }
        if self.verbose:
            result['locatie_code'] = self.result_json['government']['code']
        return result

    def transform(self, item):
        # logging.info(item)
        names = getattr(self, 'names', None) or [self.name]
        result = []
        for n in names:
            r_uri = self.url
            h_id = hashlib.sha1()
            h_id.update(r_uri.encode('utf-8'))
            # https://openspending.nl/zwijndrecht/begroting/2021/lasten/hoofdfuncties/
            openspending_url = 'https://www.openspending.nl/%s/%s/%s/lasten/hoofdfuncties/' % (
                item['government']['slug'], self.plan2openspendingplan[item['plan']],
                item['year'],)
            openspending_title = self.plan2openspendingplan[item['plan']].capitalize()
            if item['period'] > 0 and item['period'] < 5:
                openspending_title += ' %se kwartaal' % (item['period'])

            labels_options = {
                'document_id': item['id'],
                'limit': 10000
            }
            labels_scraper = LabelsScraper(**labels_options)
            labels_scraper.run()
            labels = {l['resource_uri']: l for l in labels_scraper.items}

            data = {
                'openspending_document_id': item['id']
            }

            openspending_title += ' %s' % (item['year'],)
            r = {
                '_id': h_id.hexdigest(),
                '_index': 'jodal_documents',
                'id': h_id.hexdigest(),
                'identifier': r_uri,
                'url': openspending_url,
                'location': item['government']['code'],
                'title': openspending_title,
                'created': item['created_at'],
                'modified': item['updated_at'],
                'published': item['parsed_at'],
                'source': self.name,
                'type': self.plan2openspendingplan[item['plan']].capitalize(),
                'data': data
            }
            # result.append(r)

            for direction in ['in', 'out']:
                options = {
                    'document_id': item['id'],
                    'direction': direction,
                    'labels': labels,
                    'item': r
                }
                aggregation = AggregationsScraper(**options)
                aggregation.run()
                if aggregation.items is not None:
                    result += [
                        self._convert_aggregation_item(a) for a in aggregation.items]

        # logging.info(pformat(result))
        output = result
        return result


class DocumentIdsScraper(BaseOpenSpendingScraper):
    name = 'openspending'
    url = 'https://openspending.nl/api/v1/documents/?order_by=-created_at&limit=10'
    payload = None
    headers = {
        'Content-type': 'application/json'
    }

    configurable_params = {
        'date_from': 'created_at__gt',
        'date_to':'created_at__lt',
        'year': 'year__exact',
        'period': 'period__exact'
    }

    def __init__(self, *args, **kwargs):
        super(DocumentIdsScraper, self).__init__(*args, **kwargs)
        self.config = kwargs['config']
        for k, v in self.configurable_params.items():
            setattr(self, k, kwargs.get(k))
        logging.info('Scraper: fetch from %s to %s' % (self.date_from, self.date_to,))

    def next(self):
        next_url = self.result_json['meta']['next']
        if next_url is not None:
            self.url = urljoin('https://openspending.nl', next_url)
            return True

    def fetch(self):
        sleep(2)
        for dparam, cparam in self.configurable_params.items():
            if cparam not in self.url:
                v = getattr(self, dparam)
                if v is not None:
                    self.url += '&' + cparam + '=' + getattr(self, dparam)
        result = super(DocumentIdsScraper, self).fetch()
        logging.info(
            'Scraper: in total %s results' % (result['meta']['total_count'],))
        if result is not None:
            return result['objects']
        else:
            return []

    def transform(self, item):
        # logging.info(item)
        names = getattr(self, 'names', None) or [self.name]
        result = []
        for n in names:
            result.append(item['id'])
        return result


class OpenSpendingScraperRunner(object):
    scrapers = [
        DocumentsScraper
    ]


    def run(self, *args, **kwargs):
        items = []
        for scraper in self.scrapers:
            k = scraper(**kwargs)
            try:
                k.items = []
                k.run()
                items += k.items
            except Exception as e:
                logging.error(e)
                raise e
        logging.info('Fetching resulted in %s items ...' % (len(items)))


class OpenSpendingCacheScraperRunner(object):
    scrapers = [
        DocumentIdsScraper
    ]


    def run(self, *args, **kwargs):
        items = []
        for scraper in self.scrapers:
            k = scraper(**kwargs)
            try:
                k.items = []
                k.run()
                items += k.items
            except Exception as e:
                logging.error(e)
                raise e
        logging.info('Fetching resulted in %s items ...' % (len(items)))
        for item in items:
            print(item)


class OpenSpendingDocumentScraperRunner(object):
    scrapers = [
        DocumentScraper
    ]


    def run(self, *args, **kwargs):
        items = []
        for scraper in self.scrapers:
            k = scraper(**kwargs)
            try:
                k.items = []
                k.run()
                items += k.items
            except Exception as e:
                logging.error(e)
                raise e
        logging.info('Fetching resulted in %s items ...' % (len(items)))
        #logging.info(pformat(items))
        print(json.dumps(items))
        return items
