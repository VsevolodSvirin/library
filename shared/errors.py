class Error(object):
    RESOURCE_ERROR = 'ResourceError'
    PARAMETERS_ERROR = 'ParametersError'
    SYSTEM_ERROR = 'SystemError'

    def __init__(self, type_, message):
        self.type = type_
        self.message = self._format_message(message)

    def _format_message(self, msg):
        if isinstance(msg, Exception):
            return '{}: {}'.format(msg.__class__.__name__, '{}'.format(msg))
        return msg

    @property
    def value(self):
        return {'type': self.type, 'message': self.message}

    @classmethod
    def build_resource_error(cls):
        message = {'resource error': ['page not found :(']}
        return cls(cls.RESOURCE_ERROR, message)

    @classmethod
    def build_system_error(cls, exc):
        message = {'system error': [arg for arg in exc.args]}
        return cls(cls.SYSTEM_ERROR, message)

    @classmethod
    def build_parameters_error(cls, message):
        return cls(cls.PARAMETERS_ERROR, message)

    @classmethod
    def build_from_invalid_request_object(cls, invalid_request_object):
        message = invalid_request_object.errors
        return cls.build_parameters_error(message)
