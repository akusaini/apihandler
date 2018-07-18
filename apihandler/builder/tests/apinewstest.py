import unittest
from apihandler.builder.extras.explorer import HttpJsonClient
import urllib3
import json
from apihandler.apihandler.settings import NEWS_API_TOKEN

http = urllib3.PoolManager()
domain = "http://18.220.145.52:8001/v1/news"


class TestNewsApi(unittest.TestCase):
	def test_method_allowed(self):
		# Filtering first non allowed methods.
		for method in ['POST', 'PUT', 'PATCH']:
			response = http.request(method, domain)
			self.assertEqual(response.status, 405)
			response_data = json.loads(response.data.decode('utf-8'))
			self.assertEqual(response_data.get('success'), False)

	def test_query_params(self):
		# Hitting without any query params
		url = domain
		response = http.request('GET', '%s?apiKey=%s' % (url, NEWS_API_TOKEN) )
		self.assertEqual(response.status, 400)
		response_data = json.loads(response.data.decode('utf-8'))
		self.assertEqual(response_data.get('success'), False)
		self.assertEqual(response_data.get('message').lower(), "Bad request.".lower())


		# Hitting with partial query params
		response = http.request('GET', '%s?country=us&apiKey=%s' % (url, NEWS_API_TOKEN))
		self.assertEqual(response.status, 400)
		response_data = json.loads(response.data.decode('utf-8'))
		self.assertEqual(response_data.get('success'), False)
		self.assertEqual(response_data.get('message').lower(), "Bad request.".lower())

		# Hitting with all required query params
		response = http.request('GET', '%s?country=us&category=Business&apiKey=%s' % (url, NEWS_API_TOKEN))
		self.assertEqual(response.status, 200)
		response_data = json.loads(response.data.decode('utf-8'))
		self.assertEqual(response_data.get('success'), True)


if __name__ == '__main__':
	unittest.main()
