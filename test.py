import broker
from tornado.testing import AsyncHTTPTestCase
import unittest
import json


class TestBroker(AsyncHTTPTestCase):
    def get_app(self):
        return broker.make_app()

    def test_healthcheck(self):
        response = self.fetch('/v2/healthcheck')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, b'ok')

    def test_login_method_check(self):
        response = self.fetch('/v2/login', method="POST",
                              body=json.dumps({"id": "12345678"}))
        self.assertEqual(response.code, 412)
        self.assertEqual(response.body.decode('utf8'), json.dumps(
            {"status": False, "data": "Expect json"}))
    
    def test_login_wrong_no_passwd(self):
        response = self.fetch('/v2/login', method="POST",headers={'Content-Type':'application/json'},
                              body=json.dumps({"id": "12345678"}))
        self.assertEqual(response.code, 400)
        self.assertEqual(response.body.decode('utf8'), json.dumps(
            {"status": False, "data": "wrong params"}))
    
    def test_login_wrong_wrong_id(self):
        response = self.fetch('/v2/login', method="POST",headers={'Content-Type':'application/json'},
                              body=json.dumps({"id": "1627405062","token":"5361554212512"}))
        self.assertEqual(response.code, 400)
        self.assertEqual(response.body.decode('utf8'), json.dumps(
            {"status": False, "data": "Authentication error"}))


if __name__ == "__main__":
    unittest.main()
