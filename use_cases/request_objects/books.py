import collections
import datetime

from voluptuous import Schema, Required, All, Length, Range, REMOVE_EXTRA, MultipleInvalid, Any, Datetime

from domains.book import Book
from shared.request_object import ValidRequestObject, InvalidRequestObject


def check_if_int(param):
    try:
        int(param)
        return True
    except Exception:
        return False


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


class BookDetailsRequestObject(ValidRequestObject):
    def __init__(self, pk):
        self.pk = pk

    @classmethod
    def from_dict(cls, adict):
        invalid_req = InvalidRequestObject()

        if not bool(adict):
            invalid_req.add_error('request dictionary', 'is empty, has to pass primary key')
        elif 'pk' not in adict.keys():
            invalid_req.add_error('primary key', 'has to pass primary key')
        elif not isinstance(adict.get('pk'), int) and not check_if_int(adict.get('pk')):
            invalid_req.add_error('primary key', 'has to be integer')

        if invalid_req.has_errors():
            return invalid_req

        return BookDetailsRequestObject(pk=int(adict.get('pk')))


class BookDeleteRequestObject(ValidRequestObject):
    def __init__(self, pk):
        self.pk = pk

    @classmethod
    def from_dict(cls, adict):
        invalid_req = InvalidRequestObject()

        if not bool(adict):
            invalid_req.add_error('request dictionary', 'is empty, has to pass primary key')
        elif 'pk' not in adict.keys():
            invalid_req.add_error('primary key', 'has to pass primary key')
        elif not isinstance(adict.get('pk'), int) and not check_if_int(adict.get('pk')):
            invalid_req.add_error('primary key', 'has to be integer')

        if invalid_req.has_errors():
            return invalid_req

        return BookDeleteRequestObject(pk=int(adict.get('pk')))