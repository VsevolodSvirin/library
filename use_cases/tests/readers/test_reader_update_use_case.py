from unittest import mock

from domains.reader import Reader
from use_cases import readers
from use_cases.request_objects import readers as request_readers


def test_update_reader_update():
    updated_reader = Reader(code='f853578c-fc0f-4e65-81b8-566c5dffa35a',
                            full_name='VS', reg_date='2010-01-01')

    repo = mock.Mock()
    repo.update.return_value = updated_reader

    reader_update_use_case = readers.ReaderUpdateUseCase(repo)
    request_object = request_readers.ReaderUpdateRequestObject.from_dict(
        {'pk': 1, 'patch': {'full_name': 'VS'}}
    )

    response_object = reader_update_use_case.execute(request_object)
    assert bool(response_object) is True

    repo.update.assert_called_with(patch={'full_name': 'VS'}, pk=1)
    assert response_object.value == updated_reader


def test_reader_update_without_patch():
    updated_reader = Reader(code='f853578c-fc0f-4e65-81b8-566c5dffa35a',
                            full_name='VS', reg_date='2010-01-01')

    repo = mock.Mock()
    repo.update.return_value = updated_reader

    reader_update_use_case = readers.ReaderUpdateUseCase(repo)
    request_object = request_readers.ReaderUpdateRequestObject.from_dict(
        {'pk': 1}
    )

    response_object = reader_update_use_case.execute(request_object)
    assert bool(response_object) is False
    assert response_object.value == {'patch': ['has to pass patch instructions']}


def test_reader_update_with_bad_patch():
    updated_reader = Reader(code='f853578c-fc0f-4e65-81b8-566c5dffa35a',
                            full_name='VS', reg_date='2010-01-01')

    repo = mock.Mock()
    repo.update.return_value = updated_reader

    reader_update_use_case = readers.ReaderUpdateUseCase(repo)
    request_object = request_readers.ReaderUpdateRequestObject.from_dict(
        {'pk': 1, 'patch': 100500}
    )

    response_object = reader_update_use_case.execute(request_object)
    assert bool(response_object) is False
    assert response_object.value == {'patch': ['is not iterable']}


def test_reader_update_with_bad_patch_parameters():
    updated_reader = Reader(code='f853578c-fc0f-4e65-81b8-566c5dffa35a',
                            full_name='VS', reg_date='2010-01-01')

    repo = mock.Mock()
    repo.update.return_value = updated_reader

    reader_update_use_case = readers.ReaderUpdateUseCase(repo)
    request_object = request_readers.ReaderUpdateRequestObject.from_dict(
        {'pk': 1, 'patch': {'ololo': 'ololo'}}
    )

    response_object = reader_update_use_case.execute(request_object)
    assert bool(response_object) is False
    assert response_object.value == {'patch': ['parameters in patch are wrong']}
