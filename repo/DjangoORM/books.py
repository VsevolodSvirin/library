import uuid

from django.db import IntegrityError

from Django.books.models import Book


class DjangoORMBookRepository(object):
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
