from shared import response_object


class BookListUseCase(object):
    def __init__(self, repo):
        self.repo = repo

    def execute(self, request_object):
        books = self.repo.list()
        return response_object.ResponseSuccess(books)
