from use_cases import request_objects


def test_build_reader_list_request_object_without_parameters():
    req = request_objects.ReaderListRequestObject()
    assert bool(req) is True


def test_build_file_list_request_object_from_empty_dict():
    req = request_objects.ReaderListRequestObject.from_dict({})
    assert bool(req) is True


def test_build_reader_list_request_object_with_empty_filters():
    req = request_objects.ReaderListRequestObject(filters={})
    assert req.filters == {}
    assert bool(req) is True


def test_build_reader_list_request_object_from_dict_with_empty_filters():
    req = request_objects.ReaderListRequestObject.from_dict({'filters': {}})
    assert req.filters == {}
    assert bool(req) is True


def test_build_reader_list_request_object_with_filters():
    req = request_objects.ReaderListRequestObject(filters={'a': 1, 'b': 2})
    assert req.filters == {'a': 1, 'b': 2}
    assert bool(req) is True


def test_build_reader_list_request_object_from_dict_with_filters():
    req = request_objects.ReaderListRequestObject.from_dict({'filters': {'a': 1, 'b': 2}})
    assert req.filters == {'a': 1, 'b': 2}
    assert bool(req) is True


def test_build_reader_list_request_object_from_dict_with_invalid_filters():
    req = request_objects.ReaderListRequestObject.from_dict({'filters': 5})
    assert req.has_errors()
    assert req.errors[0]['parameter'] == 'filters'
    assert bool(req) is False