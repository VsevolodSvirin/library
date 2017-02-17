import copy
import json

from django.http import HttpResponse

from repo.DjangoORM.books import DjangoORMBookRepository
from serializers.books import BookEncoder
from shared import response_object as res
from use_cases.books import BookAddUseCase
from use_cases.request_objects.books import BookAddRequestObject

STATUS_CODES = {
    res.ResponseSuccess.SUCCESS: 200,
    res.ResponseFailure.RESOURCE_ERROR: 404,
    res.ResponseFailure.PARAMETERS_ERROR: 400,
    res.ResponseFailure.SYSTEM_ERROR: 500
}


def books_add(request):
    status_codes = copy.deepcopy(STATUS_CODES)
    status_codes[res.ResponseSuccess.SUCCESS] = 201

    initial_data = request.POST
    request_object = BookAddRequestObject.from_dict(initial_data)

    repo = DjangoORMBookRepository()
    use_case = BookAddUseCase(repo)

    response = use_case.execute(request_object)
    return HttpResponse(content=json.dumps(response.value, cls=BookEncoder), content_type='application/json',
                        status=status_codes[response.type])
