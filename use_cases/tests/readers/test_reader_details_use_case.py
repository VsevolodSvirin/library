import datetime
from unittest import mock

from domains.reader import Reader
from use_cases import readers
from use_cases.request_objects import readers as request_readers


def test_get_book_details():
    reader = Reader(code='f853578c-fc0f-4e65-81b8-566c5dffa35a',
                    full_name='VS', reg_date=datetime.date(2010, 1, 1))
    repo = mock.Mock()
    repo.details.return_value = reader

    reader_details_use_case = readers.ReaderDetailsUseCase(repo)
    request_object = request_readers.ReaderDetailsRequestObject.from_dict({'pk': 1})

    response_object = reader_details_use_case.execute(request_object)
    assert bool(response_object) is True

    repo.details.assert_called_with(pk=1)
    assert response_object.value == reader


def test_book_details_with_bad_key():
    reader = Reader(code='f853578c-fc0f-4e65-81b8-566c5dffa35a',
                    full_name='VS', reg_date=datetime.date(2010, 1, 1))
    repo = mock.Mock()
    repo.details.return_value = reader

    reader_details_use_case = readers.ReaderDetailsUseCase(repo)
    request_object = request_readers.ReaderDetailsRequestObject.from_dict({'pk': 'ololo'})

    response_object = reader_details_use_case.execute(request_object)

    assert bool(response_object) is False
    assert response_object.value == {'primary key': ['has to be integer']}


def test_book_details_without_key():
    reader = Reader(code='f853578c-fc0f-4e65-81b8-566c5dffa35a',
                    full_name='VS', reg_date=datetime.date(2010, 1, 1))
    repo = mock.Mock()
    repo.details.return_value = reader

    reader_details_use_case = readers.ReaderDetailsUseCase(repo)
    request_object = request_readers.ReaderDetailsRequestObject.from_dict({'blah': 'ololo'})

    response_object = reader_details_use_case.execute(request_object)

    assert bool(response_object) is False
    assert response_object.value == {'primary key': ['has to pass primary key']}
