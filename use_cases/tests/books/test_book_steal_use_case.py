from unittest import mock

from domains.book import Book
from use_cases import books
from use_cases.request_objects import books as request_books


def test_steal_book_use_case():
    book = Book(code='f853578c-fc0f-4e65-81b8-566c5dffa35a', title='Fahrenheit 451',
                author='Ray Bradbury', year=1984, language='English', is_available=False, reader=None)

    repo = mock.Mock()
    repo.steal.return_value = book

    book_steal_use_case = books.BookStealUseCase(repo)
    request_object = request_books.BookStealRequestObject.from_dict({'pk': 1})

    response_object = book_steal_use_case.execute(request_object)
    assert bool(response_object) is True

    repo.steal.assert_called_with(pk=1)
    assert response_object.value == book
