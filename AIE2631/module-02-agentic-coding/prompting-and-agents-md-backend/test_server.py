import json
import threading
import unittest
from http.client import HTTPConnection

from server import Library, LibraryRequestHandler, create_server


class LibraryServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        LibraryRequestHandler.library = Library()
        cls.server = create_server(port=0)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.port = cls.server.server_address[1]

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def request(self, method, path, payload=None):
        connection = HTTPConnection("127.0.0.1", self.port)
        body = json.dumps(payload) if payload is not None else None
        headers = {"Content-Type": "application/json"} if body else {}
        connection.request(method, path, body=body, headers=headers)
        response = connection.getresponse()
        result = response.status, json.loads(response.read())
        connection.close()
        return result

    def test_add_and_list_books(self):
        status, created = self.request("POST", "/api/books", {"title": "Dune"})
        self.assertEqual(status, 201)
        self.assertEqual(created["title"], "Dune")

        status, books = self.request("GET", "/api/books")
        self.assertEqual(status, 200)
        self.assertIn(created, books)

    def test_rejects_an_empty_title(self):
        status, response = self.request("POST", "/api/books", {"title": "  "})
        self.assertEqual(status, 400)
        self.assertEqual(response["error"], "Title is required")


if __name__ == "__main__":
    unittest.main()
