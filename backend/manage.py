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

import click
from click.core import Command
from click.decorators import _make_command
from elasticsearch.exceptions import NotFoundError

from jodal.utils import load_config
from jodal.es import setup_elasticsearch
from jodal.locations import LocationsScraperRunner
from jodal.openspending import (
    OpenSpendingScraperRunner, OpenSpendingDocumentScraperRunner,
    OpenSpendingCacheScraperRunner)
from jodal.poliflw import PoliflwScraperRunner
from jodal.obv import OpenbesluitvormingScraperRunner

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
    """Jodal"""


@cli.group()
def elasticsearch():
    """Manage Elasticsearch"""


@cli.group()
def scrapers():
    """Manage scrapers"""


@command('locations')
def scrapers_locations():
    config = load_config()
    es = setup_elasticsearch(config)

    LocationsScraperRunner().run()


@command('openspendingdoc')
@click.option('-d', '--document-id')
def scrapers_openspendingdoc(document_id):
    config = load_config()
    es = setup_elasticsearch(config)
    kwargs = {
        'config': config,
        'document_id': document_id
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
def scrapers_openspendingcache(date_from, date_to):
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
    OpenSpendingCacheScraperRunner().run(**kwargs)


@command('poliflw')
@click.option('-f', '--date-from', default=(datetime.now() - timedelta(minutes=30)))
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
@click.option('-f', '--date-from', default=(datetime.now() - timedelta(minutes=30)))
@click.option('-t', '--date-to', default=datetime.now())
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


# Register commands explicitly with groups, so we can easily use the docstring
# wrapper
elasticsearch.add_command(es_put_template)
scrapers.add_command(scrapers_locations)
scrapers.add_command(scrapers_openspending)
scrapers.add_command(scrapers_openspendingdoc)
scrapers.add_command(scrapers_openspendingcache)
scrapers.add_command(scrapers_poliflw)
scrapers.add_command(scrapers_obv)

if __name__ == '__main__':
    cli()
