import json
from flask import Blueprint, request, Response

from repo.Flask_Alchemy.books import FlaskAlchemyBookRepository
from shared import errors
from shared import response_object as res
from use_cases.books import BookListUseCase, BookDetailsUseCase
from serializers.books import BookEncoder
from use_cases.request_objects.books import BookListRequestObject, BookDetailsRequestObject

blueprint = Blueprint('book', __name__)

STATUS_CODES = {
    res.ResponseSuccess.SUCCESS: 200,
    errors.Error.RESOURCE_ERROR: 404,
    errors.Error.PARAMETERS_ERROR: 400,
    errors.Error.SYSTEM_ERROR: 500
}


@blueprint.route('/books', methods=['GET'])
def books():
    qrystr_params = {
        'filters': {},
    }

    for arg, values in request.args.items():
        if arg.startswith('filter_'):
            qrystr_params['filters'][arg.replace('filter_', '')] = values

    request_object = BookListRequestObject.from_dict(qrystr_params)

    repo = FlaskAlchemyBookRepository()
    use_case = BookListUseCase(repo)

    response = use_case.execute(request_object)

    return Response(json.dumps(response.value, cls=BookEncoder),
                    mimetype='application/json',
                    status=STATUS_CODES[response.type])


@blueprint.route('/books/<pk>/', methods=['GET'])
def book_details(pk):
    request_object = BookDetailsRequestObject.from_dict({'pk': pk})

    repo = FlaskAlchemyBookRepository()
    use_case = BookDetailsUseCase(repo)

    response = use_case.execute(request_object)

    return Response(json.dumps(response.value, cls=BookEncoder), content_type='application/json',
                        status=STATUS_CODES[response.type])
