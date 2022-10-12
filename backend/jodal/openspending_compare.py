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

import requests

from jodal.es import setup_elasticsearch
from jodal.scrapers import (
    MemoryMixin, ElasticsearchMixin, ElasticsearchBulkMixin, BaseScraper,
    BaseWebScraper)

def openspending_compare_run(kwargs):
    logging.info(format(kwargs))
    year_mapping = {}
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
