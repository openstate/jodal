import json
import logging
import csv
import os.path
import re
from pprint import pformat
import hashlib
from copy import deepcopy
from urllib.parse import urljoin
from time import sleep
import locale
from glob import glob
from collections import OrderedDict

import requests

from jodal.es import setup_elasticsearch
from jodal.scrapers import (
    MemoryMixin, ElasticsearchMixin, ElasticsearchBulkMixin, BaseScraper,
    BaseWebScraper)

def openspending_compare_run(kwargs):
    logging.info(format(kwargs))
    year_mapping = {}
    muni_mapping = {}
    gov_slugs = {}
    municipalities = requests.get('https://www.openspending.nl/api/v1/governments/?limit=10000').json()
    for m in municipalities['objects']:
        gov_slugs[m['code']] = m['slug']
    for p in glob(os.path.join(kwargs['path'], '*.json')):
        logging.info(p)
        entries = []
        with open(p, 'r') as in_file:
            entries = json.load(in_file)
        if len(entries) <= 0:
            logging.warning('%s was empty!' % (p,))
            continue
        loc = entries[0]['locatie_code']
        year = entries[0]['jaar']
        try:
            year_mapping[loc][year] = p
        except LookupError as e:
            year_mapping[loc] = {year: p}
        muni_mapping[loc] = entries[0]['locatie']
    logging.info(pformat(year_mapping))
    for l in muni_mapping.keys():
        difference = {}
        amounts = {}
        for y, p in year_mapping[l].items():
            entries = []
            with open(p, 'r') as in_file:
                entries = json.load(in_file)
            if len(entries) <= 0:
                logging.warning('%s was empty!' % (p,))
                continue
            amounts[y] = sorted(entries, key=lambda i: i['bedrag'])
            for e in entries:
                if e['soort'].lower() != 'lasten':
                    continue
                if e['type'].lower() != 'functie':
                    continue
                key = '%s-%s-%s' % (e['soort'], e['type'], e['code'])
                if y == 2022:
                    try:
                        difference[key] = e['bedrag'] - difference[key]
                    except KeyError as e:
                        pass  # no coparison for this function or category
                else:
                    difference[key] = e['bedrag']
        if y == 2022:
            logging.info(l)
            sorted_difference = OrderedDict(
                sorted(difference.items(), key=lambda item: item[1]))
            #logging.info(pformat(sorted_difference))
            #logging.info(pformat(amounts[y]))
            logging.info(
                'https://openspending.nl/%s/begroting/2022-0/lasten/hoofdfuncties/vergelijk/%s/begroting/2021-0/' % (
                    gov_slugs[l], gov_slugs[l],))
