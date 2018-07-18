import json
from django.http import HttpResponse
from builder.common.error_handler.exceptions import BaseException
from builder.common.error_handler.error import Error
from builder.constants.errorcodes import ErrorCode


class Response(object):
    def __init__(self, success=True, data=None, errors=(), message="", status_code=200, headers=None, mimetype=None):
        self.success = success
        self.data = data
        self.errors = errors
        self.message = message

        self.status_code = status_code


def response_builder (response_obj):
    data = {
        'data': response_obj.data,
        'error': response_obj.errors,
        'success': response_obj.success,
        'message': response_obj.message
    }
    response = HttpResponse(json.dumps(data), "application/json", status=response_obj.status_code)
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response['Access-Control-Allow-Headers'] = 'Content-Type, X-Auth'
    response['Access-Control-Max-Age'] = '1000'
    return response


def unauthorized ():
    response = response_builder()
    return response


def jsonify (*dargs, **kwdargs):
    def _jsonify (func):
        """
        A decorator that takes a view response and turns it
        into json. If a callback is added through GET or POST
        the response is JSONP.
        """
        def decorator (request, *args, **kwargs):
            if request.method == "OPTIONS":
                # Lets honour CORS first
                response = HttpResponse (status = 204)
                response['Access-Control-Allow-Origin'] = '*'
                response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
                response['Access-Control-Allow-Headers'] = 'Content-Type, X-Auth, X-Auth-Agency, X-App-Choice'
                return response

            request.data = {}
            if request.content_type == "application/json":
                if request.method in ["POST", "PUT", "PATCH"]:
                    body = json.loads (request.body.decode('utf-8'))
                    request.data = body

            require_auth = kwdargs.get ("auth", True)

            if require_auth:
                if not request.user.is_authenticated:
                    return unauthorized()


            try:
                response_returned, message = func(request, *args, **kwargs)
                response_obj = Response(success=True, status_code=200, data=response_returned, errors=[], message=message)
            except BaseException as be:
                #    Custom exceptions are to be handled here.
                import traceback
                print(traceback.format_exc())
                response_obj = Response(success=False, status_code=be.status_code, message=be.message, errors=be.errors)
            except Exception as e:
                import traceback
                print(traceback.format_exc())
                response_obj = Response(success=False, status_code=500,
                                        errors=[Error(ErrorCode.NON_STANDARD_ERROR, message=str(e)).formated])

            return response_builder (response_obj)

        return decorator

    if len (kwdargs.keys()) == 0:
        return _jsonify(dargs[0])

    return _jsonify
