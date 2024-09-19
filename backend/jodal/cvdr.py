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
    MemoryMixin, ElasticsearchMixin, ElasticSearchBulkLocationMixin, BaseScraper,
    BaseWebScraper, BaseFromElasticsearch, BaseHtmlWebscraper)



class DocumentsScraper(ElasticSearchBulkLocationMixin, BaseHtmlWebscraper):
    name = 'cvdr'
    method = 'get'
    url = 'https://lokaleregelgeving.overheid.nl/ZoekResultaat?datumrange=alle&indeling=&sort=date-desc&page=1&count=50'

    def __init__(self, *args, **kwargs):
        super(DocumentsScraper, self).__init__(*args, **kwargs)
        self.config = kwargs['config']
        self.date_from = kwargs['date_from']
        self.date_to = kwargs['date_to']
        self.date_field = kwargs['date_field']
        self.cvdr_locations = None
        logging.info('Scraper: fetch from %s to %s' % (
            self.date_from, self.date_to,))
        self.url = (
            'https://zoekdienst.overheid.nl/sru/Search?version=1.2&operation='
            'searchRetrieve&x-connection=cvdr&startRecord=1&maximumRecords=10&'
            'query=issued>=%s AND issued<=%s') % (
                self.date_from, self.date_to,)


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
        next_link = self.result_json.get('next')
        if (next_link is not None) and (next_link.strip() != ''):
            self.params['offset'] += self.params['limit']
            return True

    def fetch(self):
        if self.cvdr_locations is None:
            self.cvdr_locations = self._get_cvdr_locations()
        sleep(1)
        #self.params['filter:' + self.date_field] = str(self.date_from)
        #self.payload['filters']['date']['to'] = str(self.date_to)
        result = super(DocumentsScraper, self).fetch()
        if result is not None:
            logging.info(result)
            results = result.get('results', [])
            logging.info(
                'Scraper: in total %s(%s) results before bulk' % (
                    result['total'], len(results),))
            return results
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
            name = props.get('author', ['-'])[0].strip()
            name_replacements = {
                'Gemeente ': '',
                '(L)': '(L.)',
                '(NH)': '(NH.)',
                '(Utr)': ''
            }
            for k,v in name_replacements.items():
                name = re.sub('\s+', ' ', name.replace(k, v).strip())
            if name not in self.cvdr_locations:
                logging.info(
                    'Scraper: cvdr author [%s] (%s) was not found in locations' % (
                        name, props.get('author'),))
            else:
                r = {
                    '_id': h_id.hexdigest(),
                    '_index': 'jodal_documents',
                    'id': h_id.hexdigest(),
                    'identifier': r_uri,
                    'url': item['links']['ui'],
                    'location': self.cvdr_locations[name],
                    'title': props.get('title', [''])[0].strip(),
                    'description': props.get('bodyHtml', [''])[0],
                    'created': props.get('createdAt', [None])[0],
                    'modified': props.get('modifiedAt', [None])[0],
                    'published': props.get('publishedAt', [None])[0],
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
