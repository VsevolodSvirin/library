import datetime
import uuid

from domains.reader import Reader


def test_book_model_init():
    code = uuid.uuid4()
    reader = Reader(code, full_name="VS", reg_date=datetime.date(2017, 2, 13))
    assert reader.code == code
    assert reader.full_name == "VS"
    assert reader.reg_date == datetime.date(2017, 2, 13)


def test_book_model_from_dict():
    code = uuid.uuid4()
    reader = Reader.from_dict(
        {
            "code": code,
            "full_name": "VS",
            "reg_date": datetime.date(2017, 2, 13)
        }
    )
    assert reader.code == code
    assert reader.full_name == "VS"
    assert reader.reg_date == datetime.date(2017, 2, 13)
