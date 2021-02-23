from app import ma
from app.models import Column

class ColumnSchema(ma.Schema):
    class Meta:
        fields = ("id", "user_id", "name", "locations", "user_query")
        model = Column

column_schema = ColumnSchema()
columns_schema = ColumnSchema(many=True)
