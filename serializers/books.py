import json

from serializers.readers import ReaderEncoder


class BookEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            reader = json.dumps(o.reader, cls=ReaderEncoder)
            to_serialize = {
                'code': o.code,
                'title': o.title,
                'author': o.author,
                'year': o.year,
                'language': o.language,
                'is_available': o.is_available,
                'reader': reader,
            }
            return to_serialize
        except AttributeError:
            return super().default(self, o)

