import re

import json

from marshmallow import fields, ValidationError

from app import ma
from app.models import Column, ColumnSource, Asset




class LocationsField(fields.Field):
    """Field that serializes to a string of numbers and deserializes
    to a list of numbers.
    """

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return []
        return re.split('\s*,\s*', value)

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return ",".join(value)
        except ValueError as error:
            raise ValidationError("-") from error

class ReadCountsField(fields.Field):
    """Field that serializes to a json and deserializes
    to a string
    """

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return {}
        return json.loads(value)

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return json.dumps(value)
        except ValueError as error:
            raise ValidationError("-") from error

class ColumnSourceSchema(ma.Schema):
    class Meta:
        fields = (
            "id", "column_id", "source", "enabled")
        model = ColumnSource


class ColumnSchema(ma.Schema):
    class Meta:
        fields = (
            "id", "user_id", "name", "locations", "user_query", "order",
            "src_poliflw", "src_openspending", "src_openbesluitvorming",
            "src_cvdr", "sort", "sort_order", "date_start",  "date_end",
            "read_counts")
        model = Column
    read_counts = ReadCountsField()
    locations = LocationsField()  # fields.Str()
    date_start = fields.DateTime(allow_none=True, default=None)
    date_end = fields.DateTime(allow_none=True, default=None)

class AssetSchema(ma.Schema):
    class Meta:
        fields = ("id", "user_id", "url", "created", "modified", "last_run")
        model = Asset
    date_start = fields.DateTime(allow_none=True, default=None)
    date_end = fields.DateTime(allow_none=True, default=None)


column_schema = ColumnSchema()
columns_schema = ColumnSchema(many=True)
column_source_schema = ColumnSourceSchema()
column_sources_schema = ColumnSourceSchema(many=True)
asset_schema = AssetSchema()
assets_schema = AssetSchema(many=True)
