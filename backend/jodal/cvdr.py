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
    BaseWebScraper, BaseFromElasticsearch)



class DocumentsScraper(ElasticsearchBulkMixin, BaseWebScraper):
    name = 'cvdr'
    method = 'get'
    url = 'https://aleph.openstate.eu/api/2/search'
    params = {
        'filter:schemata': 'Thing',
        'filter:collection_id': '7',
        "offset": 0,
        "limit": 10
    }
    headers = {
        'Content-type': 'application/json'
    }

    def __init__(self, *args, **kwargs):
        super(DocumentsScraper, self).__init__(*args, **kwargs)
        self.config = kwargs['config']
        self.date_from = kwargs['date_from']
        self.date_to = kwargs['date_to']
        self.cvdr_locations = None
        logging.info('Scraper: fetch from %s to %s' % (
            self.date_from, self.date_to,))

    def _get_cvdr_locations(self):
        result = {}
        logging.info('Fetching cvdr locations')
        results = self.es.search(index='jodal_locations', body={"size":1000})
        for l in results.get('hits', {}).get('hits', []):
            cbs_id = l['_id']
            for p in l['_source'].get('sources', []):
                if p['source'] == 'cvdr':
                    result[p['name']] = cbs_id
        return result

    def next(self):
        if len(self.result_json.get('next')) > 0:
            self.params['offset'] += 10
            return True

    def fetch(self):
        if self.cvdr_locations is None:
            self.cvdr_locations = self._get_cvdr_locations()
        sleep(1)
        self.params['dates'] = str(self.date_from)
        #self.payload['filters']['date']['to'] = str(self.date_to)
        result = super(DocumentsScraper, self).fetch()
        if result is not None:
            logging.info(result)
            logging.info(
                'Scraper: in total %s results' % (result['total'],))
            return result.get('results', [])
        else:
            return []

    def transform(self, item):
        # logging.info(item)
        names = getattr(self, 'names', None) or [self.name]
        result = []
        props = item['properties']
        for n in names:
            r_uri = item['links']['self']
            h_id = hashlib.sha1()
            h_id.update(r_uri.encode('utf-8'))
            item_id = item.get('id', None) or item.get('meta', {}).get('_id', None)
            data = {}
            name = props.get('author', ['-'])[0].replace('Gemeente ', '').replace('(L)','(L.)').strip()
            if name in self.cvdr_locations:
                r = {
                    '_id': h_id.hexdigest(),
                    '_index': 'jodal_documents',
                    'id': h_id.hexdigest(),
                    'identifier': r_uri,
                    'url': item['links']['ui'],
                    'location': self.cvdr_locations[name],
                    'title': props.get('title', [''])[0].strip(),
                    'description': item.get('bodyHtml', [''])[0],
                    'created': item.get('createdAt', [None])[0],
                    'modified': item.get('modifiedAt', [None])[0],
                    'published': item.get('publishedAt', [None])[0],
                    'source': self.name,
                    'type': 'Bericht',
                    'data': data
                }
                result.append(r)

        # logging.info(pformat(result))
        return result


class DocumentScraper(BaseFromElasticsearch):
    pass


class CVDRScraperRunner(object):
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


class CVDRDocumentScraperRunner(object):
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
        return items
