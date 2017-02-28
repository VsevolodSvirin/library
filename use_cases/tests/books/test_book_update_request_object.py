from use_cases.request_objects import books


def test_update_book_details_request_object():
    req = books.BookUpdateRequestObject(pk=1, patch={'title': 'Fahrenheit 451', 'author': 'Ray Bradbury'})
    assert req.pk == 1
    assert req.patch == {'title': 'Fahrenheit 451', 'author': 'Ray Bradbury'}
    assert bool(req) is True


def test_update_book_details_without_patch():
    req = books.BookUpdateRequestObject.from_dict({'pk': 1})
    assert req.has_errors()
    assert 'patch' in req.errors
    assert bool(req) is False


def test_update_book_details_with_bad_patch():
    req = books.BookUpdateRequestObject.from_dict({'pk': 1, 'patch': 'ololo'})
    assert req.has_errors()
    assert 'patch' in req.errors
    assert bool(req) is False


def test_update_book_details_with_bad_patch_parameters():
    req = books.BookUpdateRequestObject.from_dict({'pk': 1, 'patch': {'ololo': 'ololo'}})
    assert req.has_errors()
    assert 'patch' in req.errors
    assert bool(req) is False
