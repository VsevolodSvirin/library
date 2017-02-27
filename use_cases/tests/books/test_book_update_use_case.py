from unittest import mock

from domains.book import Book
from use_cases import books
from use_cases.request_objects import books as request_books


def test_update_book_update():
    updated_book = Book(code='f853578c-fc0f-4e65-81b8-566c5dffa35a', title='Fahrenheit 451',
                        author='Ray Bradbury', year=1984, language='English', is_available=True, reader=None)

    repo = mock.Mock()
    repo.update.return_value = updated_book

    book_update_use_case = books.BookUpdateUseCase(repo)
    request_object = request_books.BookUpdateRequestObject.from_dict(
        {'pk': 1, 'patch': {'title': 'Fahrenheit 451', 'author': 'Ray Bradbury'}}
    )

    response_object = book_update_use_case.execute(request_object)
    assert bool(response_object) is True

    repo.update.assert_called_with(patch={'title': 'Fahrenheit 451', 'author': 'Ray Bradbury'}, pk=1)
    assert response_object.value == updated_book


def test_book_update_without_patch():
    updated_book = Book(code='f853578c-fc0f-4e65-81b8-566c5dffa35a', title='Fahrenheit 451',
                        author='Ray Bradbury', year=1984, language='English', is_available=True, reader=None)

    repo = mock.Mock()
    repo.update.return_value = updated_book

    book_update_use_case = books.BookUpdateUseCase(repo)
    request_object = request_books.BookUpdateRequestObject.from_dict(
        {'pk': 1}
    )

    response_object = book_update_use_case.execute(request_object)
    assert bool(response_object) is False
    assert response_object.value == {'patch': ['has to pass patch instructions']}


def test_book_update_with_bad_patch():
    updated_book = Book(code='f853578c-fc0f-4e65-81b8-566c5dffa35a', title='Fahrenheit 451',
                        author='Ray Bradbury', year=1984, language='English', is_available=True, reader=None)

    repo = mock.Mock()
    repo.update.return_value = updated_book

    book_update_use_case = books.BookUpdateUseCase(repo)
    request_object = request_books.BookUpdateRequestObject.from_dict(
        {'pk': 1, 'patch': 100500}
    )

    response_object = book_update_use_case.execute(request_object)
    assert bool(response_object) is False
    assert response_object.value == {'patch': ['has to be dictionary with patch instructions']}


def test_book_update_with_bad_patch_parameters():
    updated_book = Book(code='f853578c-fc0f-4e65-81b8-566c5dffa35a', title='Fahrenheit 451',
                        author='Ray Bradbury', year=1984, language='English', is_available=True, reader=None)

    repo = mock.Mock()
    repo.update.return_value = updated_book

    book_update_use_case = books.BookUpdateUseCase(repo)
    request_object = request_books.BookUpdateRequestObject.from_dict(
        {'pk': 1, 'patch': {'ololo': 'ololo'}}
    )

    response_object = book_update_use_case.execute(request_object)
    assert bool(response_object) is False
    assert response_object.value == {'patch': ['parameters in patch are wrong']}
