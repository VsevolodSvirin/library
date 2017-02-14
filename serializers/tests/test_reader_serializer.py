import datetime
import json
import pytest

from domains.reader import Reader
from serializers import reader_serializer


def test_serialize_domain_reader():
    reader = Reader("f853578c-fc0f-4e65-81b8-566c5dffa35a", full_name="VS", reg_date=datetime.date(2017, 2, 13))

    expected_json = """
        {
            "code": "f853578c-fc0f-4e65-81b8-566c5dffa35a",
            "full_name": "VS",
            "reg_date": "2017-02-13"
        }
    """

    assert json.loads(json.dumps(reader, cls=reader_serializer.ReaderEncoder)) == json.loads(expected_json)


def test_serialize_domain_book_wrong_type():
    with pytest.raises(TypeError):
        json.dumps(datetime.datetime.now(), cls=reader_serializer.ReaderEncoder)
