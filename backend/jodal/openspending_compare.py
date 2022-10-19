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

def get_municipalities():
    gov_slugs = {}
    municipalities = requests.get('https://www.openspending.nl/api/v1/governments/?limit=10000').json()
    for m in municipalities['objects']:
        gov_slugs[m['code']] = m['slug']
    return gov_slugs

def get_year_and_municipalities_mappings(kwargs):
    year_mapping = {}
    muni_mapping = {}
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
        period = entries[0]['periode']
        if str(year) == str(kwargs['year1']):
            if str(period) != str(kwargs['period1']):
                continue
        elif str(year) == str(kwargs['year2']):
            if str(period) != str(kwargs['period2']):
                continue
        else:
            continue
        try:
            year_mapping[loc][year] = p
        except LookupError as e:
            year_mapping[loc] = {year: p}
        muni_mapping[loc] = entries[0]['locatie']
    return year_mapping, muni_mapping

def tmpl(template_path, context):
    content = ''
    with open(template_path, 'r') as in_file:
        content = in_file.read()
    for k, v in context.items():
        content = content.replace('{%s}' % (k,), v)
    return content

def openspending_compare_run(kwargs):
    logging.info(format(kwargs))
    year_mapping = {}
    muni_mapping = {}
    gov_slugs = get_municipalities()
    year_mapping, muni_mapping = get_year_and_municipalities_mappings(kwargs)
    labels_mapping = {}
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
            amounts[y] = sorted(entries, key=lambda i: -i['bedrag'])
            for e in entries:
                if e['soort'].lower() != 'lasten':
                    continue
                if e['type'].lower() != 'functie':
                    continue
                key = '%s-%s-%s' % (e['soort'], e['type'], e['code'])
                labels_mapping[key] = e['naam']
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
            if len(sorted_difference.keys()) <= 0:
                continue
            #logging.info(pformat(sorted_difference))
            #logging.info(pformat(amounts[y]))
            y1 = kwargs['year1']
            p1 = kwargs['period1']
            if str(p1) == '0':
                k1 = 'begroting'
            else:
                k1 = 'realisatie'
            y2 = kwargs['year2']
            p2 = kwargs['period2']
            if str(p2) == '0':
                k2 = 'begroting'
            else:
                k2 = 'realisatie'
            lnk = 'https://openspending.nl/%s/%s/%s-%s/lasten/hoofdfuncties/vergelijk/%s/%s/%s-%s/' % (
                gov_slugs[l], k1, y1, p1, gov_slugs[l], k2, y2, p2,)
            logging.info(lnk)
            biggest_gainer, biggest_gainer_amount = list(sorted_difference.items())[-1]
            hp =  [(a['naam'], a['bedrag'],) for a in amounts[y] if (a['type'] == 'Functie') and (a['soort'] == 'lasten')][0]
            highest_post, highest_post_amount = hp
            result = tmpl(os.path.join(kwargs['templates'], '1.txt'), {
                'naam': muni_mapping[l],
                'link': lnk,
                'grootste_stijger': str(labels_mapping[biggest_gainer]),
                'grootste_stijger_bedrag': str(biggest_gainer_amount),
                'hoogste_kostenpot': highest_post,
                'hoogste_kostenpot_bedrag': str(highest_post_amount)
            })
            with open(os.path.join(kwargs['output'], '%s.txt' % (l,)), 'w') as out_file:
                out_file.write(result)
            logging.info(result)
