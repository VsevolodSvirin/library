import datetime
import uuid

from domains.reader import Reader
from use_cases.request_objects import books


def test_give_book_request_object():
    code = uuid.uuid4()
    req = books.BookGiveRequestObject(pk=1,
                                      reader=Reader(code=code, full_name='VS', reg_date=datetime.date(2017, 2, 13)))
    assert req.pk == 1
    assert bool(req) is True


def test_give_book_without_reader():
    req = books.BookGiveRequestObject.from_dict({'pk': 1})
    assert req.has_errors()
    assert 'reader' in req.errors
    assert bool(req) is False


def test_give_book_with_bad_reader():
    req = books.BookGiveRequestObject.from_dict({'pk': 1, 'reader': 'ololo'})
    assert req.has_errors()
    assert 'reader' in req.errors
    assert bool(req) is False
