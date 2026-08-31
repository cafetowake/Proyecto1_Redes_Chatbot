import json
import subprocess
import itertools


class McpClient:
    def __init__(self, name, command, logger=None):
        self.name = name
        self.command = command
        self.logger = logger
        self.process = None
        self._id_counter = itertools.count(1)
        self.tools = []

    def start(self):
        self.process = subprocess.Popen(
            self.command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
            bufsize=1,
        )

    def _next_id(self):
        return next(self._id_counter)

    def _send(self, message):
        if self.logger:
            self.logger.log_request(self.name, message)
        self.process.stdin.write(json.dumps(message) + "\n")
        self.process.stdin.flush()

    def _send_notification(self, method, params=None):
        message = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            message["params"] = params
        self._send(message)

    def _request(self, method, params=None):
        req_id = self._next_id()
        message = {"jsonrpc": "2.0", "id": req_id, "method": method}
        if params is not None:
            message["params"] = params
        self._send(message)
        line = self.process.stdout.readline()
        response = json.loads(line)
        if self.logger:
            self.logger.log_response(self.name, response)
        return response

    def initialize(self):
        response = self._request("initialize", {
            "protocolVersion": "2025-06-18",
            "capabilities": {},
            "clientInfo": {"name": "proyecto1-chatbot", "version": "1.0.0"},
        })
        self._send_notification("notifications/initialized")
        return response

    def list_tools(self):
        response = self._request("tools/list")
        self.tools = response.get("result", {}).get("tools", [])
        return self.tools

    def call_tool(self, tool_name, arguments):
        response = self._request("tools/call", {
            "name": tool_name,
            "arguments": arguments,
        })
        return response.get("result")

    def stop(self):
        if self.process:
            self.process.terminate()