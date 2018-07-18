from .error import Error

class BaseException(Exception):
    """
    Base class for custom exceptions.
    Subclasses should provide `status_code`, `message` and `errors` properties.
    """
    status_code = 500
    message = 'A server error occurred.'
    errors = []

    def __init__(self, message=None, status_code=500, errors=()):
        self.status_code = status_code
        self.errors = errors
        if message:
            self.message = message

    def __str__(self):
        return "Error({}): {}".format(self.status_code, self.message)


class NotAuthenticated(BaseException):
    message = 'Authentication required.'

    def __init__(self, message=None, errors=()):
        message = message or self.message
        super(NotAuthenticated, self).__init__(message=message, status_code=401, errors=errors)


class AttributeError(BaseException):
    message = 'Attributee hai  required.'

    def __init__(self, message=None, errors=()):
        message = message or self.message
        super(AttributeError, self).__init__(message=message, status_code=401, errors=errors)


class Unauthorized(BaseException):
    message = "Not authorized to perform this action."

    def __init__(self, message, error):
        message = message or self.message
        super(Unauthorized, self).__init__(message, status_code=403, errors=error)


class NotFound(BaseException):
    message = 'Resource not found.'

    def __init__(self, message=None, errors=()):
        message = message or self.message
        super(NotFound, self).__init__(message=message, status_code=404, errors=errors)


class BadRequest(BaseException):
    message = 'Bad request.'

    def __init__(self, message=None, errors=()):
        message = message or self.message
        super(BadRequest, self).__init__(message=message, status_code=400, errors=errors)


class MethodNotAllowed(BaseException):
    message = 'Method not allowed.'

    def __init__(self, message=None, errors=()):
        message = message or self.message
        super(MethodNotAllowed, self).__init__(message=message, status_code=405, errors=errors)


class ExceptionBuilder(object):
    def __init__(self, exc_cls=BaseException):
        self._exc_cls = exc_cls
        self._errors = []
        self._message = ''
        self._code = None

    def error(self, error_constant, *fields, message=None):
        self._errors.append(Error(error_constant, *fields, message=message).formated)
        return self

    def message(self, msg):
        self._message = msg
        return self

    def status_code(self, code):
        self._code = code
        return self

    def throw(self):
        if self._code:
            raise self._exc_cls(errors=self._errors, message=self._message, status_code=self._code )
        else:
            raise self._exc_cls(errors=self._errors, message=self._message)

