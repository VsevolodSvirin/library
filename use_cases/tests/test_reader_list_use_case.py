import datetime
from unittest import mock

import pytest

from domains.reader import Reader
from shared import response_object
from use_cases import readers
from use_cases.request_objects import readers as request_readers


@pytest.fixture
def domain_readers():
    reader1 = Reader("r2rwr3re-bdfc-e2ww-5644-hd94id04kd9r",
                     full_name="John Smith", reg_date=datetime.date(2016, 1, 1))
    reader2 = Reader("q3eqweq2-ffwe-r23r-43r3-5eh5thrt3trw",
                     full_name="John Doe", reg_date=datetime.date(2016, 6, 1))
    reader3 = Reader("43r3regl-grgf-kjhm-gg3g-2r2r2r2e22rw",
                     full_name="Jason Statham", reg_date=datetime.date(2010, 9, 15))
    reader4 = Reader("4yfhfjuk-gefd-e2wq-2rsf-23rdsghdtdhf",
                     full_name="Marie Curie", reg_date=datetime.date(1900, 12, 15))
    return [reader1, reader2, reader3, reader4]


def test_reader_list_without_parameters(domain_readers):
    repo = mock.Mock()
    repo.list.return_value = domain_readers

    reader_list_use_case = readers.ReaderListUseCase(repo)
    request_object = request_readers.ReaderListRequestObject.from_dict({})

    response_object = reader_list_use_case.execute(request_object)
    assert bool(response_object) is True

    repo.list.assert_called_with(filters=None)
    assert response_object.value == domain_readers


def test_reader_list_with_filters(domain_readers):
    repo = mock.Mock()
    repo.list.return_value = domain_readers

    reader_list_use_case = readers.ReaderListUseCase(repo)
    qry_filters = {"a": 5}
    request_object = request_readers.ReaderListRequestObject.from_dict({"filters": qry_filters})

    response_object = reader_list_use_case.execute(request_object)

    assert bool(response_object) is True
    repo.list.assert_called_with(filters=qry_filters)
    assert response_object.value == domain_readers


def test_reader_list_handles_generic_error():
    repo = mock.Mock()
    repo.list.side_effect = Exception("Just an error message")

    reader_list_use_case = readers.ReaderListUseCase(repo)
    request_object = request_readers.ReaderListRequestObject.from_dict({})

    response = reader_list_use_case.execute(request_object)

    assert bool(response) is False
    assert response.value == {
        "type": response_object.ResponseFailure.SYSTEM_ERROR,
        "message": "Exception: Just an error message"
    }


def test_reader_list_handles_bad_request():
    repo = mock.Mock()

    reader_list_use_case = readers.ReaderListUseCase(repo)
    request_object = request_readers.ReaderListRequestObject.from_dict({"filters": 5})

    response = reader_list_use_case.execute(request_object)

    assert bool(response) is False
    assert response.value == {
        "type": response_object.ResponseFailure.PARAMETERS_ERROR,
        "message": [{'filters': 'Is not iterable'}]
    }
