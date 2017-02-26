import datetime
import json
from unittest import mock
from unittest.mock import patch

from django.test import Client
from django.test import TestCase
from django.urls import reverse

import shared.response_object as ro
from domains.reader import Reader
from serializers import readers
from shared import errors
from shared.request_object import InvalidRequestObject


class ReadersAddViewTestCase(TestCase):
    def setUp(self):
        self.c = Client()

    @patch('Django.readers.views.ReaderAddUseCase')
    def test_with_good_arguments(self, mocked_use_case):
        reader = Reader.from_dict({
            'code': '3251a5bd-86be-428d-8ae9-6e51a8048c33',
            'full_name': 'VS',
            'reg_date': '2000-10-01'
        })

        mocked_use_case().execute.return_value = ro.ResponseSuccess(reader)

        response = self.c.post(reverse('readers_list'), {})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(json.dumps(reader, cls=readers.ReaderEncoder)),
                         json.loads(response.content.decode('utf-8')))

    @patch('Django.readers.views.ReaderAddUseCase')
    def test_with_bad_arguments(self, mocked_use_case):
        invalid_request = InvalidRequestObject()
        invalid_request.add_error('full_name', 'invalid name')
        invalid_request.add_error('reg_date', 'invalid date')
        error = errors.Error.build_from_invalid_request_object(invalid_request)
        mocked_use_case().execute.return_value = ro.ResponseFailure.from_error(error)

        response = self.c.post(reverse('readers_list'), {})
        self.assertEqual(response.status_code, 400)

        response_error_data = {'full_name': ['invalid name'], 'reg_date': ['invalid date']}
        self.assertEqual(json.loads(response.content.decode('utf-8')), response_error_data)

    @patch('Django.readers.views.ReaderAddUseCase')
    def test_with_resource_error(self, mocked_use_case):
        error = errors.Error.build_resource_error()
        mocked_use_case().execute.return_value = ro.ResponseFailure.from_error(error)

        response = self.c.post(reverse('readers_list'), {})
        self.assertEqual(response.status_code, 404)

    @patch('Django.readers.views.ReaderAddUseCase')
    def test_with_system_error(self, mocked_use_case):
        error = errors.Error.build_system_error(Exception('database failure',))
        mocked_use_case().execute.return_value = ro.ResponseFailure.from_error(error)

        response = self.c.post(reverse('readers_list'), {})
        self.assertEqual(response.status_code, 500)


class ReaderListViewTestCase(TestCase):
    def setUp(self):
        self.c = Client()

    @mock.patch('Django.readers.views.ReaderListUseCase')
    def test_repository_list_without_parameters(self, mocked_use_case):
        reader = Reader.from_dict({
            'code': '3251a5bd-86be-428d-8ae9-6e51a8048c33',
            'full_name': 'VS',
            'reg_date': datetime.date(2010, 1, 1)
        })

        mocked_use_case().execute.return_value = ro.ResponseSuccess(reader)
        response = self.c.get(reverse('readers_list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(json.dumps(reader, cls=readers.ReaderEncoder)),
                         json.loads(response.content.decode('utf-8')))

    @patch('Django.readers.views.ReaderListUseCase')
    def test_with_bad_arguments(self, mocked_use_case):
        invalid_request = InvalidRequestObject()
        invalid_request.add_error('filter', 'bad filter')
        error = errors.Error.build_from_invalid_request_object(invalid_request)
        mocked_use_case().execute.return_value = ro.ResponseFailure.from_error(error)

        response = self.c.get(reverse('readers_list'), {})
        self.assertEqual(response.status_code, 400)

        response_error_data = {'filter': ['bad filter']}
        self.assertEqual(json.loads(response.content.decode('utf-8')), response_error_data)

    @patch('Django.readers.views.ReaderListUseCase')
    def test_with_resource_error(self, mocked_use_case):
        error = errors.Error.build_resource_error()
        mocked_use_case().execute.return_value = ro.ResponseFailure.from_error(error)

        response = self.c.get(reverse('readers_list'), {})
        self.assertEqual(response.status_code, 404)

    @patch('Django.readers.views.ReaderListUseCase')
    def test_get_failed_response(self, mock_use_case):
        error = errors.Error.build_system_error(Exception('database failure',))
        mock_use_case().execute.return_value = ro.ResponseFailure.from_error(error)

        response = self.c.get(reverse('readers_list'), {})
        self.assertEqual(response.status_code, 500)

    @mock.patch('Django.readers.views.ReaderListUseCase')
    def test_request_object_initialisation_and_use_with_filters(self, mocked_use_case):
        mocked_use_case().execute.return_value = ro.ResponseSuccess()

        internal_request_object = mock.Mock()

        request_object_class = 'Django.readers.views.ReaderListRequestObject'
        with mock.patch(request_object_class) as mock_request_object:
            mock_request_object.from_dict.return_value = internal_request_object
            self.c.get('/readers?filter_param1=value1&filter_param2=value2')

        mock_request_object.from_dict.assert_called_with(
            {'filters': {'param1': 'value1', 'param2': 'value2'}}
        )
        mocked_use_case().execute.assert_called_with(internal_request_object)