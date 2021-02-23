import logging

from flask import request, session
from flask_restful import Resource

from app import db
from app.models import Column
from app.schemas import (column_schema, columns_schema)


class ColumnListResource(Resource):
    def get(self):
        # TODO: proper token check
        # TODO: check the jwt token that is sent along
        if 'user' in session:
            user_id = session['user']['sub']
        else:
            user_id = None

        if user_id is None:
            return '', 401

        #columns = Column.query.all()
        columns = Column.query.filter(Column.user_id==user_id)

        return columns_schema.dump(columns)

    def post(self):
        # TODO: proper token check
        # TODO: check the jwt token that is sent along
        if 'user' in session:
            user_id = session['user']['sub']
        else:
            user_id = None

        if user_id is None:
            return '', 401

        logging.info(request.json)
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
    def get(self, column_id):
        column = Column.query.get_or_404(column_id)
        return column_schema.dump(column)

    def patch(self, column_id):
        column = Column.query.get_or_404(column_id)

        editable = ['name', 'locations', 'user_query', 'order']
        for f in editable:
            if f in request.json:
                setattr(column, f, request.json[f])

        db.session.commit()
        return column_schema.dump(column)

    def delete(self, column_id):
        column = Column.query.get_or_404(column_id)
        db.session.delete(column)
        db.session.commit()
        return '', 204
