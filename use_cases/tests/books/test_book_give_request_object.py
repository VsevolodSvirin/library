import datetime
import uuid

from domains.reader import Reader
from use_cases.request_objects import books


def test_give_book_request_object():
    code = uuid.uuid4()
    req = books.BookGiveRequestObject(pk=1, patch={})
    assert req.pk == 1
    assert bool(req) is True
