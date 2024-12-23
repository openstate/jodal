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

from jodal.utils import load_config
from jodal.es import setup_elasticsearch
from jodal.redis import setup_redis
from jodal.scrapers import (
    MemoryMixin, ElasticsearchMixin, ElasticSearchBulkLocationMixin, BaseScraper,
    BaseWebScraper, BaseFromElasticsearch)

WOO_URL = 'https://pid.wooverheid.nl/?pid=nl&dim=publisher&category=Gemeente'
WOO_TIMEOUT = (5,15)

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
        self.max_count = kwargs['max_count']
        self.item_count = 0
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
                    result[p['id']] = { "id": cbs_id, "name": p['name'] }
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
            result = sorted(
                result['infobox'].get('foi_dossiers', []),
                key=lambda d: d['foi_retrievedDate'])
            result.reverse()
            return result
        else:
            return []

    def setup(self):
        self._init_es()
        self.redis_client = setup_redis(self.config)

    def _get_hashed_id(self, dc_identifier):
        h_id = hashlib.sha1()
        h_id.update(dc_identifier.encode('utf-8'))
        return h_id.hexdigest()

    def transform(self, item):
        #logging.info(item)
        names = getattr(self, 'names', None) or [self.name]
        result = []
        for n in names:
            if ((item['foi_retrievedDate'] is not None) and
                ((item['foi_retrievedDate'] < str(self.date_from)) or
                (item['foi_retrievedDate'] > str(self.date_to)))):
                    continue
            data = {}
            r_uri = item['dc_identifier']
            h_id = self._get_hashed_id(r_uri)
            if item.get('dc_publisher', None) in self.locations:
                description = item.get('dc_description', '').strip()
                title = item.get('dc_title', '').strip()
                if (description == '') and (title == ''):
                    continue
                ud = item.get('foi_updateDate') or item['foi_retrievedDate']
                item_type = item['dc_type_description']
                if 'aanvraag omgevingsvergunning' in title.lower():
                    item_type = 'Aanvraag'
                if 'verleende omgevingsvergunning' in title.lower():
                    item_type = 'Verlening'
                r = {
                    '_id': h_id,
                    '_index': 'jodal_documents',
                    'id': h_id,
                    'identifier': r_uri,
                    'url': 'https://pid.wooverheid.nl/?doi=%s' % (r_uri,),
                    'location': self.locations[item['dc_publisher']]["id"],
                    'location_name': self.locations[item['dc_publisher']]["name"],
                    'title': title,
                    'description': description,
                    'created': item['foi_retrievedDate'],
                    'modified': ud,
                    'published': item['foi_retrievedDate'],
                    'processed': datetime.datetime.now().isoformat(),
                    'source': self.name,
                    'type': item_type,
                    'data': data
                }

                self.item_count = 0
                if self.item_count < self.max_count:
                    with Connection(self.redis_client):
                        q = Queue()
                        q.enqueue(fetch_attachments, r, [f for f in item.get('foi_files', []) if f.get('dc_source', '').endswith('.pdf')])
                        logging.info('Enqueued woo individual item %s (%s)' % (h_id, item['foi_retrievedDate'],))
                    self.item_count += 1

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

def fetch_attachments(result_item, documents):
    config = load_config()
    es = setup_elasticsearch(config)
    converted_documents = 0
    for fd in documents:
        if not fd.get('dc_source', '').endswith('.pdf'):
            logging.info('Skipping foi document %s since it is not a pdf' % (fd.get('dc_source', ''),))
            continue
        resp = requests.get('http://texter/convert', params={
            'url': fd['dc_source'],
            'filetype': 'pdf'
        }, timeout=WOO_TIMEOUT)
        if resp.status_code == 200:
            t = resp.json()
            result_item['description'] += "\n\n" + fd['dc_title'] + "\n\n" + t.get('text', '')
            converted_documents += 1
        sleep(1)

    logging.info('Converted %s documents' % (converted_documents,))
    logging.info("Result item: %s" % (result_item,))
    # only index when there are in fact attached pdfs
    if converted_documents > 0:
        bulk(es, [result_item], False)



def fetch_url(url, max_count, date_from=None, date_to=None):
    config = load_config()
    es = setup_elasticsearch(config)
    redis_client = setup_redis(config)
    df = date_from
    dt = date_to
    kwargs = {
        'config': config,
        'date_from': df,
        'date_to': dt,
        'url': url,
        'max_count': max_count
    }
    WoogleScraperRunner().run(**kwargs)

def test():
    print("Test")
    url = 'https://pid.wooverheid.nl/?doi=nl.gm0518&infobox=true'
    fetch_url(url)

def load_counts():
    result = {}
    with open('./woo-counts.json', 'r') as in_file:
        result = json.load(in_file)
    return result

def save_counts(results):
    counts = {}
    for gm in results.keys():
        counts[gm] = results[gm]['count']
    with open('./woo-counts.json', 'w') as out_file:
        json.dump(counts, out_file)

def run(config={}, date_from=None, date_to=None, force=False):
    redis_client = setup_redis(config)

    resp = requests.get(WOO_URL, timeout=WOO_TIMEOUT)
    if resp.status_code != 200:
        logging.warning('Page not fetched correctly!')
        return

    html = etree.HTML(resp.content)

    rc = 0
    max_rc = 0
    results = {}
    for r in html.xpath("//table//tr"):
        #print(r)
        try:
            l = r.xpath('./td[1]/a/@href')[0]
        except LookupError as e:
            l = None
        gl = urljoin(WOO_URL, l) + '&infobox=true'
        #gl = urljoin(WOO_URL, l) + '.2i&infobox=true'
        gm = u''.join(r.xpath('./td[1]//text()')).strip()
        name = u''.join(r.xpath('./td[2]//text()'))
        count = u''.join(r.xpath('./td[4]//text()')).replace(',', '')
        if not count:
            count = '0'
        #print({'url': gl, 'code': gm, 'name': name, 'count': int(count)})
        #logging.info((rc, max_rc))
        gln = gl.replace('&infobox=true', '').strip()
        if (gln != WOO_URL):
            logging.info(gl)
            result = {
                'url': gl, 'code': gm, 'name': name, 'count': int(count)}
            results[gm] = result

    try:
        old_counts = load_counts()
    except (json.decoder.JSONDecodeError, FileNotFoundError) as e:
        old_counts = {}

    for gm in results.keys():
        num_current = results[gm]['count']
        try:
            num_old = old_counts[gm]
        except LookupError as e:
            num_old = 0
            # num_old = num_current - 5
        if force:
            num_old = 0
        if num_old == num_current:
            print("%s has the same counts, skipping" % (gm,))
            continue
        print("Now getting result for %s" % (gm,))
        with Connection(redis_client):
            q = Queue()
            q.enqueue(
                fetch_url, results[gm]['url'], num_current - num_old, date_from, date_to)
    save_counts(results)
    #pprint(results)
