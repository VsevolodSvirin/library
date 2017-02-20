import collections
import datetime

from voluptuous import Schema, Required, Any, Match, REMOVE_EXTRA, All, Range, Length, MultipleInvalid, Datetime

from shared.request_object import ValidRequestObject, InvalidRequestObject


class ReaderListRequestObject(ValidRequestObject):
    def __init__(self, filters=None):
        self.filters = filters

    @classmethod
    def from_dict(cls, adict):
        invalid_req = InvalidRequestObject()

        if 'filters' in adict and not isinstance(adict['filters'], collections.Mapping):
            invalid_req.add_error('filters', 'Is not iterable')

        if invalid_req.has_errors():
            return invalid_req

        return ReaderListRequestObject(filters=adict.get('filters', None))


class ReaderAddRequestObject(ValidRequestObject):
    def __init__(self, init_values):
        self.init_values = init_values

    @classmethod
    def from_dict(cls, adict):
        invalid_req = InvalidRequestObject()

        schema = Schema({
            Required('full_name'): All(str, Length(min=1, max=128)),
            Required('reg_date'):
                Any(All(datetime.date, Range(min=datetime.date(1000, 1, 1), max=datetime.date.today())),
                    Datetime('%Y-%m-%d')),
        }, extra=REMOVE_EXTRA)

        try:
            values = schema(adict)
        except MultipleInvalid as exc:
            for error in exc.errors:
                try:
                    invalid_req.add_error(parameter='.'.join([p for p in error.path]),
                                          message=error.error_message)
                except TypeError as e:
                    invalid_req.add_error(parameter='.'.join([p.schema for p in error.path]),
                                          message=error.error_message)

        if invalid_req.has_errors():
            return invalid_req

        return ReaderAddRequestObject(init_values=values)
