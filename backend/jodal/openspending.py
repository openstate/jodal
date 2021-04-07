import json
import logging
import csv
import os.path
import re
from pprint import pformat
import hashlib
from copy import deepcopy
from urllib.parse import urljoin

import requests

from jodal.es import setup_elasticsearch
from jodal.scrapers import (
    MemoryMixin, ElasticsearchMixin, BaseScraper, BaseWebScraper)


class LabelsScraper(MemoryMixin, BaseWebScraper):
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
        result = super(LabelsScraper, self).fetch()
        return result['objects']

    def transform(self, item):
        names = getattr(self, 'names', None) or [self.name]
        result = []
        for n in names:
            result.append(item)
        return result

class AggregationsScraper(MemoryMixin, BaseWebScraper):
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
        self.params = deepcopy(kwargs)
        del self.params['labels']
        self.items = []

    def fetch(self):
        result = super(AggregationsScraper, self).fetch()
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
                    p_hash = hashlib.sha1()
                    p_hash.update(p_uri.encode('utf-8'))
                    label = self.labels.get(p_id, {'label': '-'})
                    result.append({
                        'id': p_hash.hexdigest(),
                        'identifier': p_uri,
                        'url': p_uri,  # need to change this!
                        'title': label['label'],
                        'type': [a, self.params['direction']],
                        'data': {
                            'value': p['total'],
                            'label': label
                        }
                    })
        return result


class DocumentsScraper(MemoryMixin, BaseWebScraper):
    name = 'openspending'
    url = 'https://openspending.nl/api/v1/documents/?limit=2'
    payload = None
    headers = {
        'Content-type': 'application/json'
    }

    def __init__(self, *args, **kwargs):
        super(DocumentsScraper, self).__init__(*args, **kwargs)

    def fetch(self):
        result = super(DocumentsScraper, self).fetch()
        return result['objects']

    def transform(self, item):
        # logging.info(item)
        names = getattr(self, 'names', None) or [self.name]
        result = []
        plan2openspendingplan = {
            'budget': 'begroting',
            'spending': 'realisatie'
        }
        gov_type2openspending = {
            'GM': '06',
            'PV': '03'
        }
        for n in names:
            r_uri = urljoin('https://www.openspending.nl/', item['resource_uri'])
            h_id = hashlib.sha1()
            h_id.update(r_uri.encode('utf-8'))
            # https://openspending.nl/zwijndrecht/begroting/2021/lasten/hoofdfuncties/

            openspending_url = 'https://www.openspending.nl/%s/%s/%s/lasten/hoofdfuncties/' % (
                item['government']['slug'], plan2openspendingplan[item['plan']],
                item['year'],)
            openspending_title = plan2openspendingplan[item['plan']].capitalize()
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
            for direction in ['in', 'out']:
                options = {
                    'document_id': item['id'],
                    'direction': direction,
                    'labels': labels
                }
                aggregation = AggregationsScraper(**options)
                aggregation.run()
                logging.info(aggregation.items)
                # agg_result = aggregation.items
                # if agg_result is not None:
                #     data[direction] = agg_result
            openspending_title += ' %s' % (item['year'],)
            r = {
                'id': h_id.hexdigest(),
                'identifier': r_uri,
                'url': openspending_url,
                'location': item['government']['code'],
                'title': openspending_title,
                'created': item['created_at'],
                'modified': item['updated_at'],
                'published': item['parsed_at'],
                'source': self.name,
                'type': plan2openspendingplan[item['plan']].capitalize(),
                'data': data
            }
            result.append(r)
        #logging.info(result)
        return result


class OpenSpendingScraperRunner(object):
    scrapers = [
        DocumentsScraper
    ]


    def run(self):
        items = []
        for scraper in self.scrapers:
            k = scraper()
            try:
                k.items = []
                k.run()
                items += k.items
            except Exception as e:
                logging.error(e)
                raise e
        logging.info('Fetching resulted in %s items ...' % (len(items)))
        # es = setup_elasticsearch()
        # for l in locations:
        #     if not es.exists(id=l['id'], index='jodal_locations'):
        #         es.create(id=l['id'], index='jodal_locations', body=l)
