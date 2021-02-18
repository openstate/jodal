from flask_restful import Resource

from app import db
from app.models import Column
from app.schemas import (column_schema, columns_schema)


class ColumnListResource(Resource):
    def get(self):
        columns = Column.query.all()
        return columns_schema.dump(columns)
