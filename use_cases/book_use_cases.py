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
        book_is_added = self.repo.add(book=request_object.book)
        return response_object.ResponseSuccess(book_is_added)
