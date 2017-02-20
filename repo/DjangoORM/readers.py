import uuid

from django.db import IntegrityError

from Django.readers.models import Reader


class DjangoORMReaderRepository:
    @classmethod
    def create(cls, **kwargs):
        reader = Reader.objects.create(**kwargs)
        return reader

    @classmethod
    def from_dict(cls, adict):
        while True:
            try:
                code = uuid.uuid4()
                reader = cls.create(code=code, **adict)
                break
            except IntegrityError as e:
                if 'unique constraint' in e.message and 'code' in e.message:
                    pass
                raise
        return reader
