import uuid

from django.db import IntegrityError

from Django.books.models import Book
from domains.book import Book as DomainBook
from shared import errors
from shared.request_object import InvalidRequestObject


class DjangoORMBookRepository(object):
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
    def create(cls, **kwargs):
        book = Book.objects.create(**kwargs)
        return book

    @classmethod
    def from_dict(cls, adict):
        while True:
            try:
                code = str(uuid.uuid4())
                book = cls.create(code=code, is_available=True, **adict)
                break
            except IntegrityError as e:
                if 'unique constraint' in e.message and 'code' in e.message:
                    pass
                raise
        return book

    @classmethod
    def list(cls, filters=None):
        if filters is None:
            books = Book.objects.all()
        else:
            filters = {key.replace('__eq', ''): value for key, value in filters.items()}
            books = Book.objects.filter(**filters)

        return [cls._convert_to_domain(book) for book in books]

    @classmethod
    def details(cls, pk):
        try:
            book = Book.objects.get(pk=pk)
            return cls._convert_to_domain(book)
        except Exception:
            error = errors.Error.build_resource_error()
            return error

    @classmethod
    def delete(cls, pk):
        try:
            Book.objects.get(pk=pk).delete()
            return
        except Exception:
            error = errors.Error.build_resource_error()
            return error

    @classmethod
    def update(cls, pk, patch):
        try:
            Book.objects.filter(pk=pk).update(**patch)
            book = Book.objects.get(pk=pk)
            return cls._convert_to_domain(book)
        except Exception:
            error = errors.Error.build_resource_error()
            return error

    @classmethod
    def give(cls, pk, reader):
        try:
            if Book.objects.get(pk=pk).is_available:
                Book.objects.filter(pk=pk).update(is_available=False, reader=reader)
                book = Book.objects.get(pk=pk)
                return cls._convert_to_domain(book)
            else:
                inv_req = InvalidRequestObject()
                inv_req.add_error('primary key', 'this book is not available')
                error = errors.Error.build_from_invalid_request_object(inv_req)
                return error
        except Exception:
            error = errors.Error.build_resource_error()
            return error

    @classmethod
    def return_book(cls, pk):
        try:
            if not Book.objects.get(pk=pk).is_available:
                Book.objects.filter(pk=pk).update(is_available=True, reader=None)
                book = Book.objects.get(pk=pk)
                return cls._convert_to_domain(book)
            else:
                inv_req = InvalidRequestObject()
                inv_req.add_error('primary key', 'this book is in the library')
                error = errors.Error.build_from_invalid_request_object(inv_req)
                return error
        except Exception:
            error = errors.Error.build_resource_error()
            return error

    @classmethod
    def steal(cls, pk):
        try:
            Book.objects.filter(pk=pk).update(is_available=False, reader=None)
            book = Book.objects.get(pk=pk)
            return cls._convert_to_domain(book)
        except Exception:
            error = errors.Error.build_resource_error()
            return error
