from shared.domain_model import DomainModel


class Book(object):
    __slots__ = ('code', 'title', 'author', 'year', 'language', 'is_available', 'reader', )

    def __init__(self, **kwargs):
        self.code = kwargs['code']
        self.title = kwargs['title']
        self.author = kwargs['author']
        self.year = kwargs['year']
        self.language = kwargs['language']
        self.is_available = kwargs['is_available']
        self.reader = kwargs['reader']

    @classmethod
    def from_dict(cls, adict):
        book = Book(
            code=adict['code'],
            title=adict['title'],
            author=adict['author'],
            year=adict['year'],
            language=adict['language'],
            is_available=adict['is_available'],
            reader=adict['reader']
        )

        return book

    def __eq__(self, other):
        return self.code == other.code and self.title == other.title and self.author == other.author \
               and self.year == other.year and self.language == other.language \
               and self.is_available == other.is_available and self.reader == other.reader

DomainModel.register(Book)
