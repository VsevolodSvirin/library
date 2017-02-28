from shared import errors
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


class BookDetailsUseCase(use_case.UseCase):
    def __init__(self, repo):
        self.repo = repo

    def process_request(self, request_object):
        resp = self.repo.details(pk=request_object.pk)
        if isinstance(resp, errors.Error):
            return response_object.ResponseFailure.from_error(resp)
        else:
            return response_object.ResponseSuccess(resp)


class BookDeleteUseCase(use_case.UseCase):
    def __init__(self, repo):
        self.repo = repo

    def process_request(self, request_object):
        resp = self.repo.delete(pk=request_object.pk)
        if isinstance(resp, errors.Error):
            return response_object.ResponseFailure.from_error(resp)
        else:
            return response_object.ResponseSuccess()


class BookUpdateUseCase(use_case.UseCase):
    def __init__(self, repo):
        self.repo = repo

    def process_request(self, request_object):
        resp = self.repo.update(pk=request_object.pk, patch=request_object.patch)
        if isinstance(resp, errors.Error):
            return response_object.ResponseFailure.from_error(resp)
        else:
            return response_object.ResponseSuccess(resp)


class BookGiveUseCase(use_case.UseCase):
    def __init__(self, repo, reader):
        self.repo = repo
        self.reader = reader

    def process_request(self, request_object):
        resp = self.repo.give(pk=request_object.pk, reader=request_object.reader)
        if isinstance(resp, errors.Error):
            return response_object.ResponseFailure.from_error(resp)
        else:
            return response_object.ResponseSuccess(resp)


class BookReturnUseCase(use_case.UseCase):
    def __init__(self, repo):
        self.repo = repo

    def process_request(self, request_object):
        resp = self.repo.give(pk=request_object.pk)
        if isinstance(resp, errors.Error):
            return response_object.ResponseFailure.from_error(resp)
        else:
            return response_object.ResponseSuccess(resp)
