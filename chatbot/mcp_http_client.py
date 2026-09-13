import json
import itertools
import urllib.request


class McpHttpClient:
    def __init__(self, name, url, logger=None):
        self.name = name
        self.url = url
        self.logger = logger
        self._id_counter = itertools.count(1)
        self.tools = []

    def start(self):
        pass

    def stop(self):
        pass

    def _next_id(self):
        return next(self._id_counter)

    def _post(self, message):
        if self.logger:
            self.logger.log_request(self.name, message)

        data = json.dumps(message).encode("utf-8")
        req = urllib.request.Request(self.url, data=data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req) as resp:
            if resp.status == 204:
                return None
            body = resp.read()
            response = json.loads(body)

        if self.logger:
            self.logger.log_response(self.name, response)
        return response

    def _send_notification(self, method, params=None):
        message = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            message["params"] = params
        self._post(message)

    def _request(self, method, params=None):
        req_id = self._next_id()
        message = {"jsonrpc": "2.0", "id": req_id, "method": method}
        if params is not None:
            message["params"] = params
        return self._post(message)

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