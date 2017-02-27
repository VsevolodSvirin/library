import json


def request_standartizer(function):
    def wrapper(request):
        if request.body and not request.POST:
            tmp = request.body.decode('utf-8')
            request.POST = json.loads(tmp)
        return function(request)
    return wrapper
