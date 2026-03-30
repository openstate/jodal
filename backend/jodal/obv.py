import json
import logging
import csv
import os.path
import re
from pprint import pformat, pprint
import hashlib
from copy import deepcopy
from urllib.parse import urljoin, quote
from time import sleep
import locale
import urllib
import datetime

import requests

from jodal.es import setup_elasticsearch
from jodal.scrapers import (
    MemoryMixin, ElasticsearchMixin, ElasticSearchBulkLocationMixin, BaseScraper,
    BaseWebScraper, BaseFromElasticsearch)

def _encode_uri_component(s):
     return quote(s, safe='~()*!.\'')

class CountsScraper(MemoryMixin, BaseWebScraper):
    url = 'https://api.openraadsinformatie.nl/v1/elastic/ori_*/_search'
    date_field = 'was_generated_by.ended_at_time'
    types = ["AgendaItem", "Meeting"]

    payload = {
        "aggs": {
          "organizations": {
            "terms": {
              "field": "has_organization_name.keyword",
              "size": 10000
            },
            "aggs": {
                "date": {
                    "date_histogram": {
                        "field": "start_date",
                        "interval": "month"
                    }
                }
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
        "from":0,
        "size":0,
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
        super(CountsScraper, self).__init__(*args, **kwargs)
        self.config = kwargs['config']
        self.date_from = kwargs['date_from']
        self.date_to = kwargs['date_to']
        self.threshold = kwargs['threshold']

        self.payload['query']['bool']['filter'] = []
        self.organizations = kwargs.get('organizations', None)
        if self.organizations is not None:
            ids_only = self.organizations.split(',')
            self.payload['query']['bool']['filter'].append(
                {"terms": {"has_organization_name": ids_only}})

        self.payload['from'] = 0
        self.payload['query']['bool']['filter'].append(
              {"terms": {"@type.keyword": self.types}})
        self.payload['query']['bool']['filter'].append(
              {
                "range": {
                    self.date_field: {
                        'from': str(self.date_from),
                        'to': str(self.date_to)
                    }
                }
            })
        # self.payload['query']['bool']['filter'].append(
        #       {
        #         "range": {
        #             "start_date": {
        #                 'to': str(self.date_from)
        #             }
        #         }
        #     })
        logging.info('Scraper: fetch from %s dates %s to %s' % (
            self.organizations, self.date_from, self.date_to,))

    def transform(self, item):
        #pprint(item)
        return item['key']

    def fetch(self):
        # if self.locations is None:
        #     self.locations = self._get_locations()
        # sleep(1)
        result = super(CountsScraper, self).fetch()
        #print(result)
        if result is not None:
            return [x for x in result.get('aggregations', {}).get('organizations', {}).get('buckets', []) if (x.get('doc_count', 0) > self.threshold) and (len(x['date']['buckets']) > 1)]
        else:
            return []



class MeetingsAndAgendaScraper(ElasticSearchBulkLocationMixin, BaseWebScraper):
    name = 'openbesluitvorming'
    url = 'https://api.openraadsinformatie.nl/v1/elastic/_search'
    types = ["AgendaItem", "Meeting"]
    date_field = 'start_date'
    page_size = 50
    obv_types = {
        'MediaObject': 'Bestand',
        'AgendaItem': 'Agendapunt',
        'Report': 'Rapport',
        'Meeting': 'Vergadering',
        'Person': 'Persoon',
        'Membership': 'Lidmaatschap',
        'Organization': 'Organisatie',
        'ImageObject': 'Beeld'
    }
    bestand_types = {
        'agenda': 'Agenda',
        'amendement': 'Amendement',
        'stemuitslag': 'Stemming',
        'raadsmemo': 'Raadsmemo'
    }
    bestand_types_contains = {
        'bijlage': 'Bijlage',
        ' rb ': 'Raadsbesluit',
        'schriftelijke vragen': 'Vragen',
        'raadsvergadering': 'Raadsvergadering',
        'raadsvragen': 'Raadsvragen',
        'raadsvraag': 'Raadsvragen',
        'bestemmingsplan': 'Bestemmingsplan',
        'raadsvoorstel': 'Raadsvoorstel',
        'besluitenlijst': 'Besluitenlijst',
        'brief': 'Brief',
        'motie': 'Motie',
    }
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
        "from":0,
        "size":page_size,
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
        self.payload = deepcopy(self.__class__.payload)
        self.config = kwargs['config']
        self.date_from = kwargs['date_from']
        self.date_to = kwargs['date_to']

        self.payload['query']['bool']['filter'] = []
        self.organizations = kwargs.get('organizations', None)
        if self.organizations is not None:
            ids_only = self.organizations.split(',')
            self.payload['query']['bool']['filter'].append(
                {"terms": {"has_organization_name": ids_only}})

        self.target_index = kwargs.get('target_index', 'jodal_documents')
        self.page_sleep = kwargs.get('page_sleep', 1)

        self.scroll = kwargs.get('scroll', None)
        if self.scroll is not None:
            self.payload['scroll'] = self.scroll

        self.payload.pop('from', None)

        self.payload['query']['bool']['filter'].append(
              {"terms": {"@type": self.types}})
        self.payload['query']['bool']['filter'].append(
              {
                "range": {
                    self.date_field: {
                        'from': str(self.date_from),
                        'to': str(self.date_to)
                    }
                }
            })
        self.payload['sort'] = [
            {self.date_field: {"order": "desc"}},
            {"_id": {"order": "asc"}}
        ]
        self.locations = None

        # Resume support: inject a search_after cursor to skip ahead
        resume_from = kwargs.get('resume_from', None)
        if resume_from:
            self.payload['search_after'] = json.loads(resume_from)
            logging.info('Resuming from cursor: %s' % resume_from)

        logging.info('Scraper: fetch from %s dates %s to %s, scroll time %s' % (
            self.organizations, self.date_from, self.date_to, self.scroll,))

    def _get_locations(self):
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
        hits = self.result_json.get('hits', {}).get('hits', [])
        if hits:
            self.payload['search_after'] = hits[-1]['sort']
            logging.info('CURSOR:%s' % json.dumps(hits[-1]['sort']))
            return True
        self.payload.pop('search_after', None)
        return None

    def fetch(self):
        if self.locations is None:
            self.locations = self._get_locations()
        sleep(self.page_sleep)
        result = super(MeetingsAndAgendaScraper, self).fetch()
        if result is not None:
            n_hits = len(result.get('hits', {}).get('hits', []))
            logging.info(
                'Scraper: got %s of in total %s results' % (
                    n_hits, result['hits']['total'],))
            return result.get('hits', {}).get('hits', [])
        else:
            return []

    def _get_description(self, sitem):
        if sitem.get('text_pages') is not None:
            return '<p>' + '</p><p>'.join(
                [p['text'] for p in sitem['text_pages']]) + '</p>'
        t = sitem.get('text')
        if t is None:
            return ''
        if isinstance(t, list):
            return '\n\n'.join(t)
        return t or ''

    def _get_md_text(self, sitem):
        md = sitem.get('md_text')
        if md is None:
            return ''
        if isinstance(md, list):
            return '\n\n'.join(md)
        return md or ''

    def transform(self, item):
        sitem = item['_source']
        # logging.info("XX: %s" % (sitem['name'],))
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
                try:
                    location_id = self.locations[location_uri]
                except KeyError as e:
                    logging.error("Could not match %s against local locations" % (location_uri,))
                    logging.error(sitem.get('name', '<no name>'))
                    #logging.error(pformat(sitem))
                    location_id = None
                if location_id is not None:
                    # 'https://openbesluitvorming.nl/?zoekterm=' + encodeURIComponent(query) + '&organisaties=%5B%22' + i._index + '%22%5D&showResource=' + encodeURIComponent(encodeURIComponent('https://id.openraadsinformatie.nl/' + i._id))
                    obv_url = 'https://openbesluitvorming.nl/?zoekterm=%22*%22&organisaties=%5B%22' + item['_index'] + '%22%5D&showResource=' + _encode_uri_component(_encode_uri_component(r_uri))
                    obv_type = self.obv_types[sitem['@type']]
                    obv_title = sitem.get('name', '')
                    if obv_type == 'Bestand':
                       obv_title_lower = obv_title.lower()
                       for k, v in self.bestand_types.items():
                           if obv_title_lower.startswith(k):
                               obv_type = v
                       for k, v in self.bestand_types_contains.items():
                           if k in obv_title_lower:
                               obv_type = v

                    r = {
                        '_id': h_id.hexdigest(),
                        '_index': self.target_index,
                        'id': h_id.hexdigest(),
                        'identifier': r_uri,
                        'url': obv_url,
                        'doc_url': sitem.get('original_url'),
                        'location': location_id,
                        'title': sitem.get('name', ''),
                        'description': self._get_description(sitem),
                        'md_text': self._get_md_text(sitem),
                        'created': sitem[self.date_field],
                        'modified': sitem[self.date_field],
                        'published': sitem[self.date_field],
                        'processed': datetime.datetime.now().isoformat(),
                        'source': self.name,
                        'type': obv_type,
                        'data': data
                    }
                    result.append(r)
            else:
                logging.warning("Item has no organization name? %s" % (sitem,))

        #logging.info(pformat(self.locations))
        # logging.info(pformat(result))
        return result


class MediaObjectsScraper(MeetingsAndAgendaScraper):
    types = ['MediaObject']
    date_field = 'last_discussed_at'


class DocumentScraper(BaseFromElasticsearch):
    pass


class OpenbesluitvormingScraperRunner(object):
    scrapers = [
        MeetingsAndAgendaScraper,
        MediaObjectsScraper
    ]
    scraper_names = {
        'meetings': MeetingsAndAgendaScraper,
        'media': MediaObjectsScraper,
    }


    def run(self, *args, **kwargs):
        only = kwargs.pop('only_scrapers', None)
        if only:
            scrapers = [self.scraper_names[n] for n in only.split(',')]
        else:
            scrapers = self.scrapers
        items = []
        for scraper in scrapers:
            k = scraper(**kwargs)
            try:
                k.items = []
                k.run()
                items += k.items
            except Exception as e:
                logging.error(e)
                raise e
        logging.info('Fetching resulted in %s items ...' % (len(items)))


class OpenbesluitvormingDocumentScraperRunner(object):
    scrapers = [
        DocumentScraper
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
        return items

class OpenbesluitvormingCountsScraperRunner(object):
    scrapers = [
        CountsScraper
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
        print("\n".join(items))
        logging.info('Fetching resulted in %s items ...' % (len(items)))
        return items
