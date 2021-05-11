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



class DocumentsScraper(ElasticsearchBulkMixin, BaseWebScraper):
    name = 'poliflw'
    url = 'https://api.poliflw.nl/v0/search'
    payload = {
        'filters': {
            'date': {
                'from': "2021-01-01",
                'to': '2021-01-01'
            }
        },
        "sort": "date",
        "order": "desc",
        "from": 0
    }
    headers = {
        'Content-type': 'application/json'
    }

    def __init__(self, *args, **kwargs):
        super(DocumentsScraper, self).__init__(*args, **kwargs)
        self.config = kwargs['config']
        self.date_from = kwargs['date_from']
        self.date_to = kwargs['date_to']
        logging.info('Scraper: fetch from %s to %s' % (
            self.date_from, self.date_to,))

    def _get_poliflw_locations(self):
        result = {}
        logging.info('Fetching locations')
        results = self.es.search(index='jodal_locations', body={"size":1000})
        for l in results.get('hits', {}).get('hits', []):
            cbs_id = l['_id']
            for p in l['_source'].get('sources', []):
                if p['source'] == 'poliflw':
                    result[p['name']] = cbs_id
        return result

    def next(self):
        if len(self.result_json.get('item', [])) > 0:
            self.payload['from'] += 10
            return True

    def fetch(self):
        self.poliflw_locations = self._get_poliflw_locations()
        sleep(1)
        self.payload['filters']['date']['from'] = str(self.date_from)
        self.payload['filters']['date']['to'] = str(self.date_to)
        result = super(DocumentsScraper, self).fetch()
        if result is not None:
            logging.info(
                'Scraper: in total %s results' % (result['meta']['total'],))
            return result.get('item', [])
        else:
            return []

    def transform(self, item):
        # logging.info(item)
        names = getattr(self, 'names', None) or [self.name]
        result = []
        for n in names:
            r_uri = item['meta']['pfl_url']
            h_id = hashlib.sha1()
            h_id.update(r_uri.encode('utf-8'))
            poliflw_url = 'https://www.poliflw.nl/l/%s/%s/%s' % (
                item['location'], item['parties'][0], item['id'],)
            data = {}
            if item['location'] in self.poliflw_locations:
                r = {
                    '_id': h_id.hexdigest(),
                    '_index': 'jodal_documents',
                    'id': h_id.hexdigest(),
                    'identifier': r_uri,
                    'url': poliflw_url,
                    'location': self.poliflw_locations[item['location']],
                    'title': item.get('title', ''),
                    'created': item['date'],
                    'modified': item['date'],
                    'published': item['date'],
                    'source': self.name,
                    'type': 'Bericht',
                    'data': data
                }
                result.append(r)

        # logging.info(pformat(result))
        return result


class PoliflwScraperRunner(object):
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
