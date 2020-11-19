import json
import logging

import requests

class MemoryMixin(object):
    items = []

    def load(self, item):
        logging.info('Should load item %s now' % (item,))
        self.items.append(item)
        pass


class ElasticsearchMixin(object):
    def load(self, item):
        pass


class BaseScraper(object):
    def __init__(self, *arg, **kwargs):
        pass

    def setup(self):
        pass

    def teardown(self):
        pass

    def fetch(self):
        raise NotImplementedError

    def transform(self, item):
        raise NotImplementedError

    def load(self, item):
        raise NotImplementedError

    def run(self):
        self.setup()
        result = self.fetch()
        logging.info("Fetched %s items ..." % (len(result),))
        for i in result:
            t = self.transform(i)
            self.load(t)
        self.teardown()


class BaseLocationScraper(BaseScraper):
    name = None
    url = None
    payload = None
    headers = None

    def fetch(self):
        if self.url is not None:
            logging.info('Fetching data for : %s' % (self.url,))
            if self.payload is not None:
                return requests.post(self.url, headers=self.headers, data=json.dumps(self.payload)).json()
            else:
                return requests.get(self.url, headers=self.headers).json()


class PoliFlwLocationScraper(MemoryMixin, BaseLocationScraper):
    name = 'poliflw'
    url = 'https://api.poliflw.nl/v0/search'
    payload = {"facets":{"location":{"size":1000}},"size":0}

    def fetch(self):
        response = super(PoliFlwLocationScraper, self).fetch()
        #logging.info(response)
        return response['facets']['location']['buckets']

    def transform(self, item):
        return {
            'name': item['key'],
            'id': item['key'],
            'source': self.name
        }


class OpenspendingLocationScraper(MemoryMixin, BaseLocationScraper):
    name = 'openspending'
    url = 'https://www.openspending.nl/api/v1/governments/?limit=1000'

    def fetch(self):
        response = super(OpenspendingLocationScraper, self).fetch()
        #logging.info(response)
        return response['objects']

    def transform(self, item):
        return {
            'name': item.get('name', None),
            'id': 'https://www.openspending.nl%s' % (item['resource_uri'],),
            'kind': item['kind'],
            'parent_kind': item['state'],
            'source': self.name
        }



class OpenBesluitvormingLocationScraper(MemoryMixin, BaseLocationScraper):
    name = 'openbesluitvorming'
    url = 'https://api.openraadsinformatie.nl/v1/elastic/ori_*/_search'
    payload = {
      "size": 500,
      "query": {
          "bool": {
              "must": {
                  "match_all": {}
              },
              "filter": {
                  "terms": {
                      "classification": ["municipality", "province"]
                  }
              }
          }
      }
    }
    headers = {
        'Content-type': 'application/json'
    }

    def fetch(self):
        response = super(OpenBesluitvormingLocationScraper, self).fetch()
        #logging.info(response)
        return response['hits']['hits']

    def transform(self, item):
        return {
            'name': item['_source'].get('name', '').replace('Gemeente ', ''),
            'id': '%s%s' % (item['_source']['@context']['@base'], item['_source']['@id'],),
            'kind': item['_source']['classification'],
            'source': self.name
        }


class LocationsScraperRunner(object):
    scrapers = [
        PoliFlwLocationScraper,
        OpenspendingLocationScraper,
        OpenBesluitvormingLocationScraper
    ]

    def aggregate(self, items):
        result = {}
        for i in items:
            name = i['name']  # .replace('Gemeente ', '')
            if name not in result:
                result[name] = {
                    'sources': [], 'ids': []
                }
            result[name]['name'] = name
            result[name]['sources'].append(i['source'])
            result[name]['ids'].append(i['id'])
        logging.info('Aggregation resulted in %s items ' % (len(result.values())))
        for k,r in result.items():
            if len(r['sources']) == 1:
                logging.info(r)
        # logging.info(result.keys())

    def run(self):
        items = []
        for scraper in self.scrapers:
            k = scraper()
            try:
                k.run()
                items += k.items
            except Exception as e:
                logging.error(e)
                raise e
        logging.info('Fetching resulted in %s items ...' % (len(items)))
        self.aggregate(items)
