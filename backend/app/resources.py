import logging
from functools import wraps

from flask import request, session
import flask_restful
from flask_restful import Resource

from app import db
from app.models import Column
from app.schemas import (column_schema, columns_schema)

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
            locations=request.json['locations'],
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

        editable = [
            'name', 'locations', 'user_query', 'order', 'src_poliflw',
            'src_openspending', 'src_openbesluitvorming']
        for f in editable:
            if f in request.json:
                setattr(column, f, request.json[f])

        db.session.commit()
        return column_schema.dump(column)

    def delete(self, column_id):
        user_id = session['user']['sub']
        column = Column.query.filter(Column.user_id==user_id, Column.id==column_id).first_or_404()
        db.session.delete(column)
        db.session.commit()
        return '', 204
