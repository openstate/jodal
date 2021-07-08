from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

import re

import bleach
from bleach.sanitizer import Cleaner
from html5lib.filters.base import Filter

from .exceptions import ConfigurationError


def html2text(s):
    ATTRS = {}
    TAGS = []
    cleaner = Cleaner(
        tags=TAGS, attributes=ATTRS, filters=[Filter], strip=True)
    try:
        return cleaner.clean(s).replace('&amp;nbsp;', '')
    except TypeError:
        return u''


def load_config(config_file='config.yaml'):
    """
    Loads a configuration file (which is a YAML file). The location iof the
    file can be specified using the parameter. It further checks if it is a
    valid configuration file and if so, returns the parsed data strcture.
    """
    config = {}
    with open(config_file) as f:
        config = load(f, Loader=Loader)

    if not is_valid_config(config):
        raise ConfigurationError('Not a valid configuration file: %s' % (config,))

    return config


def is_valid_config(config):
    """
    Checks if a data structure can be considered as a valid binoas
    configuration file. Returns true or false.
    """
    return (len(config.keys()) == 1)
