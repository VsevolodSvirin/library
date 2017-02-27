from use_cases.request_objects import books


def test_build_book_details_request_object():
    req = books.BookDetailsRequestObject(pk=1)
    assert req.pk == 1
    assert bool(req) is True


def test_build_book_details_request_object_from_dict():
    req = books.BookDetailsRequestObject.from_dict({'pk': 1})
    assert req.pk == 1
    assert bool(req) is True


def test_build_book_details_request_object_from_empty_dict():
    req = books.BookDetailsRequestObject.from_dict({})
    assert req.has_errors()
    assert 'request dictionary' in req.errors
    assert bool(req) is False


def test_build_book_details_request_object_from_big_dict():
    req = books.BookDetailsRequestObject.from_dict({'lol': True, 'pk': 2, 'a': 'b'})
    assert req.pk == 2
    assert bool(req) is True


def test_build_book_details_request_object_from_string_pk():
    req = books.BookDetailsRequestObject.from_dict({'pk': '1'})
    assert req.pk == 1
    assert bool(req) is True


def test_build_details_request_object_from_bad_pk():
    req = books.BookDetailsRequestObject.from_dict({'pk': 'ololo'})
    assert req.has_errors()
    assert 'primary key' in req.errors
    assert bool(req) is False
