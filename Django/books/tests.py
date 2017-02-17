import json
import uuid
from unittest.mock import patch

from django.test import Client
from django.test import TestCase
from Django.books.forms import NewBookForm
import shared.response_object as ro
from domains.book import Book
from serializers import books
from shared.request_object import InvalidRequestObject


class BookFormTestCase(TestCase):
    def test_form_accept_valid_data(self):
        code = uuid.uuid4()
        form_data = {
            'code': code,
            'title': '1984',
            'author': 'George Orwell',
            'year': 1984,
            'language': 'English',
            'is_available': True,
            'reader': None
        }
        form = NewBookForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_repulse_invalid_data(self):
        code = uuid.uuid4()
        form_data1 = {
            'code': code,
            'title': '1984',
            'author': 'George Orwell',
            'year': 'ololo',
            'language': 'English',
            'is_available': True,
            'reader': None
        }
        form = NewBookForm(data=form_data1)
        self.assertFalse(form.is_valid())

        form_data2 = {
            'code': code,
            'title': (1,),
            'author': True,
            'year': 1984,
            'language': 1984,
            'is_available': True,
            'reader': None
        }
        form = NewBookForm(data=form_data2)
        self.assertFalse(form.is_valid())


class BooksAddViewTestCase(TestCase):
    def setUp(self):
        self.c = Client()

    @patch('Django.books.views.BookAddUseCase')
    def test_with_good_arguments(self, mocked_use_case):
        book = Book.from_dict({
            'code': '3251a5bd-86be-428d-8ae9-6e51a8048c33',
            'title': '1984',
            'author': 'George Orwell',
            'year': 1984,
            'language': 'English',
            'is_available': True,
            'reader': None
        })

        mocked_use_case().execute.return_value = ro.ResponseSuccess(book)

        # response = mocked_use_case.execute.return_value
        response = self.c.post('/books/', book.__dict__)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(json.dumps(book, cls=books.BookEncoder)), json.loads(response.content))

    @patch('Django.books.views.BookAddUseCase')
    def test_with_bad_arguments(self, mocked_use_case):
        invalid_request = InvalidRequestObject()
        invalid_request.add_error('year', 'invalid year')
        invalid_request.add_error('title', 'invalid title')
        mocked_use_case().execute.return_value = ro.ResponseFailure.build_from_invalid_request_object(invalid_request)

        response = self.c.post('/books/', {})
        self.assertEqual(response.status_code, 400)

        response_error_data = {'type': ro.ResponseFailure.PARAMETERS_ERROR,
                               'message': [{'year': 'invalid year'}, {'title': 'invalid title'}]}
        self.assertEqual(json.loads(response.content), response_error_data)

    @patch('Django.books.views.BookAddUseCase')
    def test_with_resource_error(self, mocked_use_case):
        mocked_use_case().execute.return_value = ro.ResponseFailure.build_resource_error('page not found :(')

        response = self.c.post('/books/', {})
        self.assertEqual(response.status_code, 404)

    @patch('Django.books.views.BookAddUseCase')
    def test_with_system_error(self, mocked_use_case):
        mocked_use_case().execute.return_value = ro.ResponseFailure.build_system_error('database failure')

        response = self.c.post('/books/', {})
        self.assertEqual(response.status_code, 500)
