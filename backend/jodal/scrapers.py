import logging

import requests


class MemoryMixin(object):
    items = []

    def load(self, item):
        # logging.info('Should load item %s now' % (item,))
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
        if url is not None:
            logging.info('Fetching data for : %s' % (url,))
            payload = getattr(self, 'payload', None)
            if payload is not None:
                return requests.post(url, headers=headers, data=json.dumps(payload)).json()
            else:
                return requests.get(url, headers=headers).json()
