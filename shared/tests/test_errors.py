import pytest

from shared import errors
from use_cases.request_objects import books


@pytest.fixture
def error_type():
    return 'ResponseError'


@pytest.fixture
def error_message():
    return 'This is a response error'


def test_error_has_type_and_message(error_type, error_message):
    error = errors.Error(error_type, error_message)

    assert error.type == error_type
    assert error.message == error_message


def test_error_contains_value(error_type, error_message):
    error = errors.Error(error_type, error_message)

    assert error.value == {'type': error_type, 'message': error_message}


def test_response_failure_initialization_with_exception():
    error = errors.Error(error_type, Exception('Just an error message'))

    assert error.type == error_type
    assert error.message == 'Exception: Just an error message'


def test_errors_in_invalid_request_object():
    request_object = books.InvalidRequestObject()
    request_object.add_error('path', 'Is mandatory')
    request_object.add_error('path', "can't be blank")

    error = errors.Error.build_from_invalid_request_object(request_object)

    assert error.type == errors.Error.PARAMETERS_ERROR
    assert error.message == {'path': ['Is mandatory', "can't be blank"]}


def test_error_build_resource_error():
    error = errors.Error.build_resource_error()

    assert error.type == errors.Error.RESOURCE_ERROR
    assert error.message == {'resource error': ['page not found :(']}


def test_error_build_parameters_error():
    error = errors.Error.build_parameters_error('test message')

    assert error.type == errors.Error.PARAMETERS_ERROR
    assert error.message == 'test message'


def test_error_build_system_error():
    error = errors.Error.build_system_error(Exception('test message',))

    assert error.type == errors.Error.SYSTEM_ERROR
    assert error.message == {'system error': ['test message']}
