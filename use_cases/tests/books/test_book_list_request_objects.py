from use_cases.request_objects import books


def test_build_book_list_request_object_without_parameters():
    req = books.BookListRequestObject()
    assert req.filters is None
    assert bool(req) is True


def test_build_file_list_request_object_from_empty_dict():
    req = books.BookListRequestObject.from_dict({})
    assert req.filters is None
    assert bool(req) is True


def test_build_book_list_request_object_with_empty_filters():
    req = books.BookListRequestObject(filters={})
    assert req.filters == {}
    assert bool(req) is True


def test_build_book_list_request_object_from_dict_with_empty_filters():
    req = books.BookListRequestObject.from_dict({'filters': {}})
    assert req.filters == {}
    assert bool(req) is True


def test_build_book_list_request_object_with_filters():
    req = books.BookListRequestObject(filters={'a': 1, 'b': 2})
    assert req.filters == {'a': 1, 'b': 2}
    assert bool(req) is True


def test_build_book_list_request_object_from_dict_with_good_filters():
    req = books.BookListRequestObject.from_dict({'filters': {'title__eq': '1984', 'year__eq': 1984}})
    assert req.filters == {'title__eq': '1984', 'year__eq': 1984}
    assert bool(req) is True


def test_build_book_list_request_object_from_dict_with_bad_filters():
    req = books.BookListRequestObject.from_dict({'filters': {'a': 1, 'b': 2}})
    assert req.has_errors()
    assert 'a' in req.errors.keys()
    assert 'b' in req.errors.keys()
    assert bool(req) is False


def test_build_book_list_request_object_from_dict_with_invalid_filters():
    req = books.BookListRequestObject.from_dict({'filters': 5})
    assert req.has_errors()
    assert 'filters' in req.errors.keys()
    assert bool(req) is False


def test_build_book_list_request_object_from_dict_with_filtering_tags_and_year():
    req = books.BookListRequestObject.from_dict({'filters': {'year__gt': 1984}})
    assert req.filters == {'year__gt': 1984}
    assert bool(req) is True


def test_build_book_list_request_object_from_dict_with_filtering_tags_and_bad_parameter():
    req = books.BookListRequestObject.from_dict({'filters': {'title__gt': 1984}})
    assert req.has_errors()
    assert 'title' in req.errors.keys()
    assert bool(req) is False


def test_build_book_list_request_object_from_dict_with__bad_filtering_tags():
    req = books.BookListRequestObject.from_dict({'filters': {'year__in': [1980, 1990]}})
    assert req.has_errors()
    assert 'year' in req.errors.keys()
    assert bool(req) is False
