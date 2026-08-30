import json
import datetime


class McpLogger:
    def __init__(self, path="mcp_interactions.log"):
        self.path = path

    def log_request(self, server_name, request):
        self._write("REQUEST", server_name, request)

    def log_response(self, server_name, response):
        self._write("RESPONSE", server_name, response)

    def _write(self, kind, server_name, payload):
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "type": kind,
            "server": server_name,
            "payload": payload,
        }
        with open(self.path, "a") as f:
            f.write(json.dumps(entry) + "\n")
        print(f"[{kind}] {server_name}: {json.dumps(payload)}")