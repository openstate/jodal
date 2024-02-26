import re
from urllib.parse import urljoin
import logging
from time import sleep
import hashlib
import datetime
from time import sleep
from pprint import pprint
import json

import requests
from lxml import etree
from elasticsearch.helpers import bulk
from rq import Connection, Queue
from redis import Redis
import feedparser

from jodal.utils import load_config
from jodal.es import setup_elasticsearch
from jodal.redis import setup_redis
from jodal.scrapers import (
    MemoryMixin, ElasticsearchMixin, ElasticsearchBulkMixin, BaseScraper,
    BaseWebScraper, BaseFromElasticsearch)

OBK_URL = 'https://zoek.officielebekendmakingen.nl/rss?q=(c.product-area==%22officielepublicaties%22)and((w.organisatietype==%22gemeente%22))and((w.publicatienaam==%22Gemeenteblad%22))'
OBK_TIMEOUT = (5,15)

class DocumentsScraper(ElasticsearchBulkMixin, BaseWebScraper):
    name = 'obk'
    url = ''
    headers = {
        'Content-type': 'application/json'
    }

    def __init__(self, *args, **kwargs):
        super(DocumentsScraper, self).__init__(*args, **kwargs)
        self.config = kwargs['config']
        self.date_from = kwargs['date_from']
        self.date_to = kwargs['date_to']
        self.url = OBK_URL
        self.locations = None
        logging.info('Scraper: fetch from %s to %s' % (
            self.date_from, self.date_to,))

    def _get_locations(self):
        result = {}
        logging.info('Fetching obk locations')
        results = self.es.search(index='jodal_locations', body={"size":1000})
        for l in results.get('hits', {}).get('hits', []):
            #logging.info(l)
            cbs_id = l['_id']
            result[l['_source']['name']] = cbs_id
        return result

    def next(self):
        pass

    def fetch(self):
        if self.locations is None:
            self.locations = self._get_locations()
        result = feedparser.parse(OBK_URL)
        if result is not None:
            logging.info(
                'Scraper: in total %s results' % (len(result.entries),))
            return result.entries
        else:
            return []

    def setup(self):
        self._init_es()
        self.redis_client = setup_redis(self.config)

    def _get_hashed_id(self, dc_identifier):
        h_id = hashlib.sha1()
        h_id.update(dc_identifier.encode('utf-8'))
        return h_id.hexdigest()

    def _get_item_description(self, pdf_url):
        resp = requests.get('http://texter/convert', params={
            'url': pdf_url,
            'filetype': 'pdf'
        }, timeout=OBK_TIMEOUT)
        if resp.status_code == 200:
            t = resp.json()
            return t.get('text', '')
        else:
            return ''

    def transform(self, item):
        #logging.info(item)
        names = getattr(self, 'names', None) or [self.name]
        result = []
        for n in names:
            data = {}
            r_uri = item['link']
            h_id = self._get_hashed_id(r_uri)
            item_location = item['title'].rsplit(':', -1)[-1].strip()
            pdf_url = item['link'].replace('.html', '.pdf')
            if item_location in self.locations:
                title = item.get('summary', '').strip()
                description = self._get_item_description(pdf_url)
                if (description == '') and (title == ''):
                    continue
                ud = datetime.datetime(*item['published_parsed'][:6]).isoformat()
                r = {
                    '_id': h_id,
                    '_index': 'jodal_documents',
                    'id': h_id,
                    'identifier': r_uri,
                    'url': r_uri,
                    'location': self.locations[item_location],
                    'title': title,
                    'description': description,
                    'created': ud,
                    'modified': ud,
                    'published': ud,
                    'processed': datetime.datetime.now().isoformat(),
                    'source': self.name,
                    'type': item.tags[0]['scheme'],
                    'data': data
                }
                result.append(r)
        # logging.info(pformat(result))
        return result


class OBKScraperRunner(object):
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
        logging.info('Fetching obk resulted in %s items ...' % (len(items)))
