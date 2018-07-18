from urllib.request import Request, build_opener, HTTPError, URLError
import json
import logging

logger = logging.getLogger (__name__)

class BaseHttpClient (object):
    def __init__ (self, address, headers = {}):
        self.address = address
        if not isinstance (headers, dict):
            raise TypeError ("headers must be dictionary")

        self.headers = headers
        self._header_appender ()

    def _header_appender (self):
        pass

    def _response_parser (self, code, fp):
        raise NotImplementedError ()

    def _execute (self, request):
        opener = build_opener()
        try:
            fp = opener.open (request)
        except HTTPError as e:
            logger.warning (e.read())
            return e.code, None
        except URLError as e:
            return 0, None

        return self._response_parser (200, fp)

    def get (self):
        request = Request (url=self.address, headers=self.headers)
        return self._execute (request)

    def post (self, data):
        request = Request (url=self.address, data=json.dumps (data).encode("utf-8"), headers=self.headers)
        return self._execute (request)

class HttpClient (BaseHttpClient):

    def _response_parser (self, code, fp):
        return code, fp.read ()

class HttpJsonClient (BaseHttpClient):

    def _response_parser (self, code, fp):
        content = fp.read().decode('utf-8')
        logger.debug ("Response from server: %s", content)
        return code, json.loads (content)

    def _header_appender (self):
        self.headers["Content-Type"] = "application/json"

if __name__ == "__main__":
    import unittest

    class TestHttpClient (unittest.TestCase):

        def test_typeerror (self):
            try:
                http = HttpJsonClient ("https://jsonplaceholder.typicode.com/posts/1", [])
                return self.fail ("List accepted as dict")
            except TypeError:
                return

        def test_get_404 (self):
            http = HttpJsonClient ("https://httpbin.org/status/404")
            code, resp = http.get ()
            if code != 404:
                self.fail ("404 Didn't came up!")

        def test_get_200 (self):
            http = HttpJsonClient ("https://httpbin.org/ip")
            code, resp = http.get ()
            assert code == 200
            assert resp.has_key ("origin")

        def test_post_200 (self):
            http = HttpJsonClient ("https://httpbin.org/post")
            code, resp = http.post ({"test": "val"})
            assert code == 200
            assert resp.has_key ("data")
            data = json.loads (resp["data"])
            assert data.get ("test", "") == "val"

        def test_nojson_get_200 (self):
            http = HttpClient ("https://httpbin.org/ip")
            code, resp = http.get ()
            assert code == 200
            assert isinstance (resp, str)

    unittest.main()
