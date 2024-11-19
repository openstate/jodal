#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import json

from flask_restful import Api
from app.extensions import db, ma
from config import Config
from app.utils import AppError, load_config, load_object

import click
from flask import Flask

from app.routes.users import users_bp
from app.routes.search import search_bp
from app.routes.archive import archive_bp
from app.routes.subscriptions import subscriptions_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app_name = app.config['NAME_OF_APP']
    app.config[app_name] = load_config()[app_name]

    app.errorhandler(AppError)(AppError.serialize_error)

    db.init_app(app)
    ma.init_app(app)

    setup_es = load_object('%s.es.setup_elasticsearch' % (app_name,))
    setup_es(app.config)

    app.register_blueprint(users_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(archive_bp)
    app.register_blueprint(subscriptions_bp)

    return app

logging.basicConfig(
    format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
    level=logging.INFO)

app = create_app()

from app.fa import setup_fa

@app.cli.group("fusionauth")
def fusionauth():
    """Manage fusionauth"""

@fusionauth.command("list")
@click.argument("entity")
def list_entities(entity):
    fa = setup_fa()
    resp = fa.retrieve_application()
    if resp.was_successful():
        print(json.dumps(resp.success_response, indent=2))

if __name__ == "__main__":
    app.run(threaded=True)

# TODO: Remove resources in favour of regular Flask API routes

from app.resources import ColumnListResource, ColumnResource, AssetListResource, AssetResource

api = Api(app)
api.add_resource(ColumnListResource, '/columns')
api.add_resource(ColumnResource, '/columns/<int:column_id>')
api.add_resource(AssetListResource, '/assets')
api.add_resource(AssetResource, '/assets/<int:asset_id>')
