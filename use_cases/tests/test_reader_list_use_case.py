import datetime

import pytest
from unittest import mock

from domains.reader import Reader
from use_cases import reader_use_cases, request_objects


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


def test_book_list_without_parameters(domain_readers):
    repo = mock.Mock()
    repo.list.return_value = domain_readers

    reader_list_use_case = reader_use_cases.ReaderListUseCase(repo)
    request_object = request_objects.ReaderListRequestObject.from_dict({})

    response_object = reader_list_use_case.execute(request_object)
    assert bool(response_object) is True

    repo.list.assert_called_with()
    assert response_object.value == domain_readers
