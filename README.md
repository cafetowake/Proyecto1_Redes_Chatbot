## Universidad del Valle de Guatemala
## CC3067 Redes de Computadoras
# Proyecto 1 - MCP Chatbot
- Protocol: Model Context Protocol, manual JSON-RPC 2.0 over stdio
- Use case: pharmacy chatbot (symptom-based medication recommendation and purchase)
- Language: Python

### Author
- Paula De León

## Tools exposed by the server

| Tool | Purpose | Required arguments |
|---|---|---|
| `search_by_symptom` | Recommend medications for a symptom | `symptom` (string) |
| `get_medication_details` | Return full detail of a medication | `name` (string) |
| `purchase_medication` | Buy a medication and update stock | `name` (string), `quantity` (integer >= 1) |

## Requirements

- Python 3.10+

## Running the server standalone

    cd mcp-server-local
    python3 test_client.py

This runs the server as a subprocess and exercises initialize, notifications/initialized, tools/list and tools/call, printing each
JSON-RPC response.

## Running the server directly

    cd mcp-server-local
    python3 server.py

Then send JSON-RPC messages one per line via stdin. See mcp-server-local/SPEC.md for the full message reference.

## Project structure

    mcp-server-local/
      server.py        JSON-RPC transport and MCP method handlers
      catalog.py        Medication data and symptom mapping
      test_client.py     Standalone stdio test client
      SPEC.md            Tool specification and message examples
