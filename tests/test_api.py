import json
import threading
import unittest
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer

from kim_holiday.api import DraftAPIHandler


class DraftAPITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), DraftAPIHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.thread.join()
        cls.server.server_close()

    def request(self, method, path, body=None):
        connection = HTTPConnection(*self.server.server_address)
        encoded = None if body is None else json.dumps(body)
        headers = {"Content-Type": "application/json"} if encoded else {}
        connection.request(method, path, encoded, headers)
        response = connection.getresponse()
        payload = json.loads(response.read())
        connection.close()
        return response.status, payload

    def test_health(self):
        status, payload = self.request("GET", "/health")
        self.assertEqual((status, payload), (200, {"status": "ok"}))

    def test_draft_is_approval_gated(self):
        status, payload = self.request("POST", "/draft", {"topic": "questions to ask before planning"})
        self.assertEqual(status, 200)
        self.assertTrue(payload["approval_required"])
        self.assertEqual(payload["status"], "draft")
        self.assertIn("Kirim DM", payload["caption"])

    def test_invalid_request_is_a_clear_400(self):
        status, payload = self.request("POST", "/draft", {"topic": 123})
        self.assertEqual(status, 400)
        self.assertEqual(payload["error"], "invalid_request")
