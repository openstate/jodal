from app import app, db

from jodal.db import BinaryUUID


class Column(db.Model):
    __tablename__ = 'column'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(100), nullable=False)
    locations = db.Column('locations', db.String(1024))
    user_query = db.Column('query', db.String(100))
    user_id = db.Column('user_id', BinaryUUID())
    order = db.Column('order', db.Integer, nullable=False, default=0)
