import json


class ReaderEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            to_serialize = {
                "code": o.code,
                "full_name": o.full_name,
                "reg_date": o.reg_date.isoformat()
            }
            return to_serialize
        except AttributeError:
            return super().default(o)
