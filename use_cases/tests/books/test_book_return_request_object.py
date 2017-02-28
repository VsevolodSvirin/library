from use_cases.request_objects import books


def test_return_book_request_object():
    req = books.BookReturnRequestObject(pk=1)
    assert req.pk == 1
    assert bool(req) is True


def test_give_book_with_invalid_pk():
    req = books.BookReturnRequestObject.from_dict({'pk': 'ololo'})
    assert req.has_errors()
    assert 'primary key' in req.errors
    assert bool(req) is False
