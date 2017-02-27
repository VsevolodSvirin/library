from use_cases.request_objects import books


def test_delete_book_with_pk():
    req = books.BookDeleteRequestObject(pk=1)
    assert req.pk == 1
    assert bool(req) is True


def test_delete_book_with_invalid_pk():
    req = books.BookDeleteRequestObject.from_dict({'pk': 'ololo'})
    assert req.has_errors()
    assert 'primary key' in req.errors
    assert bool(req) is False
