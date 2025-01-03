import logging
from functools import wraps

from flask import request, session
import flask_restful
from flask_restful import Resource

from app.extensions import db
from app.models import Column, Asset, Feed
from app.schemas import (
    feed_schema, feeds_schema, column_schema, columns_schema, asset_schema, assets_schema)
from app.search import perform_query

from sqlalchemy import select

from nanoid import generate

NANOID_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # TODO: proper token check
        # TODO: check the jwt token that is sent along
        user_id = None
        try:
            user_id = session['user']['sub']
        except (LookupError, AttributeError) as e:
            pass

        if user_id:
            return func(*args, **kwargs)

        flask_restful.abort(401)
    return wrapper

class FeedResource(Resource):
    method_decorators = [authenticate]

    def get(self, feed_id):
        user_id = session['user']['sub']
        stmt = select(Feed).where(Feed.user_id==user_id, Feed.public_id==feed_id)
        feed = db.session.execute(stmt).scalar()
        return feed_schema.dump(feed)

    def post(self, feed_id):
        user_id = session['user']['sub']
        stmt = select(Feed).where(Feed.user_id==user_id, Feed.public_id==feed_id)
        feed = db.session.execute(stmt).scalar()
        updated_feed = feed_schema.load(request.json)
        editable = ['name', 'query', 'locations', 'sources']
        for f in editable:
            if f in request.json:
                setattr(feed, f, updated_feed[f])
        db.session.commit()
        return feed_schema.dump(feed)

    def delete(self, feed_id):
        user_id = session['user']['sub']
        stmt = select(Feed).where(Feed.user_id==user_id, Feed.public_id==feed_id)
        feed = db.session.execute(stmt).scalar()
        db.session.delete(feed)
        db.session.commit()
        return '', 204

class FeedListResource(Resource):
    method_decorators = [authenticate]

    def get(self):
        user_id = session['user']['sub']
        stmt = select(Feed).where(Feed.user_id==user_id)
        feeds = db.session.execute(stmt).scalars().all()
        return feeds_schema.dump(feeds)

    def post(self):
        user_id = session['user']['sub']
        new_feed = Feed(
            public_id=generate(NANOID_ALPHABET, 12),
            user_id=user_id,
            name=request.json['name'],
            query=request.json['query'],
            locations=",".join(request.json['locations']),
            sources=",".join(request.json['sources'])
        )
        db.session.add(new_feed)
        db.session.commit()
        return feed_schema.dump(new_feed)

class ColumnListResource(Resource):
    method_decorators = [authenticate]

    def get(self):
        user_id = session['user']['sub']

        #columns = Column.query.all()
        columns = Column.query.filter(Column.user_id==user_id)

        return columns_schema.dump(columns)

    def post(self):
        user_id = session['user']['sub']
        new_column = Column(
            name=request.json['name'],
            user_id=user_id,
            locations=",".join(request.json['locations']),
            user_query=request.json['user_query'],
            order=request.json['order']
        )
        db.session.add(new_column)
        db.session.commit()
        return column_schema.dump(new_column)

class ColumnResource(Resource):
    method_decorators = [authenticate]

    def get(self, column_id):
        user_id = session['user']['sub']
        column = Column.query.filter(Column.user_id==user_id, Column.id==column_id).first_or_404()
        return column_schema.dump(column)

    def post(self, column_id):
        user_id = session['user']['sub']
        column = Column.query.filter(Column.user_id==user_id, Column.id==column_id).first_or_404()
        updated_column = column_schema.load(request.json)
        editable = [
            'name', 'locations', 'user_query', 'order', 'src_poliflw',
            'src_openspending', 'src_openbesluitvorming', 'src_cvdr', 'sort',
            'sort_order', 'date_start',  'date_end', 'read_counts']
        for f in editable:
            if f in request.json:
                setattr(column, f, updated_column[f])
        db.session.commit()
        return column_schema.dump(column)

    def delete(self, column_id):
        user_id = session['user']['sub']
        column = Column.query.filter(Column.user_id==user_id, Column.id==column_id).first_or_404()
        db.session.delete(column)
        db.session.commit()
        return '', 204

class AssetListResource(Resource):
    method_decorators = [authenticate]

    def get(self):
        user_id = session['user']['sub']

        #assets = Asset.query.all()
        assets = Asset.query.filter(
            Asset.user_id==user_id).order_by(Asset.created.desc())

        return assets_schema.dump(assets)

    def post(self):
        user_id = session['user']['sub']
        new_asset = Asset(
            user_id=user_id,
            url=request.json['url'],
            external_id=request.json['external_id']
        )
        db.session.add(new_asset)
        db.session.commit()
        return asset_schema.dump(new_asset)

class AssetResource(Resource):
    method_decorators = [authenticate]

    def get(self, asset_id):
        user_id = session['user']['sub']
        asset = Asset.query.filter(Asset.user_id==user_id, Asset.id==asset_id).first_or_404()
        return asset_schema.dump(asset)

    def post(self, asset_id):
        user_id = session['user']['sub']
        asset = Asset.query.filter(Asset.user_id==user_id, Asset.id==asset_id).first_or_404()
        updated_asset = asset_schema.load(request.json)
        editable = [
            'url', 'external_id', 'last_run', 'modified']
        for f in editable:
            if f in request.json:
                setattr(asset, f, updated_asset[f])
        db.session.commit()
        return asset_schema.dump(asset)

    def delete(self, asset_id):
        user_id = session['user']['sub']
        column = Asset.query.filter(Asset.user_id==user_id, Asset.id==asset_id).first_or_404()
        db.session.delete(asset)
        db.session.commit()
        return '', 204
