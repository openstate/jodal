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
        logging.info(
            'Elasticsearch: bulk storing %s items' % (len(self.items),))
        result = bulk(self.es, self.items, False)
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
        # logging.info("Fetched %s items ..." % (len(result),))
        if result is not None:
            for i in result:
                t = self.transform(i)
                self.load(t)
        self.teardown()

    def run(self):
        another_one = True
        while another_one is not None:
            self.run_for_page()
            another_one = self.next()

class ElasticSearchScraper(BaseScraper):
    def __init__(self, *args, **kwargs):
        super(ElasticSearchScraper, self).__init__(*args, **kwargs)
        self.config = kwargs['config']
        logging.info('Elasticsearch scraper started')

class BaseWebScraper(BaseScraper):
    def fetch(self):
        try:
            url = getattr(self, 'url', None)
            headers = getattr(self, 'headers', None)
            method = getattr(self, 'method', 'post')
            result = None
            if url is not None:
                payload = getattr(self, 'payload', None)
                params = getattr(self, 'params', None)
                logging.info('%s : %s , payload/params: %s' % (
                    method, url, payload or params))
                if payload is not None:
                    f = getattr(requests, method)
                    result = f(url, headers=headers, data=json.dumps(payload), timeout=20)
                else:
                    result = requests.get(url, headers=headers, params=params, timeout=20)
            self.result = result
            if result is not None:
                self.result_json = result.json()
                return self.result_json
        except requests.exceptions.RequestException as e:
            self.result = None
            self.result_json = {}
            pass

    def next(self):
        return None


class BaseFromElasticsearch(MemoryMixin, BaseWebScraper):
    def __init__(self, *args, **kwargs):
        super(BaseFromElasticsearch, self).__init__(*args, **kwargs)
        self.config = kwargs['config']
        self.document_id = kwargs['document_id']
        logging.info('Fetching document %s' % (self.document_id,))

    def next(self):
        pass

    def fetch(self):
        self.es = setup_elasticsearch(self.config)
        item = self.es.get(index='jodal_documents', id=self.document_id)
        return [item]

    def transform(self, item):
        return item
