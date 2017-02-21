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


class ReaderListRepositoryTestCase(TestCase):
    def setUp(self):
        self.repo = DjangoORMReaderRepository()
        self.repo.create(code='f853578c-fc0f-4e65-81b8-566c5dffa35a',
                         full_name='VS', reg_date=datetime.date(2010, 1, 1))
        self.repo.create(code='fe2c3195-aeff-487a-a08f-e0bdc0ec6e9a',
                         full_name='John', reg_date=datetime.date(2010, 1, 1))
        self.repo.create(code='913694c6-435a-4366-ba0d-da5334a611b2',
                         full_name='Sansa', reg_date=datetime.date(2012, 1, 1))
        self.repo.create(code='eed76e77-55c1-41ce-985d-ca49bf6c0585',
                         full_name='Arya', reg_date=datetime.date(2014, 1, 1))

        self.expected_result = [
            DomainReader(code='f853578c-fc0f-4e65-81b8-566c5dffa35a',
                         full_name='VS', reg_date=datetime.date(2010, 1, 1)),
            DomainReader(code='fe2c3195-aeff-487a-a08f-e0bdc0ec6e9a',
                         full_name='John', reg_date=datetime.date(2010, 1, 1)),
            DomainReader(code='913694c6-435a-4366-ba0d-da5334a611b2',
                         full_name='Sansa', reg_date=datetime.date(2012, 1, 1)),
            DomainReader(code='eed76e77-55c1-41ce-985d-ca49bf6c0585',
                         full_name='Arya', reg_date=datetime.date(2014, 1, 1))
        ]

    def test_book_list(self):
        self.assertEqual(self.repo.list(), self.expected_result)

    def test_repository_list_with_filters_year(self):
        self.assertEqual(self.repo.list(
            filters={'reg_date': datetime.date(2010, 1, 1)}), [self.expected_result[0], self.expected_result[1]])
        self.assertEqual(self.repo.list(
            filters={'reg_date__lt': datetime.date(2010, 1, 1)}), [])
        self.assertEqual(self.repo.list(
            filters={'reg_date__gt': datetime.date(2010, 1, 1)}), [self.expected_result[2], self.expected_result[3]])

    def test_repository_list_with_filters_title(self):
        self.assertEqual(self.repo.list(filters={'full_name': 'VS'}), [self.expected_result[0]])