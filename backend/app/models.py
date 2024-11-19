from sqlalchemy.sql import func

from app.extensions import db

from jodal.db import BinaryUUID


class Column(db.Model):
    __tablename__ = 'column'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(100), nullable=False)
    locations = db.Column('locations', db.String(1024))
    user_query = db.Column('query', db.String(100))
    user_id = db.Column('user_id', BinaryUUID())
    read_counts = db.Column('read_counts', db.Text())
    order = db.Column('order', db.Integer, nullable=False, default=0)
    src_poliflw = db.Column('src_poliflw', db.Boolean, default=True)
    src_openspending = db.Column('src_openspending', db.Boolean, default=True)
    src_openbesluitvorming = db.Column('src_openbesluitvorming', db.Boolean, default=True)
    src_cvdr = db.Column('src_cvdr', db.Boolean, default=True)
    sort = db.Column('sort', db.String(16), default='published', nullable=False)
    sort_order = db.Column('sort_order', db.String(4), default='desc', nullable=False)
    date_start = db.Column('date_start', db.DateTime, nullable=True)
    date_end = db.Column('date_end', db.DateTime, nullable=True)


class ColumnSource(db.Model):
    __tablename__ = 'column_source'
    id = db.Column('id', db.Integer, primary_key=True)
    #column_id = db.Column('column_id', db.Integer, nullable=False)
    column_id = db.Column(db.Integer, db.ForeignKey("column.id"))
    column = db.relationship("Column", backref=db.backref("sources", lazy="dynamic"))
    source = db.Column('source', db.String(100), nullable=False)
    enabled = db.Column('enabled', db.Boolean, default=True)


class UserData(db.Model):
    __tablename__ = 'user_data'
    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', BinaryUUID())
    key = db.Column('key', db.String(100), nullable=False)
    value = db.Column('value', db.String(1024))

class Asset(db.Model):
    __tablename__ = 'asset'
    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', BinaryUUID())
    url = db.Column('url', db.String(1024))
    external_id = db.Column('external_id', db.String(100))
    created =  db.Column('created', db.DateTime(), server_default=func.now())
    modified = db.Column('modified', db.DateTime(), onupdate=func.now())
    last_run = db.Column('last_run', db.DateTime())
