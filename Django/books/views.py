import copy
import json

from django.http import HttpResponse

from repo.DjangoORM.books import DjangoORMBookRepository
from serializers.books import BookEncoder
from shared import errors
from shared import response_object as res
from use_cases.books import BookAddUseCase, BookListUseCase
from use_cases.request_objects.books import BookAddRequestObject, BookListRequestObject

STATUS_CODES = {
    res.ResponseSuccess.SUCCESS: 200,
    errors.Error.RESOURCE_ERROR: 404,
    errors.Error.PARAMETERS_ERROR: 400,
    errors.Error.SYSTEM_ERROR: 500
}


def books_list(request):
    if request.method == 'POST':
        status_codes = copy.deepcopy(STATUS_CODES)
        status_codes[res.ResponseSuccess.SUCCESS] = 201

        initial_data = request.POST
        request_object = BookAddRequestObject.from_dict(initial_data)

        repo = DjangoORMBookRepository()
        use_case = BookAddUseCase(repo)

        response = use_case.execute(request_object)
        return HttpResponse(content=json.dumps(response.value, cls=BookEncoder), content_type='application/json',
                            status=status_codes[response.type])

    qrystr_params = {
        'filters': {},
    }

    for arg, values in request.GET.items():
        if arg.startswith('filter_'):
            qrystr_params['filters'][arg.replace('filter_', '')] = values

    request_object = BookListRequestObject.from_dict(qrystr_params)

    repo = DjangoORMBookRepository()
    use_case = BookListUseCase(repo)

    response = use_case.execute(request_object)

    return HttpResponse(json.dumps(response.value, cls=BookEncoder), content_type='application/json',
                        status=STATUS_CODES[response.type])
