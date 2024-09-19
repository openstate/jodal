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
from lxml import etree

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
        self.force = kwargs['force']
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
        if not self.force:
            return
        next_link = None
        try:
            next_link = self.result_html.xpath('//div[contains(@class, "pagination__index")]/ul/li[@class="next"]/a/@href')[0]
        except LookupError as e:
            pass
        logging.info(next_link)
        if (next_link is not None) and (next_link.strip() != ''):
            self.url = urljoin(self.url, next_link)
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
            #logging.info(self.result.content)
            results = result.xpath('//div[@id="content"]//*[contains(@class, "result--list--wide")]/ul/li//h2/a/@href')
            logging.info(results)
            logging.info(
                'Scraper: in total %s(%s) results before bulk' % (
                    '0', len(results),))
            return results
        else:
            return []

    def transform(self, item):
        sleep(1)
        full_url = urljoin(self.url, item)
        logging.info(full_url)
        html = etree.HTML(requests.get(full_url).content)
        names = getattr(self, 'names', None) or [self.name]
        result = []
        for n in names:
            r_uri = full_url
            h_id = hashlib.sha1()
            h_id.update(r_uri.encode('utf-8'))
            item_id = item
            data = {}
            name = html.xpath('//meta[@name="DCTERMS.creator"]/@content')[0].strip()
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
                        name, name,))
            else:
                r = {
                    '_id': h_id.hexdigest(),
                    '_index': 'jodal_documents',
                    'id': h_id.hexdigest(),
                    'identifier': r_uri,
                    'url': full_url,
                    'location': self.cvdr_locations[name],
                    'title': html.xpath('//meta[@name="DCTERMS.title"]/@content')[0].strip(),
                    'description': str(etree.tostring(html.xpath('//*[@id="content"]')[0])),
                    'created': html.xpath('//meta[@name="DCTERMS.modified"]/@content')[0].strip(),
                    'modified': html.xpath('//meta[@name="DCTERMS.modified"]/@content')[0].strip(),
                    'published': html.xpath('//meta[@name="DCTERMS.modified"]/@content')[0].strip(),
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
