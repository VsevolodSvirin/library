from shared import errors


class InvalidRequestObject(object):

    def __init__(self):
        self.errors = []
        if self.has_errors():
            self.error = errors.Error.build_from_invalid_request_object(self)

    def add_error(self, parameter, message):
        self.errors.append({'parameter': parameter, 'message': message})
        self.error = errors.Error.build_from_invalid_request_object(self)

    def has_errors(self):
        return len(self.errors) > 0

    def __nonzero__(self):
        return False

    __bool__ = __nonzero__


class ValidRequestObject(object):

    @classmethod
    def from_dict(cls, adict):
        raise NotImplementedError

    def __nonzero__(self):
        return True

    __bool__ = __nonzero__