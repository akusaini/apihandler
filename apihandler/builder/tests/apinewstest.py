import unittest
from apihandler.builder.extras.explorer import HttpJsonClient


class TestNewsApi(unittest.TestCase):
	def test_method_allowed(self):
		http = HttpJsonClient("http://18.220.145.52:8901/v1/news")
		code, result = http.post({})
		if code == 405:
			print(33)


if __name__ == '__main__':
	unittest.main()
