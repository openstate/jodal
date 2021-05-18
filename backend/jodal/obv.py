import json
import logging
import csv
import os.path
import re
from pprint import pformat
import hashlib
from copy import deepcopy
from urllib.parse import urljoin, quote
from time import sleep
import locale
import urllib

import requests

from jodal.es import setup_elasticsearch
from jodal.scrapers import (
    MemoryMixin, ElasticsearchMixin, ElasticsearchBulkMixin, BaseScraper,
    BaseWebScraper)

def _encode_uri_component(s):
     return quote(s, safe='~()*!.\'')

class MeetingsAndAgendaScraper(ElasticsearchBulkMixin, BaseWebScraper):
    name = 'openbesluitvorming'
    url = 'https://api.openraadsinformatie.nl/v1/elastic/_search'
    types = ["AgendaItem", "Meeting"]
    date_field = 'start_date'
    payload = {
        "aggs": {
          "types": {
            "terms": {
              "field": "@type.keyword"
            }
          }
        },
        "query": {
          "bool": {
            "must": [
              {
                "simple_query_string": {
                    "query": "*",
                    "fields": ["name", "description", "text"]
                }
              }
            ],
            "filter": [
              # {"terms": {"has_organization_name": ids_only}},
              #{"terms": {"@type.keyword": types}},
              #{"range": {"start_date": {"lte": "now"}}}
            ]
          }
        },
        "highlight": {
          "fields": {
            "name": {},
            "description": {},
            "text": {}
          }
        },
        "_source": {
          "includes": [
            "*"
          ],
          "excludes": []
        },
        "size":10,
        "sort": {
            "start_date": {
                "order": "desc"
            }
        }
    }
    headers = {
        'Content-type': 'application/json'
    }

    def __init__(self, *args, **kwargs):
        super(MeetingsAndAgendaScraper, self).__init__(*args, **kwargs)
        self.payload['query']['bool']['filter'] = []
        self.payload['query']['bool']['filter'].append(
              {"terms": {"@type.keyword": self.types}})
        self.payload['query']['bool']['filter'].append(
              {"range": {self.date_field: {"lte": "now"}}})
        self.payload['sort'] = {
            self.date_field: {"order": "desc"}}
        self.config = kwargs['config']
        self.date_from = kwargs['date_from']
        self.date_to = kwargs['date_to']
        self.scroll = kwargs.get('scroll', None)
        if self.scroll is not None:
            self.payload['scroll'] = self.scroll
        self.locations = None
        logging.info('Scraper: fetch from %s to %s, scroll time %s' % (
            self.date_from, self.date_to, self.scroll,))

    def _get_poliflw_locations(self):
        result = {}
        logging.info('Fetching locations')
        results = self.es.search(index='jodal_locations', body={"size":1000})
        for l in results.get('hits', {}).get('hits', []):
            cbs_id = l['_id']
            for p in l['_source'].get('sources', []):
                if p['source'] == self.name:
                    result[p['id']] = cbs_id
        return result

    def next(self):
        if len(self.result_json.get('item', [])) > 0:
            scroll_id = self.result_json.get('meta', {}).get('scroll', None)
            if scroll_id is not None:
                self.payload['scroll_id'] = scroll_id
            self.payload['from'] += 10
            return True

    def fetch(self):
        if self.locations is None:
            self.locations = self._get_poliflw_locations()
        sleep(1)
        # self.payload['filters']['date']['from'] = str(self.date_from)
        # self.payload['filters']['date']['to'] = str(self.date_to)
        result = super(MeetingsAndAgendaScraper, self).fetch()
        if result is not None:
            logging.info(
                'Scraper: in total %s results' % (result['hits']['total'],))
            return result.get('hits', {}).get('hits', [])
        else:
            return []

    def _get_description(self, sitem):
        full_text = ''
        if sitem.get('text_pages') is not None:
            full_text = '<p>' + "</p><p>".join(
                [p['text'] for p in sitem['text_pages']]) + '</p>';
        else:
            full_text = sitem.get('text', '')
        return full_text

    def transform(self, item):
        sitem = item['_source']
        names = getattr(self, 'names', None) or [self.name]
        result = []
        for n in names:
            r_uri = urljoin(sitem['@context']['@base'], sitem['@id'])
            h_id = hashlib.sha1()
            h_id.update(r_uri.encode('utf-8'))
            data = {}
            if sitem.get('has_organization_name', None) is not None:
                location_uri = urljoin(
                    sitem['@context']['@base'], sitem['has_organization_name'])
                location_id = self.locations[location_uri]
                # logging.info('%s => %s' % (location_uri, location_id,))
                # 'https://openbesluitvorming.nl/?zoekterm=' + encodeURIComponent(query) + '&organisaties=%5B%22' + i._index + '%22%5D&showResource=' + encodeURIComponent(encodeURIComponent('https://id.openraadsinformatie.nl/' + i._id))
                obv_url = 'https://openbesluitvorming.nl/?zoekterm=%22*%22&organisaties=%5B%22' + item['_index'] + '%22%5D&showResource=' + _encode_uri_component(_encode_uri_component(r_uri))
                r = {
                    '_id': h_id.hexdigest(),
                    '_index': 'jodal_documents',
                    'id': h_id.hexdigest(),
                    'identifier': r_uri,
                    'url': obv_url,
                    'location': location_id,
                    'title': sitem.get('title', ''),
                    'description': self._get_description(sitem),
                    'created': sitem[self.date_field],
                    'modified': sitem[self.date_field],
                    'published': sitem[self.date_field],
                    'source': self.name,
                    'type': 'Bericht',  #todo actual type
                    'data': data
                }
                result.append(r)

        # logging.info(pformat(result))
        return result


class MediaObjectsScraper(MeetingsAndAgendaScraper):
    types = ['MediaObject']
    date_field = 'last_discussed_at'


class OpenbesluitvormingScraperRunner(object):
    scrapers = [
        MeetingsAndAgendaScraper,
        MediaObjectsScraper
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
        logging.info('Fetching resulted in %s items ...' % (len(items)))
