# Pharmacy MCP Server - Specification

Local MCP server exposing pharmacy-related tools over stdio using raw JSON-RPC 2.0.
Transport: newline-delimited JSON on stdin/stdout — each message is a single JSON object per line, with no embedded newlines.

## Methods

### initialize

Request:
```json
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"...","version":"..."}}}
```

Response:
```json
{"jsonrpc":"2.0","id":1,"result":{"protocolVersion":"2025-06-18","capabilities":{"tools":{}},"serverInfo":{"name":"pharmacy-mcp","version":"1.0.0"}}}
```

### notifications/initialized

Sent by the client after receiving the initialize response. No `id`, no response is sent back.

```json
{"jsonrpc":"2.0","method":"notifications/initialized"}
```

### tools/list

Request:
```json
{"jsonrpc":"2.0","id":2,"method":"tools/list"}
```

Response: returns the 3 tools below, each with its JSON Schema input.

#### search_by_symptom
- `symptom` (string, required): natural language symptom, e.g. `"dolor de cabeza"`
- Returns the matched medications with description and price. If the symptom is not in the catalog, returns a text result saying so (not an error).

#### get_medication_details
- `name` (string, required): medication name
- Returns description, price, stock and prescription requirement.
- If the medication does not exist, returns `isError: true`.

#### purchase_medication
- `name` (string, required)
- `quantity` (integer, required, >= 1)
- Validates, in order: medication exists, quantity is a valid integer (booleans are explicitly rejected, since `bool` is a subclass of
  `int` in Python and would otherwise pass as a valid quantity), medication does not require a prescription, and stock is sufficient.
- On success, decrements stock and returns a receipt as text.

### tools/call

Request:
```json
{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"search_by_symptom","arguments":{"symptom":"fiebre"}}}
```

Response (success):
```json
{"jsonrpc":"2.0","id":3,"result":{"content":[{"type":"text","text":"..."}],"isError":false}}
```

Response (business error, e.g. insufficient stock or missing prescription): the JSON-RPC call still succeeds, `isError` is set to
`true` inside the result so the calling LLM can read the reason and explain it to the user.
```json
{"jsonrpc":"2.0","id":3,"result":{"content":[{"type":"text","text":"..."}],"isError":true}}
```

## Errors (protocol-level)

These are returned as a JSON-RPC `error` object, not inside `result`, and only apply to protocol-level failures (not business logic):

| Code | Meaning |
|---|---|
| -32700 | Parse error (invalid JSON) |
| -32601 | Method not found |
| -32602 | Invalid params / unknown tool name |
| -32603 | Internal error |

## Usage example (search then purchase)

```json
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"demo","version":"1.0"}}}
{"jsonrpc":"2.0","method":"notifications/initialized"}
{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"search_by_symptom","arguments":{"symptom":"dolor de cabeza"}}}
{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"purchase_medication","arguments":{"name":"paracetamol","quantity":2}}}
```
## Remote deployment

The same server, with the same protocol and business logic defined in
protocol.py and catalog.py, is also exposed over HTTP transport for
cloud deployment on Render. Business logic is identical across both
transports, every method, tool, and validation rule described in the
previous sections applies without changes.

### Differences from the local transport

- Transport, HTTP instead of stdio.
- Each JSON-RPC message travels as the body of a POST request, instead
  of as a line on stdin/stdout.
- Content-Type application/json on every request.
- A notification (message without id) responds with 204 No Content
  instead of simply writing nothing to stdout.
- Containerized deployment with Docker, on Render.

### Sample HTTP request

    POST / HTTP/1.1
    Host: proyecto1-redes-chatbot.onrender.com
    Content-Type: application/json

    {"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"...","version":"..."}}}

### Current deployment URL

    https://proyecto1-redes-chatbot.onrender.com

### Verifying with curl

    curl -X POST https://proyecto1-redes-chatbot.onrender.com \
      -H "Content-Type: application/json" \
      -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'

Note, the free tier on Render puts the service to sleep after 15
minutes without traffic, the first request after that takes 30 to 50
seconds to respond while the container wakes up.