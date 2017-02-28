from unittest import mock

from domains.book import Book
from domains.reader import Reader
from use_cases import books
from use_cases.request_objects import books as request_books


def test_give_book_use_case():
    reader = Reader(code='', full_name='', reg_date='')
    book = Book(code='f853578c-fc0f-4e65-81b8-566c5dffa35a', title='Fahrenheit 451',
                author='Ray Bradbury', year=1984, language='English', is_available=False, reader=reader)

    repo = mock.Mock()
    repo.give.return_value = book

    book_give_use_case = books.BookGiveUseCase(repo, reader)
    request_object = request_books.BookGiveRequestObject.from_dict({'pk': 1, 'reader': reader})

    response_object = book_give_use_case.execute(request_object)
    assert bool(response_object) is True

    repo.give.assert_called_with(pk=1, reader=reader)
    assert response_object.value == book
