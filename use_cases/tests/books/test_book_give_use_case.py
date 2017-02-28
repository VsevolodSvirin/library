from unittest import mock

from domains.book import Book
from use_cases import books
from use_cases.request_objects import books as request_books


def test_update_book_update():
    book = Book(code='f853578c-fc0f-4e65-81b8-566c5dffa35a', title='Fahrenheit 451',
                author='Ray Bradbury', year=1984, language='English', is_available=True, reader=None)

    repo = mock.Mock()
    repo.update.return_value = book

    book_update_use_case = books.BookUpdateUseCase(repo)
    request_object = request_books.BookUpdateRequestObject.from_dict(
        {'pk': 1, 'patch': {'title': 'Fahrenheit 451', 'author': 'Ray Bradbury'}}
    )

    response_object = book_update_use_case.execute(request_object)
    assert bool(response_object) is True

    repo.update.assert_called_with(patch={'title': 'Fahrenheit 451', 'author': 'Ray Bradbury'}, pk=1)
    assert response_object.value == book
