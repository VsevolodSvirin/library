from shared import errors
from shared import response_object


class UseCase(object):
    def execute(self, request_object):
        if not request_object:
            error = errors.Error.build_from_invalid_request_object(request_object)
            return response_object.ResponseFailure.from_error(error)
        try:
            return self.process_request(request_object)
        except Exception as exc:
            error = errors.Error.build_system_error(exc)
            return response_object.ResponseFailure.from_error(error)

    def process_request(self, request_object):
        raise NotImplementedError(
            'process_request() not implemented by UseCase class')
