import datetime
from unittest.mock import patch

from django.db import IntegrityError
from django.test import TestCase

from Django.readers.models import Reader
from domains.reader import Reader as DomainReader
from repo.DjangoORM.readers import DjangoORMReaderRepository
from shared import errors


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

        first_reader = DjangoORMReaderRepository.create(**adict)

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

    def test_reader_list(self):
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


class ReaderDetailsRepositoryTestCase(TestCase):
    def setUp(self):
        self.repo = DjangoORMReaderRepository()
        self.repo.create(code='f853578c-fc0f-4e65-81b8-566c5dffa35a',
                         full_name='VS', reg_date=datetime.date(2010, 1, 1))

        self.expected_reader = DomainReader(code='f853578c-fc0f-4e65-81b8-566c5dffa35a',
                                            full_name='VS', reg_date=datetime.date(2010, 1, 1))

    def test_reader_details(self):
        self.assertEqual(self.repo.details(pk=1), self.expected_reader)

    def test_reader_details_with_bad_pk(self):
        error = self.repo.details(pk=10 ** 10)
        self.assertEqual(error.message, errors.Error.build_resource_error().message)


class ReaderDeleteRepositoryTestCase(TestCase):
    def setUp(self):
        self.repo = DjangoORMReaderRepository()
        self.repo.create(code='f853578c-fc0f-4e65-81b8-566c5dffa35a',
                         full_name='VS', reg_date=datetime.date(2010, 1, 1))

    def test_reader_delete(self):
        self.assertEqual(self.repo.delete(pk=1), None)

    def test_reader_delete_with_bad_pk(self):
        error = self.repo.delete(pk=10 ** 10)
        self.assertEqual(error.message, errors.Error.build_resource_error().message)


class ReaderUpdateRepositoryTestCase(TestCase):
    def setUp(self):
        self.repo = DjangoORMReaderRepository()
        self.repo.create(code='f853578c-fc0f-4e65-81b8-566c5dffa35a',
                         full_name='VS', reg_date=datetime.date(2010, 1, 1))
        self.updated_book = DomainReader(code='f853578c-fc0f-4e65-81b8-566c5dffa35a',
                                         full_name='Vsevolod Svirin', reg_date=datetime.date(2010, 1, 1))

    def test_reader_update(self):
        self.assertEqual(self.repo.update(
            pk=1, patch={'full_name': 'Vsevolod Svirin'}), self.updated_book
        )

    def test_reader_update_with_bad_pk(self):
        error = self.repo.update(pk=10 ** 10, patch={'full_name': 'Vsevolod Svirin'})
        self.assertEqual(error.message, errors.Error.build_resource_error().message)
