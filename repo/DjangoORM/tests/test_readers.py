import datetime
from unittest.mock import patch

from django.db import IntegrityError
from django.test import TestCase

from Django.books.models import Reader
from domains.reader import Reader as DomainReader
from repo.DjangoORM.readers import DjangoORMReaderRepository


class TestException(Exception):
    pass


class ReaderRepositoryTestCase(TestCase):
    def test_reader_creation(self):
        adict = {'full_name': 'VS', 'reg_date': datetime.date.today()}
        orm_reader = DjangoORMReaderRepository.from_dict(adict)

        assert type(orm_reader) == Reader
        assert hasattr(orm_reader, 'code')
        assert (orm_reader.full_name == adict['full_name'])

    def test_duplicate_code_exception(self):
        adict = {'full_name': 'VS', 'reg_date': datetime.date.today()}

        first_reader = DjangoORMReaderRepository.from_dict(adict)
        second_reader = DjangoORMReaderRepository.from_dict(adict)

        self.assertNotEqual(first_reader.code, second_reader.code)
        self.assertNotEqual(first_reader.pk, second_reader.pk)

    @patch('repo.DjangoORM.readers.Reader')
    def test_reader_creation_reraises_orm_exceptions(self, mocked_reader):
        mocked_reader.objects.create.side_effect = TestException('Something went wrong...')

        adict = {'full_name': 'VS', 'reg_date': datetime.date.today()}

        self.assertRaises(TestException, DjangoORMReaderRepository.from_dict, adict)

    def test_raises_exception_with_same_codes(self):
        code = 'r2rwr3re-bdfc-e2ww-5644-hd94id04kd9r'
        adict = {'code': code, 'full_name': 'VS'}

        first_book = DjangoORMReaderRepository.create(**adict)

        self.assertRaises(IntegrityError, DjangoORMReaderRepository.create, **adict)
