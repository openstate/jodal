import json
import logging

import requests

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
        for i in result:
            self.load(self.transform(i))
        self.teardown()


class BaseLocationScraper(BaseScraper):
    url = None
    payload = None

    def fetch(self):
        if self.url is not None:
            logging.info('Fetching data for : %s' % (self.url,))
            if self.payload is not None:
                return requests.post(self.url, data=json.dumps(self.payload)).json()
            else:
                return requests.get(self.url).json()


class PoliFlwLocationScraper(BaseLocationScraper, ElasticsearchMixin):
    url = 'https://api.poliflw.nl/v0/search'
    payload = {"facets":{"location":{"size":1000}},"size":0}

    def fetch(self):
        response = super(PoliFlwLocationScraper, self).fetch()
        #logging.info(response)
        return response['facets']['location']['buckets']

class OpenspendingLocationScraper(BaseLocationScraper, ElasticsearchMixin):
    url = 'https://www.openspending.nl/api/v1/governments/?limit=1000'

    def fetch(self):
        response = super(OpenspendingLocationScraper, self).fetch()
        #logging.info(response)
        return response['objects']

class OpenBesluitvormingLocationScraper(BaseLocationScraper, ElasticsearchMixin):
    pass

class LocationsScraperRunner(object):
    scrapers = [
        PoliFlwLocationScraper,
        OpenspendingLocationScraper,
    ]

    def run(self):
        for scraper in self.scrapers:
            k = scraper()
            try:
                k.run()
            except Exception as e:
                logging.error(e)
