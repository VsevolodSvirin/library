from unittest import mock

import pytest

from domains.book import Book
from use_cases import books
from use_cases.request_objects import books as request_books


@pytest.fixture
def adict():
    parameters = {'title': '1984', 'author': 'George Orwell', 'year': 1984, 'language': 'English'}
    return parameters


def test_book_addition(adict):
    code = 'f853578c-fc0f-4e65-81b8-566c5dffa35a'
    book = Book(code=code, title=adict['title'], author=adict['author'], year=adict['year'],
                language=adict['language'], is_available=True, reader=None)
    repo = mock.Mock()
    repo.from_dict.return_value = book

    book_list_add_case = books.BookAddUseCase(repo)
    request_object = request_books.BookAddRequestObject.from_dict(adict)

    response_object = book_list_add_case.execute(request_object)
    assert bool(response_object) is True

    repo.from_dict.assert_called_with(adict)
    assert response_object.value == book
