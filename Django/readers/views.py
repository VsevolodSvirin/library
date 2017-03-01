import copy
import json

from django.http import HttpResponse

from Django.django_shared.request_handlers import request_standartizer
from repo.DjangoORM.readers import DjangoORMReaderRepository
from serializers.readers import ReaderEncoder
from shared import errors
from shared import response_object as res
from use_cases.readers import ReaderAddUseCase, ReaderListUseCase, ReaderDetailsUseCase, ReaderDeleteUseCase, \
    ReaderUpdateUseCase
from use_cases.request_objects.readers import ReaderAddRequestObject, ReaderListRequestObject, \
    ReaderDetailsRequestObject, ReaderDeleteRequestObject, ReaderUpdateRequestObject

STATUS_CODES = {
    res.ResponseSuccess.SUCCESS: 200,
    errors.Error.RESOURCE_ERROR: 404,
    errors.Error.PARAMETERS_ERROR: 400,
    errors.Error.SYSTEM_ERROR: 500
}


@request_standartizer
def readers_list(request):
    if request.method == 'POST':
        status_codes = copy.deepcopy(STATUS_CODES)
        status_codes[res.ResponseSuccess.SUCCESS] = 201

        initial_data = request.POST
        request_object = ReaderAddRequestObject.from_dict(initial_data)

        repo = DjangoORMReaderRepository()
        use_case = ReaderAddUseCase(repo)

        response = use_case.execute(request_object)
        return HttpResponse(content=json.dumps(response.value, cls=ReaderEncoder), content_type='application/json',
                            status=status_codes[response.type])

    qrystr_params = {
        'filters': {},
    }

    for arg, values in request.GET.items():
        if arg.startswith('filter_'):
            qrystr_params['filters'][arg.replace('filter_', '')] = values

    request_object = ReaderListRequestObject.from_dict(qrystr_params)

    repo = DjangoORMReaderRepository()
    use_case = ReaderListUseCase(repo)

    response = use_case.execute(request_object)

    return HttpResponse(json.dumps(response.value, cls=ReaderEncoder), content_type='application/json',
                        status=STATUS_CODES[response.type])


@request_standartizer
def reader_detail(request, pk):
    if request.method == 'DELETE':
        status_codes = copy.deepcopy(STATUS_CODES)
        status_codes[res.ResponseSuccess.SUCCESS] = 204

        request_object = ReaderDeleteRequestObject.from_dict({'pk': pk})

        repo = DjangoORMReaderRepository()
        use_case = ReaderDeleteUseCase(repo)

        response = use_case.execute(request_object)
        return HttpResponse(content=json.dumps(response.value, cls=ReaderEncoder), content_type='application/json',
                            status=status_codes[response.type])

    if request.method == 'PATCH':
        patch_data = request.POST
        repo = DjangoORMReaderRepository()
        request_object = ReaderUpdateRequestObject.from_dict(
            {'pk': pk, 'patch': patch_data}
        )
        use_case = ReaderUpdateUseCase(repo)

        response = use_case.execute(request_object)
        return HttpResponse(content=json.dumps(response.value, cls=ReaderEncoder), content_type='application/json',
                            status=STATUS_CODES[response.type])

    request_object = ReaderDetailsRequestObject.from_dict({'pk': pk})

    repo = DjangoORMReaderRepository()
    use_case = ReaderDetailsUseCase(repo)

    response = use_case.execute(request_object)

    return HttpResponse(json.dumps(response.value, cls=ReaderEncoder), content_type='application/json',
                        status=STATUS_CODES[response.type])
