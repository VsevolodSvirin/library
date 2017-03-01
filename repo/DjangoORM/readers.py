import uuid

from django.db import IntegrityError

from Django.readers.models import Reader
from domains.reader import Reader as DomainReader
from shared import errors


class DjangoORMReaderRepository:
    @classmethod
    def _convert_to_domain(cls, reader):
        domain_book = DomainReader.from_dict({
            'code': reader.code,
            'full_name': reader.full_name,
            'reg_date': reader.reg_date
        })
        return domain_book

    @classmethod
    def create(cls, **kwargs):
        reader = Reader.objects.create(**kwargs)
        return reader

    @classmethod
    def from_dict(cls, adict):
        while True:
            try:
                code = str(uuid.uuid4())
                reader = cls.create(code=code, **adict)
                break
            except IntegrityError as e:
                if 'unique constraint' in e.message and 'code' in e.message:
                    pass
                raise
        return reader

    @classmethod
    def list(cls, filters=None):
        if filters is None:
            readers = Reader.objects.all()
        else:
            filters = {key.replace('__eq', ''): value for key, value in filters.items()}
            readers = Reader.objects.filter(**filters)

        return [cls._convert_to_domain(reader) for reader in readers]

    @classmethod
    def details(cls, pk):
        try:
            reader = Reader.objects.get(pk=pk)
            return cls._convert_to_domain(reader)
        except Exception:
            error = errors.Error.build_resource_error()
            return error

    @classmethod
    def delete(cls, pk):
        try:
            Reader.objects.get(pk=pk).delete()
            return
        except Exception:
            error = errors.Error.build_resource_error()
            return error

    @classmethod
    def update(cls, pk, patch):
        try:
            Reader.objects.filter(pk=pk).update(**patch)
            book = Reader.objects.get(pk=pk)
            return cls._convert_to_domain(book)
        except Exception:
            error = errors.Error.build_resource_error()
            return error
