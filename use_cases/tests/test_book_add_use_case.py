from unittest import mock

import pytest

from domains.book import Book
from use_cases import book_use_cases
from use_cases.requests import books


@pytest.fixture
def adict():
    parameters = {'title': '1984', 'author': 'George Orwell', 'year': 1984, 'language': 'English'}
    return parameters


def test_book_list_without_parameters(adict):
    code = 'f853578c-fc0f-4e65-81b8-566c5dffa35a'
    book = Book(code, adict['title'], adict['author'], adict['year'], adict['language'], True, None)
    repo = mock.Mock()
    repo.create.return_value = book

    book_list_add_case = book_use_cases.BookAddUseCase(repo)
    request_object = books.BookAddRequestObject.from_dict(adict)

    response_object = book_list_add_case.execute(request_object)
    assert bool(response_object) is True

    repo.create.assert_called_with(book=adict)
    assert response_object.value == book
