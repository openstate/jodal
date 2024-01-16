import re
from urllib.parse import urljoin
import logging
from time import sleep
import hashlib
import datetime

import requests
from lxml import etree

from jodal.utils import load_config
from jodal.es import setup_elasticsearch
from jodal.scrapers import (
    MemoryMixin, ElasticsearchMixin, ElasticsearchBulkMixin, BaseScraper,
    BaseWebScraper, BaseFromElasticsearch)

WOO_URL = 'https://doi.wooverheid.nl/?doi=nl&dim=publisher&category=Gemeente'


class DocumentsScraper(ElasticsearchBulkMixin, BaseWebScraper):
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

def test():
    print("Test")
    config = load_config()
    es = setup_elasticsearch(config)
    df = None
    dt = None
    url = 'https://doi.wooverheid.nl/?doi=nl.gm0518&infobox=true'
    kwargs = {
        'config': config,
        'date_from': df,
        'date_to': dt,
        'url': url
    }
    WoogleScraperRunner().run(**kwargs)

def run():
    resp = requests.get(WOO_URL)
    print(resp)
    if resp.status_code != 200:
        return

    html = etree.HTML(resp.content)

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
        print({'url': gl, 'code': gm, 'name': name, 'count': int(count)})
