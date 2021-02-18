from app import app, db

from jodal.db import BinaryUUID


class Column(db.Model):
    __tablename__ = 'column'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(100), nullable=False)
    user_query = db.Column('query', db.String(100))
    user_id = db.Column('user_id', BinaryUUID())
