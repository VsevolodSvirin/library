from use_cases.request_objects import readers


def test_delete_reader_with_pk():
    req = readers.ReaderDeleteRequestObject(pk=1)
    assert req.pk == 1
    assert bool(req) is True


def test_delete_reader_with_invalid_pk():
    req = readers.ReaderDeleteRequestObject.from_dict({'pk': 'ololo'})
    assert req.has_errors()
    assert 'primary key' in req.errors
    assert bool(req) is False
