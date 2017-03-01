from use_cases.request_objects import books


def test_return_book_request_object():
    req = books.BookReturnRequestObject(pk=1, patch={'reader': None})
    assert req.pk == 1
    assert bool(req) is True
