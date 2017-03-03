import json
from unittest import mock

from domains.book import Book

from shared import response_object as res

dictionary = {
    'code': '3251a5bd-86be-428d-8ae9-6e51a8048c33',
    'title': '1984',
    'author': 'George Orwell',
    'year': 1984,
    'language': 'English',
    'is_available': True,
    'reader': None
}

book = Book.from_dict(dictionary)

books = [book]


@mock.patch('flask_interface.library.books.book.BookListUseCase')
def test_get(mock_use_case, client):
    mock_use_case().execute.return_value = res.ResponseSuccess(books)

    http_response = client.get('/books')

    assert json.loads(http_response.data) == [dictionary]
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'
