import re

from marshmallow import fields, ValidationError

from app import ma
from app.models import Column




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

class ColumnSchema(ma.Schema):
    class Meta:
        fields = (
            "id", "user_id", "name", "locations", "user_query", "order",
            "src_poliflw", "src_openspending", "src_openbesluitvorming")
        model = Column
    locations = LocationsField()  # fields.Str()

column_schema = ColumnSchema()
columns_schema = ColumnSchema(many=True)
