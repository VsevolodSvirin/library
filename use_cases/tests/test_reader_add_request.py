import datetime

import pytest

from shared.request_object import InvalidRequestObject
from use_cases.request_objects import readers


@pytest.fixture
def dictionaries():
    dict1 = {}
    dict2 = {'full_name': True, 'reg_date': 'lulz'}
    dict3 = {'full_name': 'VS', 'reg_date': '2018-01-01'}
    dict4 = {'full_name': 'VS', 'reg_date': datetime.date(2017, 1, 1)}
    return [dict1, dict2, dict3, dict4]


def test_new_reader_validation(dictionaries):
    request_object = readers.ReaderAddRequestObject.from_dict(dictionaries[0])
    assert bool(request_object) is False

    request_object = readers.ReaderAddRequestObject.from_dict(dictionaries[1])
    assert bool(request_object) is False

    request_object = readers.ReaderAddRequestObject.from_dict(dictionaries[2])
    assert bool(request_object) is True

    request_object = readers.ReaderAddRequestObject.from_dict(dictionaries[3])
    assert bool(request_object) is True


def test_validation_error_messages(dictionaries):
    try:
        request_object_errors = readers.ReaderAddRequestObject.from_dict(dictionaries[0]).errors
    except AttributeError:
        request_object_errors = True
    assert bool(request_object_errors) is True
    invalid_request_object = InvalidRequestObject()
    invalid_request_object.add_error(parameter='full_name', message=['required key not provided'])
    invalid_request_object.add_error(parameter='reg_date', message=['required key not provided'])

    assert sorted(request_object_errors) == sorted(invalid_request_object.errors)

    try:
        request_object_errors = readers.ReaderAddRequestObject.from_dict(dictionaries[1]).errors
    except AttributeError:
        request_object_errors = True
    assert bool(request_object_errors) is True
    invalid_request_object = InvalidRequestObject()
    invalid_request_object.add_error(parameter='full_name', message=['expected str'])
    invalid_request_object.add_error(parameter='reg_date', message=['does not match regular expression'])

    assert sorted(request_object_errors) == sorted(invalid_request_object.errors)

    try:
        request_object_errors = readers.ReaderAddRequestObject.from_dict(dictionaries[2]).errors
    except AttributeError:
        request_object_errors = False
    assert bool(request_object_errors) is False

    try:
        request_object_errors = readers.ReaderAddRequestObject.from_dict(dictionaries[3]).errors
    except AttributeError:
        request_object_errors = False
    assert bool(request_object_errors) is False
