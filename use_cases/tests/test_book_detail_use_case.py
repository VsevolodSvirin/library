from unittest import mock

from domains.book import Book
from use_cases import books
from use_cases.request_objects import books as request_books


def test_get_book_details():
    book = Book(code='f853578c-fc0f-4e65-81b8-566c5dffa35a', title='1984',
                author='George Orwell', year=1984, language='English', is_available=True, reader=None)
    repo = mock.Mock()
    repo.details.return_value = book

    book_details_use_case = books.BookDetailsUseCase(repo)
    request_object = request_books.BookDetailsRequestObject.from_dict({'pk': 1})

    response_object = book_details_use_case.execute(request_object)
    assert bool(response_object) is True

    repo.details.assert_called_with(pk=1)
    assert response_object.value == book


def test_book_details_with_bad_key():
    book = Book(code='f853578c-fc0f-4e65-81b8-566c5dffa35a', title='1984',
                author='George Orwell', year=1984, language='English', is_available=True, reader=None)
    repo = mock.Mock()
    repo.details.return_value = book

    book_details_use_case = books.BookDetailsUseCase(repo)
    request_object = request_books.BookDetailsRequestObject.from_dict({'pk': 'ololo'})

    response_object = book_details_use_case.execute(request_object)

    assert bool(response_object) is False
    assert response_object.value == {'primary key': ['has to be integer']}


def test_book_details_without_key():
    book = Book(code='f853578c-fc0f-4e65-81b8-566c5dffa35a', title='1984',
                author='George Orwell', year=1984, language='English', is_available=True, reader=None)
    repo = mock.Mock()
    repo.details.return_value = book

    book_details_use_case = books.BookDetailsUseCase(repo)
    request_object = request_books.BookDetailsRequestObject.from_dict({'blah': 'ololo'})

    response_object = book_details_use_case.execute(request_object)

    assert bool(response_object) is False
    assert response_object.value == {'primary key': ['has to pass primary key']}
