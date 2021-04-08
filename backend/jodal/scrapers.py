import json
import logging

import requests
from elasticsearch.helpers import bulk
from jodal.es import setup_elasticsearch


class MemoryMixin(object):
    def load(self, item):
        items = getattr(self, 'items', None)
        if items is None:
            self.items = []
        if isinstance(item, list):
            self.items += item
        else:
            self.items.append(item)


class ElasticsearchMixin(object):
    es = None

    def _init_es(self):
        if self.es is None:
            logging.info('Elasticsearch: setting up')
            self.es = setup_elasticsearch()

    def load(self, item):
        self._init_es()


class ElasticsearchBulkMixin(MemoryMixin, ElasticsearchMixin):
    def setup(self):
        self._init_es()

    def teardown(self):
        result = bulk(self.es, self.items, False)
        logging.info(result)
        self.items = []


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

    def next(self):
        raise NotImplementedError

    def run_for_page(self):
        self.setup()
        result = self.fetch()
        logging.info("Fetched %s items ..." % (len(result),))
        for i in result:
            t = self.transform(i)
            self.load(t)
        self.teardown()

    def run(self):
        another_one = True
        while another_one is not None:
            self.run_for_page()
            another_one = self.next()

class BaseWebScraper(BaseScraper):
    def fetch(self):
        url = getattr(self, 'url', None)
        headers = getattr(self, 'headers', None)
        method = getattr(self, 'method', 'post')
        result = None
        if url is not None:
            logging.info('Fetching data for : %s' % (url,))
            payload = getattr(self, 'payload', None)
            if payload is not None:
                logging.info('Fetch payload: %s' % (payload,))
                f = getattr(requests, method)
                result = f(url, headers=headers, data=json.dumps(payload))
            else:
                params = getattr(self, 'params', None)
                logging.info('Fetch params: %s' % (params,))
                result = requests.get(url, headers=headers, params=params)
        self.result = result
        if result is not None:
            self.result_json = result.json()
            return self.result_json

    def next(self):
        return None
