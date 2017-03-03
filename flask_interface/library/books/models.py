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

    def __init__(self, code, title, author, year, language, is_available, reader):
        self.code = code
        self.title = title
        self.author = author
        self.year = year
        self.language = language
        self.is_available = is_available
        self.reader = reader


class Reader(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(128), unique=True)
    full_name = db.Column(db.String(128))
    reg_date = db.Column(db.Date, default=datetime.date.today)

    def __init__(self, code, full_name, reg_date):
        self.code = code
        self.full_name = full_name
        self.reg_date = reg_date
