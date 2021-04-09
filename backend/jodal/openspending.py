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
                        p_url = self.item['url'] + '%s/%s/#l-%s' % (
                            m_label['slug'], self.agg2openspending[a],
                            p['term'],)
                    else:
                        p_url = self.item['url'].replace(
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
                        'description': '%s' % (
                            self.item['title'],),
                        'location': self.item['location'],
                        'created': self.item['created'],
                        'modified': self.item['modified'],
                        'published': self.item['published'],
                        'type': [self.agg2openspending_names[a], self.item['type']],
                        'data': {
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
        logging.info('Scraper: fetch from %s' % (self.date_from,))

    def next(self):
        next_url = self.result_json['meta']['next']
        if next_url is not None:
            self.url = urljoin('https://openspending.nl', next_url)
            return True

    def fetch(self):
        sleep(2)
        if 'created_at__gt' not in self.url:
            self.url += '&created_at__gt=' + self.date_from
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

            data = {}

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
