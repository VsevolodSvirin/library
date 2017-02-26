from shared import response_object, use_case


class BookListUseCase(use_case.UseCase):
    def __init__(self, repo):
        self.repo = repo

    def process_request(self, request_object):
        domain_book = self.repo.list(filters=request_object.filters)
        return response_object.ResponseSuccess(domain_book)


class BookAddUseCase(use_case.UseCase):
    def __init__(self, repo):
        self.repo = repo

    def process_request(self, request_object):
        book = self.repo.from_dict(request_object.init_values)
        return response_object.ResponseSuccess(book)
