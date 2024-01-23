import re
from urllib.parse import urljoin
import logging
from time import sleep
import hashlib
import datetime
from time import sleep

import requests
from lxml import etree
from elasticsearch.helpers import bulk
from rq import Queue
from redis import Connection, Redis

from jodal.utils import load_config
from jodal.es import setup_elasticsearch
from jodal.redis import setup_redis
from jodal.scrapers import (
    MemoryMixin, ElasticsearchMixin, ElasticsearchBulkMixin, BaseScraper,
    BaseWebScraper, BaseFromElasticsearch)

WOO_URL = 'https://doi.wooverheid.nl/?doi=nl&dim=publisher&category=Gemeente'


class DocumentsScraper(ElasticsearchMixin, BaseWebScraper):
    name = 'woogle'
    url = ''
    headers = {
        'Content-type': 'application/json'
    }

    def __init__(self, *args, **kwargs):
        super(DocumentsScraper, self).__init__(*args, **kwargs)
        self.config = kwargs['config']
        self.date_from = kwargs['date_from']
        self.date_to = kwargs['date_to']
        self.url = kwargs['url']
        self.locations = None
        logging.info('Scraper: fetch from %s to %s' % (
            self.date_from, self.date_to,))

    def _get_locations(self):
        result = {}
        logging.info('Fetching woogle locations')
        results = self.es.search(index='jodal_locations', body={"size":1000})
        for l in results.get('hits', {}).get('hits', []):
            cbs_id = l['_id']
            for p in l['_source'].get('sources', []):
                if p['source'] == self.name:
                    result[p['id']] = cbs_id
        return result

    def next(self):
        pass

    def fetch(self):
        if self.locations is None:
            self.locations = self._get_locations()
        sleep(1)
        result = super(DocumentsScraper, self).fetch()
        if result is not None:
            logging.info(
                'Scraper: in total %s results' % (result['infobox']['foi_totalDossiers'],))
            return result['infobox'].get('foi_dossiers', [])
        else:
            return []

    def setup(self):
        self._init_es()

    def load(self, item):
        super(DocumentsScraper, self).load(item)
        result = bulk(self.es, item, False)

    def transform(self, item):
        #logging.info(item)
        names = getattr(self, 'names', None) or [self.name]
        result = []
        for n in names:
            data = {}
            r_uri = item['dc_identifier']
            h_id = hashlib.sha1()
            h_id.update(r_uri.encode('utf-8'))
            if item.get('dc_publisher', None) in self.locations:
                description = item.get('dc_description', '').strip()
                title = item.get('dc_title', '').strip()
                if (description == '') and (title == ''):
                    continue
                ud = item.get('foi_updateDate') or item['foi_retrievedDate']
                r = {
                    '_id': h_id.hexdigest(),
                    '_index': 'jodal_documents',
                    'id': h_id.hexdigest(),
                    'identifier': r_uri,
                    'url': 'https://doi.wooverheid.nl/?doi=%s' % (r_uri,),
                    'location': self.locations[item['dc_publisher']],
                    'title': title,
                    'description': description,
                    'created': item['foi_retrievedDate'],
                    'modified': ud,
                    'published': item['foi_retrievedDate'],
                    'processed': datetime.datetime.now().isoformat(),
                    'source': self.name,
                    'type': item['dc_type_description'],
                    'data': data
                }

                for fd in item['foi_files']:
                    if not fd.get('dc_source', '').endswith('.pdf'):
                        logging.info('Skipping foi document %s since it is not a pdf' % (fd.get('dc_source', ''),))
                        continue
                    resp = requests.get('http://texter/convert', params={
                        'url': fd['dc_source'],
                        'filetype': 'pdf'
                    })
                    if resp.status_code == 200:
                        t = resp.json()
                        r['description'] += "\n\n" + fd['dc_title'] + "\n\n" + t.get('text', '')
                    sleep(1)
                ## todo: something with attached documents
                logging.info(r)
                result.append(r)

        # logging.info(pformat(result))
        return result


class WoogleScraperRunner(object):
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
        logging.info('Fetching woogle resulted in %s items ...' % (len(items)))

def fetch_url(url):
    config = load_config()
    es = setup_elasticsearch(config)
    redis_client = setup_redis(config)
    df = None
    dt = None
    kwargs = {
        'config': config,
        'date_from': df,
        'date_to': dt,
        'url': url
    }
    print(url)
    WoogleScraperRunner().run(**kwargs)

def test():
    print("Test")
    url = 'https://doi.wooverheid.nl/?doi=nl.gm0518&infobox=true'
    fetch_url(url)

def run(config={}):
    resp = requests.get(WOO_URL)
    if resp.status_code != 200:
        logging.warning('Page not fetched correctly!')
        return

    html = etree.HTML(resp.content)

    rc = 0
    max_rc = 2
    for r in html.xpath("//table//tr"):
        #print(r)
        try:
            l = r.xpath('./td[1]/a/@href')[0]
        except LookupError as e:
            l = None
        gl = urljoin(WOO_URL, l) + '&infobox=true'
        gm = u''.join(r.xpath('./td[1]//text()')).strip()
        name = u''.join(r.xpath('./td[2]//text()'))
        count = u''.join(r.xpath('./td[3]//text()')).replace(',', '')
        if not count:
            count = '0'
        #print({'url': gl, 'code': gm, 'name': name, 'count': int(count)})
        logging.info((rc, max_rc))
        gln = gl.replace('&infobox=true', '').strip()
        if (gln != WOO_URL) and (rc < max_rc):
            logging.info(gl)
            fetch_url(gl)
        rc += 1
