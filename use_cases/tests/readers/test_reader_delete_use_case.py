from unittest import mock

from use_cases import readers
from use_cases.request_objects import readers as request_readers


def test_delete_reader_use_case():
    repo = mock.Mock()
    repo.delete.return_value = None

    reader_delete_use_case = readers.ReaderDeleteUseCase(repo)
    request_object = request_readers.ReaderDeleteRequestObject.from_dict({'pk': 1})

    response_object = reader_delete_use_case.execute(request_object)
    assert bool(response_object) is True

    repo.delete.assert_called_with(pk=1)
    assert response_object.value is None
