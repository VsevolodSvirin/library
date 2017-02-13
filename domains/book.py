from shared.domain_model import DomainModel


class Book(object):
    def __init__(self, code, title, author, year, language, is_available, reader):
        self.code = code
        self.title = title
        self.author = author
        self.year = year
        self.language = language
        self.is_available = is_available
        self.reader = reader


DomainModel.register(Book)
