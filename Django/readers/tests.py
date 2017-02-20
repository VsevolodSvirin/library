import json
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
        self.assertEqual(json.loads(json.dumps(reader, cls=readers.ReaderEncoder)), json.loads(response.content))

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
        self.assertEqual(json.loads(response.content), response_error_data)

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
