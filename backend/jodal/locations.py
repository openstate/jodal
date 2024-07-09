import json
import logging
import csv
import os.path
import re
from pprint import pformat
import hashlib
from copy import deepcopy
from urllib.parse import urljoin

import requests
from elasticsearch.helpers import bulk
from lxml import etree

from jodal.es import setup_elasticsearch
from jodal.scrapers import MemoryMixin, ElasticsearchMixin, BaseScraper, ElasticsearchBulkMixin


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

    def next(self):
        return None


class OverheidsOrganisatiesScraper(MemoryMixin, BaseLocationScraper):
    name = 'oo'
    url = 'https://organisaties.overheid.nl/archive/exportOO.xml'
    nsmap = {}

    def fetch(self):
        xml = etree.XML(requests.get(self.url).content)
        self.nsmap = xml.nsmap
        return xml.xpath('//p:organisaties/p:organisatie', namespaces=xml.nsmap)

    def transform(self, item):
        result = {
            'name': u''.join(item.xpath('./p:naam//text()', namespaces=self.nsmap)),
            'id': item.xpath('./@p:systeemId', namespaces=self.nsmap)[0],
            'type': item.xpath('./p:types//p:type/text()', namespaces=self.nsmap),
            'source': self.name
        }
        if 'Ministerie' in result['type']:
            result['name'] = 'Ministerie van %s' % (result['name'],)
        return super(OverheidsOrganisatiesScraper, self).transform(result)

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
        item_type = 'Gemeente'
        if name.lower().startswith('provincie'):
            item_type = 'Provincie'
        return super(PoliFlwLocationScraper, self).transform({
            'name': name,
            'id': item['key'],
            'source': self.name,
            'type': [item_type]
        })


class OpenspendingCountyLocationScraper(MemoryMixin, BaseLocationScraper):
    name = 'openspending'
    url = 'https://www.openspending.nl/api/v1/governments/?kind=county&limit=1000'
    item_type = 'Gemeente'

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
            'source': self.name,
            'type': [self.item_type]
        })

class OpenspendingProvinceLocationScraper(OpenspendingCountyLocationScraper):
    name = 'openspending'
    url = 'https://www.openspending.nl/api/v1/governments/?kind=province&limit=1000'
    item_type = 'Provincie'

class OpenBesluitvormingLocationScraper(MemoryMixin, BaseLocationScraper):
    name = 'openbesluitvorming'
    url = 'https://api.openraadsinformatie.nl/v1/elastic/ori_*,osi_*/_search'
    payload = {
      "size": 1000,
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
        if item['_source']['classification'] == 'municipality':
            item_type = 'Gemeente'
        else:
            item_type = 'Provincie'
        return super(OpenBesluitvormingLocationScraper, self).transform({
            'name': name,
            'id': '%s%s' % (item['_source']['@context']['@base'], item['_source']['@id'],),
            'kind': item['_source']['classification'],
            'source': self.name,
            'type': [item_type]
        })


class CVDRLocationScraper(MemoryMixin, BaseLocationScraper):
    name = 'cvdr'
    url = 'https://aleph.openstate.eu/api/2/search?filter%3Aschemata=PublicBody&filter%3Acollection_id=7&limit=10000'

    def _sanatize_name(self, name):
        output = re.sub('^\s*\-?\s*', '', name)
        return output[0].capitalize() + output[1:]

    def fetch(self):
        response = super(CVDRLocationScraper, self).fetch()
        return response['results']

    def transform(self, item):
        name = self._sanatize_name(item['properties']['name'][0])
        return super(CVDRLocationScraper, self).transform({
            'name': name,
            'id': item['id'],
            'source': self.name,
            'type': ['Gemeente']
        })


class WoogleLocationScraper(MemoryMixin, BaseLocationScraper):
    name = 'woogle'
    url = 'https://doi.wooverheid.nl/?doi=nl&dim=publisher&category=Gemeente'

    def _sanatize_name(self, name):
        return name.replace('Gemeente ', '')

    def fetch(self):
        resp = requests.get(self.url, headers=self.headers)
        html = etree.HTML(resp.content)
        results = []

        for r in html.xpath("//table//tr"):
            #print(r)
            try:
                l = r.xpath('./td[1]/a/@href')[0]
            except LookupError as e:
                l = None
            gl = urljoin(self.url, l)
            gm = u''.join(r.xpath('./td[1]//text()')).strip()
            name = u''.join(r.xpath('./td[2]//text()'))
            count = u''.join(r.xpath('./td[3]//text()')).replace(',', '')
            if not count:
                count = '0'
            results.append({
                'url': gl,
                'code': gm,
                'name': name,
                'count': int(count)
            })

        return results

    def transform(self, item):
        name = self._sanatize_name(item['name'])
        return super(WoogleLocationScraper, self).transform({
            'name': name,
            'id': item['code'],
            'source': self.name,
            'type': ['Gemeente']
        })

class LocationsScraperRunner(object):
    scrapers = [
        PoliFlwLocationScraper,
        #OpenspendingCountyLocationScraper,
        #OpenspendingProvinceLocationScraper,
        OpenBesluitvormingLocationScraper,
        CVDRLocationScraper,
        WoogleLocationScraper,
        OverheidsOrganisatiesScraper
    ]
    year = '2023'

    def read_renames(self):
        renames = []
        filepath = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '../mappings/gemeenten-uniform-%s.csv' % (self.year,)))
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
            os.path.dirname(__file__), '../mappings/gemeenten-%s.csv' % (self.year,)))
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
                'type': ['Gemeente'],
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
                'type': ['Provincie'],
                'source': 'cbs'}
        return list(provinces.values())

    def extract_oo(self, items):
        return [i for i in items if (i['source'] == 'oo' and 'Ministerie' in i['type'])]

    def get_hash(self, source, identifier):
        return '%s:%s' % (source, identifier,)

    def aggregate(self, items):
        result = {}
        renames = self.read_renames()
        municipalities = self.read_municipalities()
        # logging.info(municipalities)
        provinces = self.extract_provinces(municipalities)
        locations = self.extract_municipalities(municipalities) + provinces
        locations += self.extract_oo(items)

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
        all_items = [
            {
                'name': 'Alles',
                'id': '*',
                'kind': 'municipality',
                'type': 'Aggregatie',
                'source': 'cbs',
                'sources': []
            },
            {
                'name': 'Alle gemeenten',
                'id': 'type:Gemeente',
                'kind': 'municipality',
                'type': 'Aggregatie',
                'source': 'cbs',
                'sources': []
            },
            {
                'name': 'Alle provincies',
                'id': 'type:Provincie',
                'kind': 'municipality',
                'type': 'Aggregatie',
                'source': 'cbs',
                'sources': []
            },
            {
                'name': 'Alle ministeries',
                'id': 'type:Ministerie',
                'kind': 'municipality',
                'type': 'Aggregatie',
                'source': 'cbs',
                'sources': []
            }
        ]
        for scraper in self.scrapers:
            k = scraper()
            for a in all_items:
                a['sources'].append({
                    'name': a['name'],
                    'id': a['id'],
                    'source': k.name
                })
            try:
                k.items = []
                k.run()
                items += k.items
            except Exception as e:
                logging.error(e)
                raise e
        logging.info('Fetching resulted in %s items ...' % (len(items)))
        locations = all_items + list(self.aggregate(items))
        es = setup_elasticsearch()
        for l in locations:
            l['_id'] = l['id']
            l['_index'] = 'jodal_locations'
        result = bulk(es, locations, False)
