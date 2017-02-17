import pytest

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
    assert bool(response_object.ResponseFailure(response_type, response_message)) is False


def test_response_success_contains_value(response_value):
    response = response_object.ResponseSuccess(response_value)

    assert response.value == response_value


def test_response_failure_has_type_and_message(response_type, response_message):
    response = response_object.ResponseFailure(response_type, response_message)

    assert response.type == response_type
    assert response.message == response_message


def test_response_failure_contains_value(response_type, response_message):
    response = response_object.ResponseFailure(response_type, response_message)

    assert response.value == {'type': response_type, 'message': response_message}


def test_response_failure_initialization_with_exception():
    response = response_object.ResponseFailure(response_type, Exception('Just an error message'))

    assert bool(response) is False
    assert response.type == response_type
    assert response.message == "Exception: Just an error message"


def test_response_failure_from_invalid_request_object():
    response = response_object.ResponseFailure.build_from_invalid_request_object(books.InvalidRequestObject())

    assert bool(response) is False


def test_response_failure_from_invalid_request_object_with_errors():
    request_object = books.InvalidRequestObject()
    request_object.add_error('path', 'Is mandatory')
    request_object.add_error('path', "can't be blank")

    response = response_object.ResponseFailure.build_from_invalid_request_object(request_object)

    assert bool(response) is False
    assert response.type == response_object.ResponseFailure.PARAMETERS_ERROR
    assert response.message == [{'path': 'Is mandatory'}, {'path': "can't be blank"}]


def test_response_failure_build_resource_error():
    response = response_object.ResponseFailure.build_resource_error("test message")

    assert bool(response) is False
    assert response.type == response_object.ResponseFailure.RESOURCE_ERROR
    assert response.message == "test message"


def test_response_failure_build_parameters_error():
    response = response_object.ResponseFailure.build_parameters_error("test message")

    assert bool(response) is False
    assert response.type == response_object.ResponseFailure.PARAMETERS_ERROR
    assert response.message == "test message"


def test_response_failure_build_system_error():
    response = response_object.ResponseFailure.build_system_error("test message")

    assert bool(response) is False
    assert response.type == response_object.ResponseFailure.SYSTEM_ERROR
    assert response.message == "test message"
