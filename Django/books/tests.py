import json
import uuid
from unittest import mock
from unittest.mock import patch

from django.test import Client
from django.test import TestCase
from django.urls import reverse

import shared.response_object as ro
from domains.book import Book
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

        response = self.c.post(reverse('books_list'), {})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(json.dumps(book, cls=books.BookEncoder)), json.loads(response.content))

    @patch('Django.books.views.BookAddUseCase')
    def test_with_bad_arguments(self, mocked_use_case):
        invalid_request = InvalidRequestObject()
        invalid_request.add_error('year', 'invalid year')
        invalid_request.add_error('title', 'invalid title')
        error = errors.Error.build_from_invalid_request_object(invalid_request)
        mocked_use_case().execute.return_value = ro.ResponseFailure.from_error(error)

        response = self.c.post(reverse('books_list'), {})
        self.assertEqual(response.status_code, 400)

        response_error_data = {'year': ['invalid year'], 'title': ['invalid title']}
        self.assertEqual(json.loads(response.content), response_error_data)

    @patch('Django.books.views.BookAddUseCase')
    def test_with_resource_error(self, mocked_use_case):
        error = errors.Error.build_resource_error()
        mocked_use_case().execute.return_value = ro.ResponseFailure.from_error(error)

        response = self.c.post(reverse('books_list'), {})
        self.assertEqual(response.status_code, 404)

    @patch('Django.books.views.BookAddUseCase')
    def test_with_system_error(self, mocked_use_case):
        error = errors.Error.build_system_error(Exception('database failure',))
        mocked_use_case().execute.return_value = ro.ResponseFailure.from_error(error)

        response = self.c.post(reverse('books_list'), {})
        self.assertEqual(response.status_code, 500)


class BookListViewTestCase(TestCase):
    def setUp(self):
        self.c = Client()

    @mock.patch('Django.books.views.BookListUseCase')
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
        self.assertEqual(json.loads(json.dumps(book, cls=books.BookEncoder)), json.loads(response.content))

    @patch('Django.books.views.BookListUseCase')
    def test_with_bad_arguments(self, mocked_use_case):
        invalid_request = InvalidRequestObject()
        invalid_request.add_error('filter', 'bad filter')
        error = errors.Error.build_from_invalid_request_object(invalid_request)
        mocked_use_case().execute.return_value = ro.ResponseFailure.from_error(error)

        response = self.c.get(reverse('books_list'), {})
        self.assertEqual(response.status_code, 400)

        response_error_data = {'filter': ['bad filter']}
        self.assertEqual(json.loads(response.content), response_error_data)

    @patch('Django.books.views.BookListUseCase')
    def test_with_resource_error(self, mocked_use_case):
        error = errors.Error.build_resource_error()
        mocked_use_case().execute.return_value = ro.ResponseFailure.from_error(error)

        response = self.c.get(reverse('books_list'), {})
        self.assertEqual(response.status_code, 404)

    @patch('Django.books.views.BookListUseCase')
    def test_get_failed_response(self, mock_use_case):
        error = errors.Error.build_system_error(Exception('database failure',))
        mock_use_case().execute.return_value = ro.ResponseFailure.from_error(error)

        response = self.c.get(reverse('books_list'), {})
        self.assertEqual(response.status_code, 500)
