from builder.constants.errorcodes import ErrorCode


class Error(object):
	def __init__(self, error_constant, *fields, message=None):
		self.error_constant = error_constant
		self.fields = tuple(fields)
		self.message = message if message else ErrorCode.NON_STANDARD_ERROR

	@property
	def formated(self):
		error_dict = {
			'error_code': self.error_constant,
			'message': self.message,
			'fields': self.fields
		}
		return error_dict