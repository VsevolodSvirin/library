import datetime

import pytest
from unittest import mock

from domains.book import Book
from domains.reader import Reader
from use_cases import book_use_cases


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
    book_list_use_case = book_use_cases.BookListUseCase(repo)
    result = book_list_use_case.execute()
    repo.list.assert_called_with()
    assert result == domain_books
