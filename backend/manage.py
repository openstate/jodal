#!/usr/bin/env python
from copy import deepcopy
from datetime import datetime, date, timedelta
import json
from glob import glob
import gzip
from hashlib import sha1
import os
import sys
import time
import logging
from time import sleep
import glob

import requests
from redis import Redis
from rq import Connection, Queue, Worker

import click
from click.core import Command
from click.decorators import _make_command
from elasticsearch.exceptions import NotFoundError
from elasticsearch.helpers import reindex

from jodal.utils import load_config
from jodal.es import setup_elasticsearch
from jodal.redis import setup_redis

from jodal.locations import LocationsScraperRunner
from jodal.openspending import (
    OpenSpendingScraperRunner, OpenSpendingDocumentScraperRunner,
    OpenSpendingCacheScraperRunner)
from jodal.openspending_compare import openspending_compare_run
from jodal.poliflw import PoliflwScraperRunner
from jodal.obv import (OpenbesluitvormingScraperRunner,
    OpenbesluitvormingCountsScraperRunner)
from jodal.cvdr import CVDRScraperRunner
from jodal.scrapers import ElasticSearchScraper, BinoasMixin
from jodal.woo import run

class BinoasUploader(BinoasMixin, ElasticSearchScraper):
    pass

logging.basicConfig(
    format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
    level=logging.INFO)

def command(name=None, cls=None, **attrs):
    """
    Wrapper for click Commands, to replace the click.Command docstring with the
    docstring of the wrapped method (i.e. the methods defined below). This is
    done to support the autodoc in Sphinx, and the correct display of docstrings
    """
    if cls is None:
        cls = Command
    def decorator(f):
        r = _make_command(f, name, attrs, cls)
        r.__doc__ = f.__doc__
        return r
    return decorator


def _create_path(path):
    if not os.path.exists(path):
        click.secho('Creating path "%s"' % path, fg='green')
        os.makedirs(path)

    return path


@click.group()
@click.version_option()
def cli():
    """Open Overheidsdata"""


@cli.group()
def elasticsearch():
    """Manage Elasticsearch"""


@cli.group()
def scrapers():
    """Manage scrapers"""


@cli.group()
def openspending():
    """Manage openspending stuff"""


@cli.group()
def worker():
    """Manage workers"""

@command('elasticsearch')
def scrapers_elasticsearch():
    config = load_config()
    es = setup_elasticsearch(config)
    kwargs = {
        'config': config
    }
    BinoasUploader(**kwargs).run()


@command('locations')
def scrapers_locations():
    config = load_config()
    es = setup_elasticsearch(config)

    LocationsScraperRunner().run()


@command('openspendingdoc')
@click.option('-d', '--document-id')
@click.option('--verbose', '-v', is_flag=True, default=False, help="More.")
def scrapers_openspendingdoc(document_id, verbose):
    config = load_config()
    es = setup_elasticsearch(config)
    kwargs = {
        'config': config,
        'document_id': document_id,
        'verbose': verbose
    }
    OpenSpendingDocumentScraperRunner().run(**kwargs)


@command('openspending')
@click.option('-f', '--date-from', default=(date.today() - timedelta(days=1)))
@click.option('-t', '--date-to', default=datetime.now())
def scrapers_openspending(date_from, date_to):
    config = load_config()
    es = setup_elasticsearch(config)
    try:
        df = date_from.isoformat()
    except AttributeError as e:
        df = str(date_from)
    try:
        dt = date_to.isoformat()
    except AttributeError as e:
        dt = str(date_to)
    kwargs = {
        'config': config,
        'date_from': df,
        'date_to': dt
    }
    OpenSpendingScraperRunner().run(**kwargs)

@command('openspendingcache')
@click.option('-f', '--date-from', default=(date.today() - timedelta(days=1)))
@click.option('-t', '--date-to', default=datetime.now())
@click.option('-y', '--year', default=None)
@click.option('-p', '--period', default='0')
def scrapers_openspendingcache(date_from, date_to, year, period):
    config = load_config()
    es = setup_elasticsearch(config)
    try:
        df = date_from.isoformat()
    except AttributeError as e:
        df = str(date_from)
    try:
        dt = date_to.isoformat()
    except AttributeError as e:
        dt = str(date_to)
    # year takes precendence
    if year is not None:
        df = None
        dt = None
    kwargs = {
        'config': config,
        'date_from': df,
        'date_to': dt,
        'year': year,
        'period': period
    }
    OpenSpendingCacheScraperRunner().run(**kwargs)


@command('compare')
@click.option('-p', '--path', default='./2021-2022-comparison')
@click.option('-t', '--templates', default='./2021-2022-templates')
@click.option('-o', '--output', default='./2021-2022-articles')
@click.option('-y1', '--year1', default='2021')
@click.option('-p1', '--period1', default='5')
@click.option('-y2', '--year2', default='2022')
@click.option('-p2', '--period2', default='0')
def openspending_openspendingcompare(path, templates, output, year1, period1, year2, period2):
    config = load_config()
    kwargs = {
        'config': config,
        'path': path,
        'templates': templates,
        'output': output,
        'year1': year1,
        'period1': period1,
        'year2': year2,
        'period2': period2
    }
    openspending_compare_run(kwargs)


@command('poliflw')
@click.option('-f', '--date-from', default=(datetime.now() - timedelta(minutes=360)))
@click.option('-t', '--date-to', default=datetime.now())
@click.option('-s', '--scroll', default=None)
def scrapers_poliflw(date_from, date_to, scroll):
    config = load_config()
    es = setup_elasticsearch(config)
    try:
        df = date_from.isoformat()
    except AttributeError as e:
        df = str(date_from)
    try:
        dt = date_to.isoformat()
    except AttributeError as e:
        dt = str(date_to)
    kwargs = {
        'config': config,
        'date_from': df,
        'date_to': dt,
        'scroll': scroll
    }
    PoliflwScraperRunner().run(**kwargs)


@command('obv')
@click.option('-f', '--date-from', default=(datetime.now() - timedelta(minutes=360)))
@click.option('-t', '--date-to', default=datetime.now() + timedelta(days=7))
@click.option('-s', '--scroll', default=None)
@click.option('-o', '--organizations', default=None)
def scrapers_obv(date_from, date_to, scroll, organizations):
    config = load_config()
    es = setup_elasticsearch(config)
    try:
        df = date_from.isoformat()
    except AttributeError as e:
        df = str(date_from)
    try:
        dt = date_to.isoformat()
    except AttributeError as e:
        dt = str(date_to)
    kwargs = {
        'config': config,
        'date_from': df,
        'date_to': dt,
        'scroll': scroll,
        'organizations': organizations
    }
    OpenbesluitvormingScraperRunner().run(**kwargs)


@command('obv-counts')
@click.option('-f', '--date-from', default=(datetime.now() - timedelta(days=1)))
@click.option('-t', '--date-to', default=datetime.now())
@click.option('-T', '--threshold', default=1000)
@click.option('-o', '--organizations', default=None)
def scrapers_obv_counts(date_from, date_to, threshold, organizations):
    config = load_config()
    es = setup_elasticsearch(config)
    try:
        df = date_from.isoformat()
    except AttributeError as e:
        df = str(date_from)
    try:
        dt = date_to.isoformat()
    except AttributeError as e:
        dt = str(date_to)
    kwargs = {
        'config': config,
        'date_from': df,
        'date_to': dt,
        'threshold': threshold,
        'organizations': organizations
    }
    OpenbesluitvormingCountsScraperRunner().run(**kwargs)


@command('cvdr')
@click.option('-f', '--date-from', default=(datetime.now() - timedelta(days=1)))
@click.option('-t', '--date-to', default=datetime.now())
@click.option('-w', '--date-field', default='dates')  # created_at, updated_at, dates
def scrapers_cvdr(date_from, date_to, date_field):
    config = load_config()
    es = setup_elasticsearch(config)
    try:
        df = date_from.isoformat()[0:19]
    except AttributeError as e:
        df = str(date_from)
    try:
        dt = date_to.isoformat()[0:19]
    except AttributeError as e:
        dt = str(date_to)
    kwargs = {
        'config': config,
        'date_from': df,
        'date_to': dt,
        'date_field': date_field
    }
    CVDRScraperRunner().run(**kwargs)

@command('woo')
@click.option('-f', '--date-from', default=(datetime.now() - timedelta(days=1)))
@click.option('-t', '--date-to', default=datetime.now())
def scrapers_woo(date_from, date_to):
    config = load_config()
    run(config)

@command('put_templates')
@click.option('--template_dir', default='./mappings/', help='Path to JSON file containing the template.')
def es_put_template(template_dir):
    """
    Put a template into Elasticsearch. A template contains settings and mappings
    that should be applied to multiple indices. Check ``mappings/template.json``
    for an example.
    :param template_file: Path to JSON file containing the template. Defaults to ``mappings/template.json``.
    """

    config = load_config()
    es = setup_elasticsearch(config)

    click.echo('Putting ES template from dir: %s' % template_dir)

    for template_path in glob.glob(os.path.join(template_dir, 'es-*.json')):
        click.echo(template_path)
        template = {}
        with open(template_path, 'rb') as template_file:
            template = json.load(template_file)
        template_name = os.path.basename(template_file.name.replace('es-','').replace('.json', ''))
        es.indices.put_template(template_name, template)
        index_name = 'jodal_%s' % (template_name)
        if not es.indices.exists(index=index_name):
            click.echo("Should make index %s" % (index_name,))
            es.indices.create(index=index_name)

@command('reindex')
@click.option('--source', default='jodal_documents', help='Source index')
@click.option('--target', default='jodal_copy_documents', help='Target index')
def es_reindex(source, target):
    config = load_config()
    es = setup_elasticsearch(config)

    click.echo('Copying ES template %s to %s' % (source, target,))
    reindex(es, source, target)

@command('run')
@click.option('--host', default='redis', help='Redis host')
@click.option('--port', default=6379, help='Redis port')
def worker_run(host, port):
    config = load_config()
    redis_conn = setup_redis(config)
    # Tell rq what Redis connection to use
    with Connection(redis_conn):
        q = Queue()
        Worker(q).work()

# Register commands explicitly with groups, so we can easily use the docstring
# wrapper
elasticsearch.add_command(es_put_template)
elasticsearch.add_command(es_reindex)

openspending.add_command(openspending_openspendingcompare)

scrapers.add_command(scrapers_locations)
scrapers.add_command(scrapers_openspending)
scrapers.add_command(scrapers_openspendingdoc)
scrapers.add_command(scrapers_openspendingcache)
scrapers.add_command(scrapers_poliflw)
scrapers.add_command(scrapers_obv)
scrapers.add_command(scrapers_obv_counts)
scrapers.add_command(scrapers_cvdr)
scrapers.add_command(scrapers_elasticsearch)
scrapers.add_command(scrapers_woo)

worker.add_command(worker_run)

if __name__ == '__main__':
    cli()
