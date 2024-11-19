from functools import wraps
import json
from flask import jsonify, request, session
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

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

def load_object(path):
    """Load an object given it's absolute object path, and return it.
    The object can be a class, function, variable or instance.
    :param path: absolute object path (i.e. 'ocd_backend.extractor.BaseExtractor')
    :type path: str.
    """
    try:
        dot = path.rindex('.')
    except ValueError:
        raise ValueError("Error loading object '%s': not a full path" % path)

    module, name = path[:dot], path[dot+1:]
    try:
        mod = __import__(module, {}, {}, [''])
    except ImportError as e:
        raise ImportError("Error loading object '%s': %s" % (path, e))

    try:
        obj = getattr(mod, name)
    except AttributeError:
        raise NameError("Module '%s' doesn't define any object named '%s'" % (module, name))

    return obj

def is_valid_config(config):
    """
    Checks if a data structure can be considered as a valid binoas
    configuration file. Returns true or false.
    """
    return (len(config.keys()) == 1)

def ensure_authenticated(fn):
    """"Decorator thst cheks if user is logged in"""
    @wraps(fn)
    def wrapped_function(*args, **kwargs):
        if session.get('user') != None:
            user = session['user']
        else:
            user = None
        if user is None:
            raise AppError('Not logged in', 403)
        return fn(*args, **kwargs)

    return wrapped_function

def decode_json_post_data(fn):
    """Decorator that parses POSTed JSON and attaches it to the request
    object (:obj:`request.data`)."""

    @wraps(fn)
    def wrapped_function(*args, **kwargs):
        if request.method in ['POST', 'DELETE']:
            data = request.get_data(cache=False)
            if not data:
                raise AppError('No data was POSTed', 400)

            try:
                request_charset = request.mimetype_params.get('charset')
                if request_charset is not None:
                    data = json.loads(data, encoding=request_charset)
                else:
                    data = json.loads(data)
            except:
                raise AppError('Unable to parse POSTed JSON', 400)

            request.data = data

        return fn(*args, **kwargs)

    return wrapped_function

class AppError(Exception):
    """API error class.
    :param msg: the message that should be returned to the API user.
    :param status_code: the HTTP status code of the response
    """

    def __init__(self, msg, status_code):
        self.msg = msg
        self.status_code = status_code

    def __str__(self):
        return repr(self.msg)

    @staticmethod
    def serialize_error(e):
        return jsonify(dict(status='error', error=e.msg)), e.status_code
