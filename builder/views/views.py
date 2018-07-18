from builder.common.error_handler.exceptions import ExceptionBuilder, MethodNotAllowed
from builder.constants.errorcodes import HttpErrorCode
from builder.extras.decorators import jsonify


@jsonify(auth=False)
def test(request):
	if request.method != 'GET':
		eb = ExceptionBuilder(exc_cls=MethodNotAllowed).error(HttpErrorCode.METHOD_NOT_ALLOWED,
															  message="Only Post method is allowed")
		eb.throw()
	data = {'name': 'Akash saini'}
	return data, "User info displayed."
