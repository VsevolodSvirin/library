import datetime
import json
from unittest import mock
from unittest.mock import patch

from django.test import Client
from django.test import TestCase

from django.urls import reverse

import shared.response_object as ro
from domains.book import Book
from domains.reader import Reader
from serializers import books
from shared import errors
from shared.request_object import InvalidRequestObject


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

        response = self.c.post(reverse('books_list'), {
            'code': '3251a5bd-86be-428d-8ae9-6e51a8048c33',
            'title': '1984',
            'author': 'George Orwell',
            'year': 1984,
            'language': 'English',
            'is_available': True,
            'reader': None
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(json.dumps(book, cls=books.BookEncoder)),
                         json.loads(response.content.decode('utf-8')))

    @patch('Django.books.views.BookAddUseCase')
    def test_with_bad_arguments(self, mocked_use_case):
        invalid_request = InvalidRequestObject()
        invalid_request.add_error('year', 'invalid year')
        invalid_request.add_error('title', 'invalid title')
        error = errors.Error.build_from_invalid_request_object(invalid_request)
        mocked_use_case().execute.return_value = ro.ResponseFailure.from_error(error)

        response = self.c.post(reverse('books_list'), error.value)
        self.assertEqual(response.status_code, 400)

        response_error_data = {'year': ['invalid year'], 'title': ['invalid title']}
        self.assertEqual(json.loads(response.content.decode('utf-8')), response_error_data)

    @patch('Django.books.views.BookAddUseCase')
    def test_with_resource_error(self, mocked_use_case):
        error = errors.Error.build_resource_error()
        mocked_use_case().execute.return_value = ro.ResponseFailure.from_error(error)

        response = self.c.post(reverse('books_list'), error.value)
        self.assertEqual(response.status_code, 404)

    @patch('Django.books.views.BookAddUseCase')
    def test_with_system_error(self, mocked_use_case):
        error = errors.Error.build_system_error(Exception('database failure', ))
        mocked_use_case().execute.return_value = ro.ResponseFailure.from_error(error)

        response = self.c.post(reverse('books_list'), error.value)
        self.assertEqual(response.status_code, 500)


class BookListViewTestCase(TestCase):
    def setUp(self):
        self.c = Client()

    @patch('Django.books.views.BookListUseCase')
    def test_repository_list_without_parameters(self, mocked_use_case):
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
        response = self.c.get(reverse('books_list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(json.dumps(book, cls=books.BookEncoder)),
                         json.loads(response.content.decode('utf-8')))

    @patch('Django.books.views.BookListUseCase')
    def test_with_bad_arguments(self, mocked_use_case):
        invalid_request = InvalidRequestObject()
        invalid_request.add_error('filter', 'bad filter')
        error = errors.Error.build_from_invalid_request_object(invalid_request)
        mocked_use_case().execute.return_value = ro.ResponseFailure.from_error(error)

        response = self.c.get(reverse('books_list'), {})
        self.assertEqual(response.status_code, 400)

        response_error_data = {'filter': ['bad filter']}
        self.assertEqual(json.loads(response.content.decode('utf-8')), response_error_data)

    @patch('Django.books.views.BookListUseCase')
    def test_with_resource_error(self, mocked_use_case):
        error = errors.Error.build_resource_error()
        mocked_use_case().execute.return_value = ro.ResponseFailure.from_error(error)

        response = self.c.get(reverse('books_list'), {})
        self.assertEqual(response.status_code, 404)

    @patch('Django.books.views.BookListUseCase')
    def test_get_failed_response(self, mock_use_case):
        error = errors.Error.build_system_error(Exception('database failure', ))
        mock_use_case().execute.return_value = ro.ResponseFailure.from_error(error)

        response = self.c.get(reverse('books_list'), {})
        self.assertEqual(response.status_code, 500)

    @patch('Django.books.views.BookListUseCase')
    def test_request_object_initialisation_and_use_with_filters(self, mocked_use_case):
        mocked_use_case().execute.return_value = ro.ResponseSuccess()

        internal_request_object = mock.Mock()

        request_object_class = 'Django.books.views.BookListRequestObject'
        with mock.patch(request_object_class) as mock_request_object:
            mock_request_object.from_dict.return_value = internal_request_object
            self.c.get('/books?filter_param1=value1&filter_param2=value2')

        mock_request_object.from_dict.assert_called_with(
            {'filters': {'param1': 'value1', 'param2': 'value2'}}
        )
        mocked_use_case().execute.assert_called_with(internal_request_object)


class BookDetailsViewTestCase(TestCase):
    def setUp(self):
        self.c = Client()

    @patch('Django.books.views.BookDetailsUseCase')
    def test_repository_details(self, mocked_use_case):
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
        response = self.c.get('/books/1/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(json.dumps(book, cls=books.BookEncoder)),
                         json.loads(response.content.decode('utf-8')))


class BookDeleteViewTestCase(TestCase):
    def setUp(self):
        self.c = Client()

    @patch('Django.books.views.BookDeleteUseCase')
    def test_repository_details(self, mocked_use_case):
        mocked_use_case().execute.return_value = ro.ResponseSuccess()
        response = self.c.delete('/books/1/')

        self.assertEqual(response.status_code, 204)
        self.assertEqual('', response.content.decode('utf-8'))


class BookUpdateViewTestCase(TestCase):
    def setUp(self):
        self.c = Client()

    @patch('Django.books.views.BookUpdateUseCase')
    def test_repository_update(self, mocked_use_case):
        updated_book = Book.from_dict({'code': '3251a5bd-86be-428d-8ae9-6e51a8048c33',
                                       'title': 'Fahrenheit 451',
                                       'author': 'Ray Bradbury',
                                       'year': 1984,
                                       'language': 'English',
                                       'is_available': True,
                                       'reader': None
                                       })

        mocked_use_case().execute.return_value = ro.ResponseSuccess(updated_book)
        response = self.c.patch(
            '/books/1/', {"title": "Fahrenheit 451", "author": "Ray Bradbury", 'action': 'update'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(json.dumps(updated_book, cls=books.BookEncoder)),
                         json.loads(response.content.decode('utf-8')))


class BookGiveViewTestCase(TestCase):
    def setUp(self):
        self.c = Client()

    @patch('Django.books.views.BookGiveUseCase')
    def test_repository_give(self, mocked_use_case):
        reader = Reader.from_dict({
            'code': 'r2rwr3re-bdfc-e2ww-5644-hd94id04kd9r',
            'full_name': 'John Smith',
            'reg_date': datetime.date(2017, 2, 13)
        })
        updated_book = Book.from_dict({'code': '3251a5bd-86be-428d-8ae9-6e51a8048c33',
                                       'title': 'Fahrenheit 451',
                                       'author': 'Ray Bradbury',
                                       'year': 1984,
                                       'language': 'English',
                                       'is_available': False,
                                       'reader': reader
                                       })

        mocked_use_case().execute.return_value = ro.ResponseSuccess(updated_book)
        response = self.c.patch('/books/1/', {"reader": reader, 'action': 'give'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(json.dumps(updated_book, cls=books.BookEncoder)),
                         json.loads(response.content.decode('utf-8')))


class BookReturnViewTestCase(TestCase):
    def setUp(self):
        self.c = Client()

    @patch('Django.books.views.BookReturnUseCase')
    def test_repository_return(self, mocked_use_case):
        updated_book = Book.from_dict({'code': '3251a5bd-86be-428d-8ae9-6e51a8048c33',
                                       'title': 'Fahrenheit 451',
                                       'author': 'Ray Bradbury',
                                       'year': 1984,
                                       'language': 'English',
                                       'is_available': True,
                                       'reader': None
                                       })

        mocked_use_case().execute.return_value = ro.ResponseSuccess(updated_book)
        response = self.c.patch('/books/1/', {"reader": None, 'action': 'take'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(json.dumps(updated_book, cls=books.BookEncoder)),
                         json.loads(response.content.decode('utf-8')))
