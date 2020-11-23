import json
import logging
import csv
import os.path
import re
from pprint import pformat
import hashlib

import requests

class MemoryMixin(object):
    items = []

    def load(self, item):
        # logging.info('Should load item %s now' % (item,))
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
    renames = {}

    def __init__(self, *args, **kwargs):
        super(BaseLocationScraper, self).__init__(*args, **kwargs)
        if self.name is not None and 'renames' in kwargs:
            self.renames = {r['Naam']: r['Uniform'] for r in kwargs['renames'] if r['Bron'] == self.name}

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

    def _sanatize_name(self, name):
        output = re.sub('^\s*\-?\s*', '', name)
        return output[0].capitalize() + output[1:]

    def fetch(self):
        response = super(PoliFlwLocationScraper, self).fetch()
        #logging.info(response)
        logging.info(self.renames)
        return response['facets']['location']['buckets']

    def transform(self, item):
        name = self._sanatize_name(item['key'])
        other_names = []
        if name in self.renames:
            other_names = [name]
            name = self.renames[name]
        return {
            'name': name,
            'other_names': other_names,
            'id': item['key'],
            'source': self.name
        }


class OpenspendingCountyLocationScraper(MemoryMixin, BaseLocationScraper):
    name = 'openspending'
    url = 'https://www.openspending.nl/api/v1/governments/?kind=county&limit=1000'

    def fetch(self):
        response = super(OpenspendingCountyLocationScraper, self).fetch()
        return response['objects']

    def transform(self, item):
        name = item['name']
        other_names = []
        if name in self.renames:
            other_names = [name]
            name = self.renames[name]
        return {
            'name': name,
            'other_names': other_names,
            'id': 'https://www.openspending.nl%s' % (item['resource_uri'],),
            'kind': item['kind'],
            'parent_kind': item['state'],
            'source': self.name
        }

class OpenspendingProvinceLocationScraper(OpenspendingCountyLocationScraper):
    name = 'openspending'
    url = 'https://www.openspending.nl/api/v1/governments/?kind=province&limit=1000'


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
        name = item['_source'].get('name', '').replace('Gemeente ', '').replace('(L)','(L.)')
        other_names = []
        if name in self.renames:
            other_names = [name]
            name = self.renames[name]
        return {
            'name': name,
            'other_names': other_names,
            'id': '%s%s' % (item['_source']['@context']['@base'], item['_source']['@id'],),
            'kind': item['_source']['classification'],
            'source': self.name
        }


class LocationsScraperRunner(object):
    scrapers = [
        PoliFlwLocationScraper,
        OpenspendingCountyLocationScraper,
        OpenspendingProvinceLocationScraper,
        OpenBesluitvormingLocationScraper
    ]

    def read_renames(self):
        renames = []
        filepath = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '../mappings/gemeenten-uniform-2020.csv'))
        with open(filepath, newline='') as f:
            reader = csv.reader(f)
            header = reader.__next__()
            for row in reader:
                renames.append(dict(zip(header, row)))
        return renames

    def read_municipalities(self):
        municipalities = []
        filepath = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '../mappings/gemeenten-2020.csv'))
        with open(filepath, newline='') as f:
            reader = csv.reader(f)
            header = reader.__next__()
            for row in reader:
                municipalities.append(dict(zip(header, row)))
        return municipalities

    def extract_municipalities(self, orig_municipalities):
        municipalities = []
        for m in orig_municipalities:
            r = {
                'name': m['Gemeentenaam'],
                'id': m['GemeentecodeGM'],
                'kind': 'municipality',
                'source': 'cbs'
            }
            municipalities.append(r)
        return municipalities

    def extract_provinces(self, municipalties):
        provinces = {}
        for m in municipalties:
            if m['Provinciecode'] in provinces:
                continue
            provinces[m['ProvinciecodePV']] = {
                'name': 'Provincie %s' % (m['Provincienaam'],),
                'id': m['ProvinciecodePV'],
                'kind': 'province',
                'source': 'cbs'}
        return list(provinces.values())

    def get_hash(self, source, identifier):
        return '%s:%s' % (source, identifier,)

    def aggregate(self, items):
        result = {}
        municipalities = self.read_municipalities()
        # logging.info(municipalities)
        provinces = self.extract_provinces(municipalities)
        locations = self.extract_municipalities(municipalities) + provinces
        location_names = [l['name'] for l in locations]
        # logging.info(locations)
        total_counts = {}
        matched_counts = {}
        unmatched = {}
        for i in items:
            name = i['name']  # .replace('Gemeente ', '')
            if name not in location_names:
                continue

            if name not in result:
                result[name] = {
                    'sources': [], 'other_names': []
                }
            try:
                total_counts[i['source']] += 1
            except KeyError as e:
                total_counts[i['source']] = 1
            if name in location_names:
                try:
                    matched_counts[i['source']] += 1
                except LookupError as e:
                    matched_counts[i['source']] = 1
            else:
                try:
                    unmatched[i['source']].append(name)
                except LookupError as e:
                    unmatched[i['source']] = [name]
            if i['source'] not in result[name]['sources']:
                result[name]['name'] = name
                if self.get_hash(i['source'], i['id']) not in [self.get_hash(s['source'], s['id']) for s in result[name]['sources']]:
                    result[name]['sources'].append({
                        'source': i['source'],
                        'id': i['id']})
                for o in i['other_names']:
                    if self.get_hash(i['source'], o) not in [self.get_hash(s['source'], s['name']) for s in result[name]['other_names']]:
                        result[name]['other_names'] += [{
                            'source': i['source'],
                            'name': n} for n in i['other_names']]
        logging.info('Aggregation resulted in %s items ' % (len(result.values())))
        logging.info(pformat(unmatched))
        logging.info('Total counts: %s' % (total_counts,))
        logging.info('Matched counts: %s' % (matched_counts,))
        # for k,r in result.items():
        #     if len(r['sources']) == 1:
        #         logging.info(r)
        logging.info(pformat(result))
        logging.info('Final result has %s items' % (len(result),))

    def run(self):
        items = []
        renames = self.read_renames()
        for scraper in self.scrapers:
            k = scraper(renames=renames)
            try:
                k.items = []
                k.run()
                items += k.items
            except Exception as e:
                logging.error(e)
                raise e
        logging.info('Fetching resulted in %s items ...' % (len(items)))
        self.aggregate(items)
