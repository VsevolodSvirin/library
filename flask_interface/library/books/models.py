import datetime

from repo.Flask_Alchemy.database import db


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(128), unique=True)
    title = db.Column(db.String(128))
    author = db.Column(db.String(128))
    year = db.Column(db.Integer)
    language = db.Column(db.String(64))
    is_available = db.Column(db.Boolean, default=True)
    reader = db.Column(db.Integer, db.ForeignKey('reader.id'), default=None, nullable=True)


class Reader(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(128), unique=True)
    full_name = db.Column(db.String(128))
    reg_date = db.Column(db.Date, default=datetime.date.today)
