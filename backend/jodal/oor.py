import re
from urllib.parse import urljoin, urlparse
import logging
from time import sleep
import hashlib
import datetime
from time import sleep
from pprint import pprint, pformat
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

OOR_URL = 'https://open.overheid.nl/zoekresultaten?informatiesoort=c_3300f29a&sort=date-desc&page=1'
OOR_TIMEOUT = (5,15)

class DocumentsScraper(ElasticsearchBulkMixin, BaseWebScraper):
    name = 'oor'
    url = ''
    headers = {
        'Content-type': 'application/json'
    }
    html = None

    def __init__(self, *args, **kwargs):
        super(DocumentsScraper, self).__init__(*args, **kwargs)
        self.config = kwargs['config']
        self.date_from = kwargs['date_from']
        self.date_to = kwargs['date_to']
        self.paging = kwargs['paging']
        self.max_pages = kwargs['max_pages']
        self.current_page = 0
        self.url = OOR_URL
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
        next_url = urljoin(OOR_URL, u''.join(self.html.xpath('//li[@class="next"]/a/@href')))
        #next_link = u''.join(self.html.xpath('//li[@class="next"]/a/@href'))
        logging.info(f'Should get next page: {next_url}')
        #return False
        if self.paging and (next_url.strip() != '') and (self.current_page < self.max_pages):
            self.url = next_url
            self.current_page += 1
            return next_url

    def fetch(self):
        if self.locations is None:
            self.locations = self._get_locations()
        self.html = etree.HTML(requests.get(self.url).content)
        entries = self.html.xpath('//div[@id="content"]/div[contains(@class,"result--list--wide")]/ul/li')
        if entries is not None:
            logging.info(
                'Scraper: in total %s results' % (len(entries),))
            return entries
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
        try:
            resp = requests.get('http://texter/convert', params={
                'url': pdf_url,
                'filetype': 'pdf'
            }, timeout=OOR_TIMEOUT)
        except requests.exceptions.ReadTimeout as e:
            logging.warning(f'Time out converting pdf to text: {pdf_url}')
            return ''
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
            full_uri = urljoin(OOR_URL, u''.join(item.xpath('.//h2/a/@href')))
            parse_uri = urlparse(full_uri)
            r_uri = parse_uri.scheme + '://' + parse_uri.netloc + parse_uri.path  # create stable urls
            h_id = self._get_hashed_id(r_uri)
            if self.es.exists(id=h_id, index='jodal_documents'):
                logging.info('Document %s already exists.' % (h_id,))
                continue
            item_location = u''.join(
                item.xpath('.//ul[contains(@class,"list--metadata")]/li[2]//text()')).strip()
            pdf_url = urljoin(OOR_URL, u''.join(item.xpath('.//ul[contains(@class,"list--linked")]/li/a/@href')))
            if item_location in self.locations:
                title = u''.join(item.xpath('.//h2//text()'))
                description = self._get_item_description(pdf_url)
                if (description == '') and (title == ''):
                    continue
                item_date = u''.join(
                    item.xpath('.//ul[contains(@class,"list--metadata")]/li[3]//text()')).split(':')[-1]
                d, m, y = item_date.strip().split('-')
                ud = datetime.datetime(int(y), int(m), int(d)).isoformat()
                item_type = u''.join(
                    item.xpath('.//ul[contains(@class,"list--metadata")]/li[1]//text()'))
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
                    'type': item_type,
                    'data': data
                }
                #logging.info(r['url'])
                # logging.info(pformat(r))
                result.append(r)
        #logging.info(pformat(result))
        return result


class OORScraperRunner(object):
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
        logging.info('Fetching oor resulted in %s items ...' % (len(items)))
