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
        reader = self.repo.create(reader=request_object.init_values)
        return response_object.ResponseSuccess(reader)
