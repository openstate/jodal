#!/usr/bin/env python
from copy import deepcopy
from datetime import datetime
import json
from glob import glob
import gzip
from hashlib import sha1
import os
import sys
import time
import logging
from time import sleep

import requests

import click
from click.core import Command
from click.decorators import _make_command
from elasticsearch.exceptions import NotFoundError

from jodal.utils import load_config
from jodal.es import setup_elasticsearch
from jodal.locations import LocationsScraperRunner

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
    LocationsScraperRunner().run()

@command('put_template')
@click.option('--template_file', default='mappings/template.json',
              type=click.File('rb'), help='Path to JSON file containing the template.')
def es_put_template(template_file):
    """
    Put a template into Elasticsearch. A template contains settings and mappings
    that should be applied to multiple indices. Check ``mappings/template.json``
    for an example.
    :param template_file: Path to JSON file containing the template. Defaults to ``mappings/template.json``.
    """

    config = load_config()
    es = setup_elasticsearch(config)

    click.echo('Putting ES template: %s' % template_file.name)

    template = json.load(template_file)
    template_file.close()

    #es.indices.put_template('jodal_template', template)



# Register commands explicitly with groups, so we can easily use the docstring
# wrapper
elasticsearch.add_command(es_put_template)
scrapers.add_command(scrapers_locations)

if __name__ == '__main__':
    cli()
