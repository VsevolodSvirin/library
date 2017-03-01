import datetime
import json
import pytest

from domains.book import Book
from serializers import books


def test_serialize_domain_book():
    book = Book(code='f853578c-fc0f-4e65-81b8-566c5dffa35a', title='1984', author='George Orwell', year=1984,
                language='English', is_available=True, reader=None)

    expected_json = """
        {
            "code": "f853578c-fc0f-4e65-81b8-566c5dffa35a",
            "title": "1984",
            "author": "George Orwell",
            "year": 1984,
            "language": "English",
            "is_available": true,
            "reader": "null"
        }
    """

    assert json.loads(json.dumps(book, cls=books.BookEncoder)) == json.loads(expected_json)


def test_serialize_domain_book_wrong_type():
    with pytest.raises(TypeError):
        json.dumps(datetime.datetime.now(), cls=books.BookEncoder)
