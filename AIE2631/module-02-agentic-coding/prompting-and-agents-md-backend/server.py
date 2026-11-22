import argparse
import json
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Lock
from urllib.parse import urlparse


APP_DIRECTORY = Path(__file__).resolve().parent


class Library:
    def __init__(self):
        self._books = []
        self._next_id = 1
        self._lock = Lock()

    def all(self):
        with self._lock:
            return [book.copy() for book in self._books]

    def add(self, title):
        with self._lock:
            book = {"id": self._next_id, "title": title}
            self._books.append(book)
            self._next_id += 1
            return book.copy()


class LibraryRequestHandler(SimpleHTTPRequestHandler):
    library = Library()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(APP_DIRECTORY), **kwargs)

    def do_GET(self):
        if urlparse(self.path).path == "/api/books":
            self._send_json(self.library.all())
            return

        super().do_GET()

    def do_POST(self):
        if urlparse(self.path).path != "/api/books":
            self.send_error(HTTPStatus.NOT_FOUND)
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            if content_length > 10_000:
                self._send_json({"error": "Request body is too large"}, HTTPStatus.REQUEST_ENTITY_TOO_LARGE)
                return

            payload = json.loads(self.rfile.read(content_length) or b"{}")
            title = payload.get("title", "").strip()
        except (json.JSONDecodeError, AttributeError, TypeError):
            self._send_json({"error": "Send a JSON object with a title"}, HTTPStatus.BAD_REQUEST)
            return

        if not title:
            self._send_json({"error": "Title is required"}, HTTPStatus.BAD_REQUEST)
            return

        if len(title) > 200:
            self._send_json({"error": "Title must be 200 characters or fewer"}, HTTPStatus.BAD_REQUEST)
            return

        self._send_json(self.library.add(title), HTTPStatus.CREATED)

    def _send_json(self, payload, status=HTTPStatus.OK):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)


def create_server(host="127.0.0.1", port=8001):
    return ThreadingHTTPServer((host, port), LibraryRequestHandler)


def main():
    parser = argparse.ArgumentParser(description="Run My Little Library with its books API.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8001)
    args = parser.parse_args()

    server = create_server(args.host, args.port)
    print(f"My Little Library is running at http://{args.host}:{args.port}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
