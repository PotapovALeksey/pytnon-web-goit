import mimetypes
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from client.socket_client import send_record
from config.http_server_config import HTTP_HOST, HTTP_PORT

FRONT_DIR = "front"


class SimpleHttpServer(BaseHTTPRequestHandler):
    def do_GET(self):
        request = urllib.parse.urlparse(self.path)

        match request.path:
            case "/":
                self.send_html("/index.html")
            case "/message":
                self.send_html("/message.html")
            case _:
                path = Path(f"{FRONT_DIR}{request.path}")

                if path.exists():
                    self.send_static(request.path)
                else:
                    self.send_html("/error.html", 404)

    def do_POST(self):
        data = self.rfile.read(int(self.headers["Content-Length"]))

        send_record(data)

        self.send_response(302)
        self.send_header("Location", "/")
        self.end_headers()

    def read_file(self, file_name):
        with open(f"{FRONT_DIR}{file_name}", "rb") as file:
            return file.read()

    def send_html(self, file_name, status=200):
        self.send_response(status)
        self.end_headers()
        self.wfile.write(self.read_file(file_name))

    def send_static(self, file_name, status=200):
        self.send_response(status)

        mt = mimetypes.guess_type(file_name)

        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", "text/plain")

        self.end_headers()
        self.wfile.write(self.read_file(file_name))


http_server = HTTPServer((HTTP_HOST, HTTP_PORT), SimpleHttpServer)
