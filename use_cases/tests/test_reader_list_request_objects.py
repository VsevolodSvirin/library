import datetime

from use_cases.request_objects import readers


def test_build_reader_list_request_object_without_parameters():
    req = readers.ReaderListRequestObject()
    assert bool(req) is True


def test_build_file_list_request_object_from_empty_dict():
    req = readers.ReaderListRequestObject.from_dict({})
    assert bool(req) is True


def test_build_reader_list_request_object_with_empty_filters():
    req = readers.ReaderListRequestObject(filters={})
    assert req.filters == {}
    assert bool(req) is True


def test_build_reader_list_request_object_from_dict_with_empty_filters():
    req = readers.ReaderListRequestObject.from_dict({'filters': {}})
    assert req.filters == {}
    assert bool(req) is True


def test_build_reader_list_request_object_with_filters():
    req = readers.ReaderListRequestObject(filters={'a': 1, 'b': 2})
    assert req.filters == {'a': 1, 'b': 2}
    assert bool(req) is True


def test_build_reader_list_request_object_from_dict_with_good_filters():
    req = readers.ReaderListRequestObject(filters={'full_name': 'VS'})
    assert req.filters == {'full_name': 'VS'}
    assert bool(req) is True


def test_build_reader_list_request_object_from_dict_with_bad_filters():
    req = readers.ReaderListRequestObject.from_dict({'filters': {'a': 1, 'b': 2}})
    assert req.has_errors()
    assert 'a' in req.errors.keys()
    assert 'b' in req.errors.keys()
    assert bool(req) is False


def test_build_reader_list_request_object_from_dict_with_invalid_filters():
    req = readers.ReaderListRequestObject.from_dict({'filters': 5})
    assert req.has_errors()
    assert 'filters' in req.errors.keys()
    assert bool(req) is False


def test_build_book_list_request_object_from_dict_with_filtering_tags_and_year():
    req = readers.ReaderListRequestObject.from_dict({'filters': {'reg_date__gt': datetime.date(2015, 1, 1)}})
    assert req.filters == {'reg_date__gt': datetime.date(2015, 1, 1)}
    assert bool(req) is True


def test_build_book_list_request_object_from_dict_with_filtering_tags_and_bad_parameter():
    req = readers.ReaderListRequestObject.from_dict({'filters': {'full_name__gt': 'VS'}})
    assert req.has_errors()
    assert 'full_name' in req.errors.keys()
    assert bool(req) is False


def test_build_book_list_request_object_from_dict_with__bad_filtering_tags():
    req = readers.ReaderListRequestObject.from_dict(
        {'filters': {'reg_date__in': [datetime.date(2010, 1, 1), datetime.date(2015, 1, 1)]}})
    assert req.has_errors()
    assert 'reg_date' in req.errors.keys()
    assert bool(req) is False
