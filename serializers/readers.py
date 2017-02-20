import json


class ReaderEncoder(json.JSONEncoder):
    def default(self, o):
        try:

            reg_date = None
            if isinstance(o.reg_date, str):
                reg_date = o.reg_date
            else:
                reg_date = o.reg_date.isoformat()

            to_serialize = {
                'code': o.code,
                'full_name': o.full_name,
                'reg_date': reg_date
            }
            return to_serialize
        except AttributeError:
            return super().default(o)
