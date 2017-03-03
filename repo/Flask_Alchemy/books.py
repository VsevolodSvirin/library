from flask_interface.library.books.models import Book
from domains.book import Book as DomainBook


class FlaskAlchemyBookRepository(object):
    @classmethod
    def _convert_to_domain(cls, book):
        domain_book = DomainBook.from_dict({
            'code': book.code,
            'title': book.title,
            'author': book.author,
            'year': book.year,
            'language': book.language,
            'is_available': book.is_available,
            'reader': book.reader
        })
        return domain_book

    @classmethod
    def list(cls, filters=None):
        if filters is None:
            books = Book.query.all()
        else:
            filters = {key.replace('__eq', ''): value for key, value in filters.items()}
            books = Book.query.filter(**filters)

        return [cls._convert_to_domain(book) for book in books]
