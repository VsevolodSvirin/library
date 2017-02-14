from use_cases import request_objects


def test_build_book_list_request_object_without_parameters():
    req = request_objects.BookListRequestObject()
    assert bool(req) is True


def test_build_file_list_request_object_from_empty_dict():
    req = request_objects.BookListRequestObject.from_dict({})
    assert bool(req) is True
