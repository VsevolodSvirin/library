from unittest.mock import patch

from django.db import IntegrityError
from django.test import TestCase

from Django.books.models import Book
from repo.DjangoORM.books import DjangoORMBookRepository


class TestException(Exception):
    pass


class BookRepositoryTestCase(TestCase):
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
