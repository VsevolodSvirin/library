import uuid

from django.db import IntegrityError

from Django.books.models import Book
from domains.book import Book as DomainBook


class DjangoORMBookRepository(object):
    def _convert_to_domain(self, book):
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
    def create(cls, **kwargs):
        book = Book.objects.create(**kwargs)
        return book

    @classmethod
    def from_dict(cls, adict):
        while True:
            try:
                code = uuid.uuid4()
                book = cls.create(code=code, is_available=True, **adict)
                break
            except IntegrityError as e:
                if 'unique constraint' in e.message and 'code' in e.message:
                    pass
                raise
        return book

    @classmethod
    def list(cls, filters=None):
        if not filters:
            books = Book.objects.all()
            domain_books = [cls._convert_to_domain(book) for book in books]
