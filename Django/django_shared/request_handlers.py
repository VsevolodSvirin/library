import json


def request_standartizer(function):
    def wrapper(request, **kwargs):
        if request.body and not request.POST:
            tmp = request.body.decode('utf-8')
            try:
                request.POST = json.loads(tmp)
            except Exception:
                request.POST = json.loads(json.dumps(tmp))
        return function(request, **kwargs)
    return wrapper
