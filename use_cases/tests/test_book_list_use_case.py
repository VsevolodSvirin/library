import datetime
from unittest import mock

import pytest

from domains.book import Book
from domains.reader import Reader
from shared import errors
from shared import response_object
from use_cases import books
from use_cases.request_objects import books as request_books


@pytest.fixture
def domain_books():
    reader = Reader("r2rwr3re-bdfc-e2ww-5644-hd94id04kd9r", full_name="John Smith", reg_date=datetime.date(2016, 1, 1))
    book1 = Book("f853578c-fc0f-4e65-81b8-566c5dffa35a", title="1984", author="George Orwell",
                 year=1984, language="English", is_available=True, reader=None)
    book2 = Book("fe2c3195-aeff-487a-a08f-e0bdc0ec6e9a", title="The Lord of the Rings", author="J.R.R. Tolkien",
                 year=2000, language="English", is_available=False, reader=reader)
    book3 = Book("913694c6-435a-4366-ba0d-da5334a611b2", title="The Master and Margarita", author="Mikhail Bulgakov",
                 year=2005, language="Russian", is_available=False, reader=None)
    book4 = Book("eed76e77-55c1-41ce-985d-ca49bf6c0585", title="The Dark Tower", author="Stephen King",
                 year=2015, language="English", is_available=True, reader=None)
    return [book1, book2, book3, book4]


def test_book_list_without_parameters(domain_books):
    repo = mock.Mock()
    repo.list.return_value = domain_books

    book_list_use_case = books.BookListUseCase(repo)
    request_object = request_books.BookListRequestObject.from_dict({})

    response_object = book_list_use_case.execute(request_object)
    assert bool(response_object) is True

    repo.list.assert_called_with(filters=None)
    assert response_object.value == domain_books


def test_book_list_with_filters(domain_books):
    repo = mock.Mock()
    repo.list.return_value = domain_books

    book_list_use_case = books.BookListUseCase(repo)
    qry_filters = {"a": 5}
    request_object = request_books.BookListRequestObject.from_dict({"filters": qry_filters})

    response_object = book_list_use_case.execute(request_object)

    assert bool(response_object) is True
    repo.list.assert_called_with(filters=qry_filters)
    assert response_object.value == domain_books


def test_book_list_handles_generic_error():
    repo = mock.Mock()
    repo.list.side_effect = Exception("Just an error message")

    book_list_use_case = books.BookListUseCase(repo)
    request_object = request_books.BookListRequestObject.from_dict({})

    response = book_list_use_case.execute(request_object)

    assert bool(response) is False
    assert response.value == "Exception: Just an error message"

def test_book_list_handles_bad_request():
    repo = mock.Mock()

    book_list_use_case = books.BookListUseCase(repo)
    request_object = request_books.BookListRequestObject.from_dict({"filters": 5})

    response = book_list_use_case.execute(request_object)

    assert bool(response) is False
    assert response.value == [{'filters': 'Is not iterable'}]
