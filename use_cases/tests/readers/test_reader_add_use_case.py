from unittest import mock

import pytest

from domains.reader import Reader
from use_cases import readers
from use_cases.request_objects import readers as request_readers


@pytest.fixture
def adict():
    parameters = {'full_name': 'VS', 'reg_date': '2017-01-01'}
    return parameters


def test_reader_addition(adict):
    code = 'f853578c-fc0f-4e65-81b8-566c5dffa35a'
    reader = Reader(code=code, full_name=adict['full_name'], reg_date=adict['reg_date'])
    repo = mock.Mock()
    repo.create.return_value = reader

    reader_list_add_case = readers.ReaderAddUseCase(repo)
    request_object = request_readers.ReaderAddRequestObject.from_dict(adict)

    response_object = reader_list_add_case.execute(request_object)
    assert bool(response_object) is True

    repo.create.assert_called_with(reader=adict)
    assert response_object.value == reader
