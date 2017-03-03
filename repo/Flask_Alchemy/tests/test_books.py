from flask_testing import TestCase

from flask_interface.library.books.models import Book
from flask_interface.library.app import create_app
from flask_interface.manage import db

from domains.book import Book as DomainBook
from repo.Flask_Alchemy.books import FlaskAlchemyBookRepository
from shared import errors


class BookTestCase(TestCase):
    def create_app(self):
        self.repo = FlaskAlchemyBookRepository()
        return create_app(db)

    def setUp(self):
        db.create_all()
        db.session.add(Book(code='f853578c-fc0f-4e65-81b8-566c5dffa35a', title='1984',
                            author='George Orwell', year=1984, language='English', is_available=True,reader=None))
        db.session.add(Book(code='fe2c3195-aeff-487a-a08f-e0bdc0ec6e9a', title='The Lord of the Rings',
                            author='J.R.R. Tolkien', year=2000, language='English', is_available=False, reader=None))
        db.session.add(Book(code='913694c6-435a-4366-ba0d-da5334a611b2', title='The Master and Margarita',
                            author='Mikhail Bulgakov', year=2005, language='Russian', is_available=False, reader=None))
        db.session.add(Book(code='eed76e77-55c1-41ce-985d-ca49bf6c0585', title='The Dark Tower',
                            author='Stephen King', year=2015, language='English', is_available=True, reader=None))
        db.session.commit()

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

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_book_list(self):
        assert self.repo.list() == self.expected_result

    def test_repository_list_with_filters_year(self):
        assert self.repo.list(filters={'year': 2000}) == [self.expected_result[1]]
        assert self.repo.list(filters={'year__lt': 2000}) == [self.expected_result[0]]
        assert self.repo.list(filters={'year__gt': 2000}) == [self.expected_result[2], self.expected_result[3]]

    def test_repository_list_with_filters_title(self):
        assert self.repo.list(filters={'title': '1984'}) == [self.expected_result[0]]

    def test_book_details(self):
        self.assertEqual(self.repo.details(id=1), self.expected_result[0])

    def test_book_details_with_bad_pk(self):
        error = self.repo.details(id=10 ** 10)
        self.assertEqual(error.message, errors.Error.build_resource_error().message)
