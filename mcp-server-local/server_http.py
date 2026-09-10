import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from protocol import process_request

PORT = int(os.environ.get("PORT", 8081))


class McpHttpHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        try:
            request = json.loads(body)
        except json.JSONDecodeError:
            response = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Parse error"}}
            self._write(response, status=400)
            return

        if "id" not in request:
            self._write(None, status=204)
            return

        response = process_request(request)
        self._write(response, status=200)

    def _write(self, payload, status):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        if payload is not None:
            self.wfile.write(json.dumps(payload).encode("utf-8"))

    def log_message(self, format, *args):
        pass


def main():
    server = HTTPServer(("0.0.0.0", PORT), McpHttpHandler)
    print(f"MCP HTTP server escuchando en el puerto {PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()