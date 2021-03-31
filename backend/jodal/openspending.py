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


class AggregationsScraper(MemoryMixin, BaseWebScraper):
    name = 'openspending'
    url = 'https://openspending.nl/api/v1/aggregations/all/'
    method = 'get'
    aggregation_type = None
    payload = None
    params = None
    headers = {
        'Content-type': 'application/json'
    }

    def __init__(self, *args, **kwargs):
        super(AggregationsScraper, self).__init__(*args, **kwargs)
        self.params = deepcopy(kwargs)

    def fetch(self):
        result = super(AggregationsScraper, self).fetch()
        results = {}
        for f in ['main', 'sub', 'cat', 'total']:
            results[f] = result.get('facets', {}).get(f, {})
        return [results]

    def transform(self, item):
        names = getattr(self, 'names', None) or [self.name]
        result = []
        for n in names:
            result.append(item)
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

            data = {}
            for agg in ['all']:
                # TODO: add 'direction' and 'type' and store accordingly
                for direction in ['in', 'out']:
                    options = {
                        'document_id': item['id'],
                        'direction': direction
                    }
                    aggregation = AggregationsScraper(**options)
                    aggregation.run()
                    agg_result = aggregation.items
                    if agg_result is not None:
                        data[direction] = agg_result
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
        logging.info(result)
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
