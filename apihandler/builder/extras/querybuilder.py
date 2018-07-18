from builder.extras.explorer import HttpJsonClient
from django.core.cache import cache
from django.conf import settings


class QueryBuilder(object):
	def __init__(self, domain, query_params={}, headers={}):
		self.domain = domain
		self.query_params = query_params
		self.headers = headers
		self.final_url = ''
		self.payload = {}

	def build(self):
		query_str = None
		if len(self.query_params.items()) > 0:
			# Query params will be in sorted order to preserve the order for making keys for caching.
			query_str = '&'.join("{key}={value}".format(key=key, value=val) for (key, val) in self.query_params.items())
		self.final_url = "{domain}?{query_str}".format(domain=self.domain, query_str=query_str) if query_str else self.domain
		return self

	def get(self, cache_ttl=0):
		url = '%s&apiKey=%s' % (self.final_url, settings.NEWS_API_TOKEN)
		cached_response = cache.get(url.lower())
		if cached_response is not None:
			print("Returning the response from the cache")
			return cached_response

		print("GET : %s" % url)
		http = HttpJsonClient(url)
		code, result = http.get()
		if 200 <= code < 300:
			# Cache the result for the specified time.
			if cache_ttl > 0:
				cache.set(url.lower(), result, timeout=10*60)
			return result

	def post(self):
		http = HttpJsonClient(self.final_url, headers=self.headers)
		code, result = http.post(self.payload)
		print("POST : %s" % self.final_url)
		if 200 <= code < 300:
			return result
