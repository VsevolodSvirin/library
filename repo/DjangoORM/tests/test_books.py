from unittest.mock import patch

from django.db import IntegrityError
from django.test import TestCase

from Django.books.models import Book
from domains.book import Book as DomainBook
from repo.DjangoORM.books import DjangoORMBookRepository
from shared import errors


class TestException(Exception):
    pass


class BookAddRepositoryTestCase(TestCase):
    def test_book_creation(self):
        adict = {'title': '1984', 'author': 'George Orwell', 'year': 1984, 'language': 'English'}
        orm_book = DjangoORMBookRepository.from_dict(adict)

        assert type(orm_book) == Book
        assert hasattr(orm_book, 'code')
        assert (orm_book.title == adict['title'])
        assert (orm_book.author == adict['author'])
        assert (orm_book.year == adict['year'])
        assert (orm_book.language == adict['language'])

    def test_duplicate_code_exception(self):
        adict = {'title': '1984', 'author': 'George Orwell', 'year': 1984, 'language': 'English'}

        first_book = DjangoORMBookRepository.from_dict(adict)
        second_book = DjangoORMBookRepository.from_dict(adict)

        self.assertNotEqual(first_book.code, second_book.code)
        self.assertNotEqual(first_book.pk, second_book.pk)

    @patch('repo.DjangoORM.books.Book')
    def test_book_creation_reraises_orm_exceptions(self, mocked_book):
        mocked_book.objects.create.side_effect = TestException('Something went wrong...')

        adict = {'title': '1984', 'author': 'George Orwell', 'year': 1984, 'language': 'English'}

        self.assertRaises(TestException, DjangoORMBookRepository.from_dict, adict)

    def test_raises_exception_with_same_codes(self):
        code = 'r2rwr3re-bdfc-e2ww-5644-hd94id04kd9r'
        is_available = True
        adict = {'code': code, 'title': '1984', 'author': 'George Orwell', 'year': 1984, 'language': 'English',
                 'is_available': is_available}

        first_book = DjangoORMBookRepository.create(**adict)

        self.assertRaises(IntegrityError, DjangoORMBookRepository.create, **adict)


class BookListRepositoryTestCase(TestCase):
    def setUp(self):
        self.repo = DjangoORMBookRepository()
        self.repo.create(code='f853578c-fc0f-4e65-81b8-566c5dffa35a', title='1984',
                         author='George Orwell', year=1984, language='English', is_available=True, reader=None)
        self.repo.create(code='fe2c3195-aeff-487a-a08f-e0bdc0ec6e9a', title='The Lord of the Rings',
                         author='J.R.R. Tolkien', year=2000, language='English', is_available=False, reader=None)
        self.repo.create(code='913694c6-435a-4366-ba0d-da5334a611b2', title='The Master and Margarita',
                         author='Mikhail Bulgakov', year=2005, language='Russian', is_available=False, reader=None)
        self.repo.create(code='eed76e77-55c1-41ce-985d-ca49bf6c0585', title='The Dark Tower',
                         author='Stephen King', year=2015, language='English', is_available=True, reader=None)

        self.expected_result = [
            DomainBook(code='f853578c-fc0f-4e65-81b8-566c5dffa35a', title='1984',
                       author='George Orwell', year=1984, language='English', is_available=True, reader=None),
            DomainBook(code='fe2c3195-aeff-487a-a08f-e0bdc0ec6e9a', title='The Lord of the Rings',
                       author='J.R.R. Tolkien', year=2000, language='English', is_available=False, reader=None),
            DomainBook(code='913694c6-435a-4366-ba0d-da5334a611b2', title='The Master and Margarita',
                       author='Mikhail Bulgakov', year=2005, language='Russian', is_available=False, reader=None),
            DomainBook(code='eed76e77-55c1-41ce-985d-ca49bf6c0585', title='The Dark Tower',
                       author='Stephen King', year=2015, language='English', is_available=True, reader=None)
        ]

    def test_book_list(self):
        self.assertEqual(self.repo.list(), self.expected_result)

    def test_repository_list_with_filters_year(self):
        self.assertEqual(self.repo.list(filters={'year': 2000}), [self.expected_result[1]])
        self.assertEqual(self.repo.list(filters={'year__lt': 2000}), [self.expected_result[0]])
        self.assertEqual(self.repo.list(filters={'year__gt': 2000}), [self.expected_result[2], self.expected_result[3]])

    def test_repository_list_with_filters_title(self):
        self.assertEqual(self.repo.list(filters={'title': '1984'}), [self.expected_result[0]])


class BookDetailsRepositoryTestCase(TestCase):
    def setUp(self):
        self.repo = DjangoORMBookRepository()
        self.repo.create(code='f853578c-fc0f-4e65-81b8-566c5dffa35a', title='1984',
                         author='George Orwell', year=1984, language='English', is_available=True, reader=None)

        self.expected_book = \
            DomainBook(code='f853578c-fc0f-4e65-81b8-566c5dffa35a', title='1984',
                       author='George Orwell', year=1984, language='English', is_available=True, reader=None)

    def test_book_details(self):
        self.assertEqual(self.repo.details(pk=1), self.expected_book)

    def test_book_details_with_bad_pk(self):
        error = self.repo.details({'pk': 10**10})
        self.assertEqual(error.message, errors.Error.build_resource_error().message)
