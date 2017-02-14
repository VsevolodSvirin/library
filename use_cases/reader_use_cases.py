from shared import response_object


class ReaderListUseCase(object):
    def __init__(self, repo):
        self.repo = repo

    def execute(self, request_object):
        readers = self.repo.list()
        return response_object.ResponseSuccess(readers)
