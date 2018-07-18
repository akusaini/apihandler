from builder.common.error_handler.exceptions import ExceptionBuilder, MethodNotAllowed, BadRequest
from builder.constants.errorcodes import HttpErrorCode
from builder.extras.decorators import jsonify
from builder.extras.querybuilder import QueryBuilder
import re


@jsonify(auth=False)
def fetch_news(request):
	if request.method != 'GET':
		eb = ExceptionBuilder(exc_cls=MethodNotAllowed).error(HttpErrorCode.METHOD_NOT_ALLOWED, message="Only Get method is allowed.")
		eb.throw()

	error_fields = []
	query_criteria = {}
	filterkey = request.GET.get('filterKey', None)
	for query_key in ['country', 'category']:
		param = request.GET.get(query_key, None)
		if not param:
			error_fields.append(query_key)
		else:
			query_criteria[query_key] = param

	if len(error_fields) > 0:
		error_message = "Given fields are not present. Hence aborting"
		eb = ExceptionBuilder(exc_cls=BadRequest).error(HttpErrorCode.BAD_REQUEST, error_fields, message=error_message)
		eb.throw()

	data = QueryBuilder("https://newsapi.org/v2/top-headlines", query_criteria, {}).build().get(cache_ttl=2000)

	filterable_data = data.get('articles', [])

	filtered_articles = filterable_data
	if filterkey:
		filtered_articles = list(filter(lambda article: re.search(r'\b' + filterkey + '\W', str(article)) is not None, filterable_data))

	news = []

	for article in filtered_articles:
		news.append({
			'title': article.get('title', ''),
			'description': str(article.get('description', ''))[:100],
			'source': article.get('source', {}).get('name', "Unknown")})

	response_data = {
		'category': query_criteria.get('category'),
		'country': query_criteria.get('country'),
		'filterKey': filterkey,
		'news': news
	}
	return response_data, "News fetched successfully"
