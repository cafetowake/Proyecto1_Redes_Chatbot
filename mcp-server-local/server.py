import sys
import json

PROTOCOL_VERSION = "2025-06-18"
SERVER_NAME = "pharmacy-mcp"
SERVER_VERSION = "1.0.0"

class McpError(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code
        self.message = message

def handle_initialize(params):
    return {
        "protocolVersion": PROTOCOL_VERSION,
        "capabilities": {"tools": {}},
        "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
    }

METHODS = {
    "initialize": handle_initialize,
}

def write_message(obj):
    sys.stdout.write(json.dumps(obj) + "\n")
    sys.stdout.flush()

def process_request(request):
    req_id = request.get("id")
    method = request.get("method")
    params = request.get("params", {})

    if method not in METHODS:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method not found: {method}"}}

    try:
        result = METHODS[method](params)
        return {"jsonrpc": "2.0", "id": req_id, "result": result}
    except McpError as e:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": e.code, "message": e.message}}
    except Exception as e:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32603, "message": str(e)}}

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
        except json.JSONDecodeError:
            write_message({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Parse error"}})
            continue

        if "id" not in request:
            continue

        response = process_request(request)
        write_message(response)

if __name__ == "__main__":
    main()