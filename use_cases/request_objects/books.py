import collections
import datetime

from voluptuous import Schema, Required, All, Length, Range, REMOVE_EXTRA, MultipleInvalid, Any, Datetime

from domains.book import Book
from shared.request_object import ValidRequestObject, InvalidRequestObject


class BookListRequestObject(ValidRequestObject):
    def __init__(self, filters=None):
        self.filters = filters

    @classmethod
    def from_dict(cls, adict):
        invalid_req = InvalidRequestObject()

        if 'filters' in adict:
            if not isinstance(adict['filters'], collections.Mapping):
                invalid_req.add_error('filters', 'Is not iterable')
            else:
                good_operators = ('eq',)
                for key in adict['filters'].keys():
                    try:
                        field, operator = key.split('__')
                        if field == 'year':
                            if operator not in ('eq', 'gt', 'lt'):
                                invalid_req.add_error(field, 'no such comparison operator %s' % operator)
                        else:
                            if operator not in good_operators:
                                invalid_req.add_error(field, 'no such comparison operator %s' % operator)
                        if field not in Book.__slots__:
                            invalid_req.add_error(field, 'no such field')
                    except ValueError:
                        invalid_req.add_error(key, 'invalid filter')

        if invalid_req.has_errors():
            return invalid_req

        return BookListRequestObject(filters=adict.get('filters', None))


class BookAddRequestObject(ValidRequestObject):
    def __init__(self, init_values=None):
        self.init_values = init_values

    @classmethod
    def from_dict(cls, adict):
        invalid_req = InvalidRequestObject()

        schema = Schema({
            Required('title'): All(str, Length(min=1, max=128)),
            Required('author'): All(str, Length(min=1, max=128)),
            Required('year'):
                Any(Datetime('%Y'), All(int, Range(min=1000, max=datetime.datetime.now().year))),
            Required('language'): All(str, Length(min=1, max=128)),
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

        return BookAddRequestObject(init_values=values)
