from shared import errors
from shared import response_object, use_case


class ReaderListUseCase(use_case.UseCase):
    def __init__(self, repo):
        self.repo = repo

    def process_request(self, request_object):
        domain_reader = self.repo.list(filters=request_object.filters)
        return response_object.ResponseSuccess(domain_reader)


class ReaderAddUseCase(use_case.UseCase):
    def __init__(self, repo):
        self.repo = repo

    def process_request(self, request_object):
        reader = self.repo.from_dict(request_object.init_values)
        return response_object.ResponseSuccess(reader)


class ReaderDetailsUseCase(use_case.UseCase):
    def __init__(self, repo):
        self.repo = repo

    def process_request(self, request_object):
        resp = self.repo.details(pk=request_object.pk)
        if isinstance(resp, errors.Error):
            return response_object.ResponseFailure.from_error(resp)
        else:
            return response_object.ResponseSuccess(resp)
