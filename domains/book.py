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

    @classmethod
    def from_dict(cls, adict):
        book = Book(
            code=adict["code"],
            title=adict["title"],
            author=adict["author"],
            year=adict["year"],
            language=adict["language"],
            is_available=adict["is_available"],
            reader=adict["reader"]
        )

        return book

    def __eq__(self, other):
        return self.code == other.code and self.title == other.title and self.author == other.author \
               and self.year == other.year and self.language == other.language \
               and self.is_available == other.is_available and self.reader == other.reader

DomainModel.register(Book)
