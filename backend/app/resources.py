from flask import request
from flask_restful import Resource

from app import db
from app.models import Column
from app.schemas import (column_schema, columns_schema)


class ColumnListResource(Resource):
    def get(self):
        columns = Column.query.all()
        return columns_schema.dump(columns)

    def post(self):
        new_column = Column(
            name=request.json['name'],
            user_id=request.json['user_id'],
            user_query=request.json['user_query']
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

        if 'name' in request.json:
            column.name = request.json['name']
        if 'user_query' in request.json:
            column.user_query = request.json['user_query']

        db.session.commit()
        return column_schema.dump(column)

    def delete(self, column_id):
        column = Column.query.get_or_404(column_id)
        db.session.delete(column)
        db.session.commit()
        return '', 204
