from unittest import mock

from domains.book import Book
from use_cases import books
from use_cases.request_objects import books as request_books


def test_return_book_use_case():
    book = Book(code='f853578c-fc0f-4e65-81b8-566c5dffa35a', title='Fahrenheit 451',
                author='Ray Bradbury', year=1984, language='English', is_available=True, reader=None)

    repo = mock.Mock()
    repo.return_book.return_value = book

    book_return_use_case = books.BookReturnUseCase(repo)
    request_object = request_books.BookReturnRequestObject.from_dict({'pk': 1})

    response_object = book_return_use_case.execute(request_object)
    assert bool(response_object) is True

    repo.return_book.assert_called_with(pk=1)
    assert response_object.value == book
