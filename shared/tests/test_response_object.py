import pytest

from shared import errors
from shared import response_object
from use_cases.request_objects import books


@pytest.fixture
def response_value():
    return {'key': ['value1', 'value2']}


@pytest.fixture
def response_type():
    return 'ResponseError'


@pytest.fixture
def response_message():
    return 'This is a response error'


def test_response_success_is_true(response_value):
    assert bool(response_object.ResponseSuccess(response_value)) is True


def test_response_failure_is_false(response_type, response_message):
    error = errors.Error(response_type, response_message)
    assert bool(response_object.ResponseFailure(error)) is False


def test_response_success_contains_value(response_value):
    response = response_object.ResponseSuccess(response_value)

    assert response.value == response_value


def test_response_failure_has_type_and_value(response_type, response_message):
    error = errors.Error(response_type, response_message)
    response = response_object.ResponseFailure(error)

    assert response.type == response_type
    assert response.value == response_message


def test_response_failure_contains_value(response_type, response_message):
    error = errors.Error(response_type, response_message)
    response = response_object.ResponseFailure.from_error(error)

    assert response.value == 'This is a response error'


def test_response_failure_from_invalid_request_object():
    error = errors.Error.build_from_invalid_request_object(books.InvalidRequestObject())
    response = response_object.ResponseFailure.from_error(error)

    assert bool(response) is False
