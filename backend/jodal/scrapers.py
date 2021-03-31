import json
import logging

import requests


class MemoryMixin(object):

    def load(self, item):
        # logging.info('Should load item %s now' % (item,))
        items = getattr(self, 'items', None)
        if items is None:
            self.items = []
        if isinstance(item, list):
            self.items += item
        else:
            self.items.append(item)


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
        if result is not None:
            return result.json()
