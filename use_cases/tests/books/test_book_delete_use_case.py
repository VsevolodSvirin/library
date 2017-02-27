from unittest import mock

from use_cases import books
from use_cases.request_objects import books as request_books


def test_delete_book_use_case():
    repo = mock.Mock()
    repo.delete.return_value = None

    book_delete_use_case = books.BookDeleteUseCase(repo)
    request_object = request_books.BookDeleteRequestObject.from_dict({'pk': 1})

    response_object = book_delete_use_case.execute(request_object)
    assert bool(response_object) is True

    repo.delete.assert_called_with(pk=1)
    assert response_object.value is None
