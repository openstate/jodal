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
    src_poliflw = db.Column('src_poliflw', db.Boolean, default=True)
    src_openspending = db.Column('src_openspending', db.Boolean, default=True)
    src_openbesluitvorming = db.Column('src_openbesluitvorming', db.Boolean, default=True)
    sort = db.Column('sort', db.String(16), default='published', nullable=False)
    sort_order = db.Column('sort_order', db.String(4), default='desc', nullable=False)
    date_start = db.Column('date_start', db.DateTime, nullable=True)
    date_end = db.Column('date_end', db.DateTime, nullable=True)
