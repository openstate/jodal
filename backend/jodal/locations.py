import json
import logging
import csv
import os.path
import re
from pprint import pformat
import hashlib
from copy import deepcopy

import requests

from jodal.es import setup_elasticsearch
from jodal.scrapers import MemoryMixin, ElasticsearchMixin, BaseScraper


class BaseLocationScraper(BaseScraper):
    name = None
    url = None
    payload = None
    headers = None

    def __init__(self, *args, **kwargs):
        super(BaseLocationScraper, self).__init__(*args, **kwargs)

    def fetch(self):
        if self.url is not None:
            logging.info('Fetching data for : %s' % (self.url,))
            if self.payload is not None:
                return requests.post(self.url, headers=self.headers, data=json.dumps(self.payload)).json()
            else:
                return requests.get(self.url, headers=self.headers).json()

    def transform(self, item):
        names = getattr(self, 'names', None) or [self.name]
        result = []
        for n in names:
            r = deepcopy(item)
            r['source'] = n
            result.append(r)
        return result


class PoliFlwLocationScraper(MemoryMixin, BaseLocationScraper):
    name = 'poliflw'
    url = 'https://api.poliflw.nl/v0/search'
    payload = {"facets":{"location":{"size":1000}},"size":0}

    def _sanatize_name(self, name):
        output = re.sub('^\s*\-?\s*', '', name)
        return output[0].capitalize() + output[1:]

    def fetch(self):
        response = super(PoliFlwLocationScraper, self).fetch()
        return response['facets']['location']['buckets']

    def transform(self, item):
        name = self._sanatize_name(item['key'])
        return super(PoliFlwLocationScraper, self).transform({
            'name': name,
            'id': item['key'],
            'source': self.name
        })


class OpenspendingCountyLocationScraper(MemoryMixin, BaseLocationScraper):
    name = 'openspending'
    url = 'https://www.openspending.nl/api/v1/governments/?kind=county&limit=1000'

    def fetch(self):
        response = super(OpenspendingCountyLocationScraper, self).fetch()
        return response['objects']

    def transform(self, item):
        name = item['name']
        return super(OpenspendingCountyLocationScraper, self).transform({
            'name': name,
            'id': item['code'],  # 'https://www.openspending.nl%s' % (item['resource_uri'],),
            'kind': item['kind'],
            'parent_kind': item['state'],
            'source': self.name
        })

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
        return super(OpenBesluitvormingLocationScraper, self).transform({
            'name': name,
            'id': '%s%s' % (item['_source']['@context']['@base'], item['_source']['@id'],),
            'kind': item['_source']['classification'],
            'source': self.name
        })


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
        result = {}
        for r in renames:
            if r['Bron'] not in result:
                result[r['Bron']] = {r['Naam']: r}
            else:
                result[r['Bron']][r['Naam']] = r
        return result

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
        renames = self.read_renames()
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
            if name in renames.get(i['source'], {}):
                logging.info('Renamig %s => %s for %s' % (name, renames[i['source']][name]['Uniform'],i['source'],))
                name = renames[i['source']][name]['Uniform']

            if name not in location_names:
                continue

            if name not in result:
                result[name] = [l for l in locations if l['name'] == name][0]
                result[name].update({
                    'sources': []
                })
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
                        'name': i['name'],
                        'source': i['source'],
                        'id': i['id']})
        logging.info('Aggregation resulted in %s items ' % (len(result.values())))
        #logging.info(pformat(unmatched))
        logging.info('Total counts: %s' % (total_counts,))
        logging.info('Matched counts: %s' % (matched_counts,))
        logging.info('Final result has %s items' % (len(result),))
        return result.values()

    def run(self):
        items = []
        for scraper in self.scrapers:
            k = scraper()
            try:
                k.items = []
                k.run()
                items += k.items
            except Exception as e:
                logging.error(e)
                raise e
        logging.info('Fetching resulted in %s items ...' % (len(items)))
        locations = self.aggregate(items)
        es = setup_elasticsearch()
        for l in locations:
            if not es.exists(id=l['id'], index='jodal_locations'):
                es.create(id=l['id'], index='jodal_locations', body=l)
