import json


class BookEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            to_serialize = {
                "code": o.code,
                "title": o.title,
                "author": o.author,
                "year": o.year,
                "language": o.language,
                "is_available": o.is_available,
                "reader": o.reader,
            }
            return to_serialize
        except AttributeError:
            return super().default(o)
