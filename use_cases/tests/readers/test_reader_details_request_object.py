from use_cases.request_objects import readers


def test_build_reader_details_request_object():
    req = readers.ReaderDetailsRequestObject(pk=1)
    assert req.pk == 1
    assert bool(req) is True


def test_build_reader_details_request_object_from_dict():
    req = readers.ReaderDetailsRequestObject.from_dict({'pk': 1})
    assert req.pk == 1
    assert bool(req) is True


def test_build_reader_details_request_object_from_empty_dict():
    req = readers.ReaderDetailsRequestObject.from_dict({})
    assert req.has_errors()
    assert 'request dictionary' in req.errors
    assert bool(req) is False


def test_build_reader_details_request_object_from_big_dict():
    req = readers.ReaderDetailsRequestObject.from_dict({'lol': True, 'pk': 2, 'a': 'b'})
    assert req.pk == 2
    assert bool(req) is True


def test_build_reader_details_request_object_from_string_pk():
    req = readers.ReaderDetailsRequestObject.from_dict({'pk': '1'})
    assert req.pk == 1
    assert bool(req) is True


def test_build_details_request_object_from_bad_pk():
    req = readers.ReaderDetailsRequestObject.from_dict({'pk': 'ololo'})
    assert req.has_errors()
    assert 'primary key' in req.errors
    assert bool(req) is False
