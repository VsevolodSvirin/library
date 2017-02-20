import pytest

from shared.request_object import InvalidRequestObject
from use_cases.request_objects import books


@pytest.fixture
def dictionaries():
    dict1 = {"title": "1984", "author": "George Orwell", "year": 1984, "language": "English"}
    dict2 = {}
    dict3 = {"title": "1984", "author": "George Orwell", "year": "ololo", "language": "English"}
    dict4 = {"title": "1984", "author": "George Orwell", "year": "1984", "language": "English"}
    dict5 = {"title": "1984", "author": True, "year": "ololo", "language": "English"}
    return [dict1, dict2, dict3, dict4, dict5]


def test_new_book_validation(dictionaries):
    request_object = books.BookAddRequestObject.from_dict(dictionaries[0])
    assert bool(request_object) is True

    request_object = books.BookAddRequestObject.from_dict(dictionaries[1])
    assert bool(request_object) is False

    request_object = books.BookAddRequestObject.from_dict(dictionaries[2])
    assert bool(request_object) is False

    request_object = books.BookAddRequestObject.from_dict(dictionaries[3])
    assert bool(request_object) is True

    request_object = books.BookAddRequestObject.from_dict(dictionaries[4])
    assert bool(request_object) is False


def test_validation_error_messages(dictionaries):
    try:
        request_object_errors = books.BookAddRequestObject.from_dict(dictionaries[0]).errors
    except AttributeError:
        request_object_errors = False
    assert bool(request_object_errors) is False

    try:
        request_object_errors = books.BookAddRequestObject.from_dict(dictionaries[1]).errors
    except AttributeError:
        request_object_errors = False
    assert bool(request_object_errors) is True
    invalid_request_object = InvalidRequestObject()
    invalid_request_object.add_error(parameter='year', message=['required key not provided'])
    invalid_request_object.add_error(parameter='title', message=['required key not provided'])
    invalid_request_object.add_error(parameter='author', message=['required key not provided'])
    invalid_request_object.add_error(parameter='language', message=['required key not provided'])

    assert sorted(request_object_errors) == \
           sorted(invalid_request_object.errors)

    try:
        request_object_errors = books.BookAddRequestObject.from_dict(dictionaries[2]).errors
    except AttributeError:
        request_object_errors = False
    assert bool(request_object_errors) is True

    invalid_request_object = InvalidRequestObject()
    invalid_request_object.add_error(parameter='year', message=['does not match regular expression'])
    assert sorted(request_object_errors) == \
           sorted(invalid_request_object.errors)

    try:
        request_object_errors = books.BookAddRequestObject.from_dict(dictionaries[3]).errors
    except AttributeError:
        request_object_errors = False
    assert bool(request_object_errors) is False

    try:
        request_object_errors = books.BookAddRequestObject.from_dict(dictionaries[4]).errors
    except AttributeError:
        request_object_errors = False
    assert bool(request_object_errors) is True

    invalid_request_object = InvalidRequestObject()
    invalid_request_object.add_error(parameter='year', message=['does not match regular expression'])
    invalid_request_object.add_error(parameter='author', message=['expected str'])
    assert sorted(request_object_errors) == \
           sorted(invalid_request_object.errors)


