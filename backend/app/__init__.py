#!/usr/bin/env python
# -*- coding: utf-8 -*-
import locale
import os
import logging
# from logging.handlers import SMTPHandler, RotatingFileHandler
from config import Config
from .utils import load_config

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api

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


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app_name = app.config['NAME_OF_APP']
    app.config[app_name] = load_config()[app_name]

    app.errorhandler(AppError)(AppError.serialize_error)

    def add_cors_headers(resp):
        # resp.headers['Access-Control-Allow-Origin'] = '*'
        # # See https://stackoverflow.com/questions/12630231/how-do-cors-and-access-control-allow-headers-work
        # resp.headers['Access-Control-Allow-Headers'] = 'origin, content-type, accept'
        return resp

    app.after_request(add_cors_headers)

    setup_es = load_object('%s.es.setup_elasticsearch' % (app_name,))
    setup_es(app.config)

    return app

logging.basicConfig(
    format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
    level=logging.INFO)


app = create_app()
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)


from app import routes
from app.resources import ColumnListResource

api.add_resource(ColumnListResource, '/columns')
