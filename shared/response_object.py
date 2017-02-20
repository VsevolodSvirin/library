class ResponseSuccess(object):
    SUCCESS = 'Success'

    def __init__(self, value=None):
        self.type = self.SUCCESS
        self.value = value

    def __nonzero__(self):
        return True

    __bool__ = __nonzero__


class ResponseFailure(object):
    def __init__(self, error):
        self.type = error.type
        self.value = error.message

    @classmethod
    def from_error(cls, error):
        return cls(error)

    def __nonzero__(self):
        return False

    __bool__ = __nonzero__