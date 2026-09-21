## Universidad del Valle de Guatemala
## CC3067 Redes de Computadoras
# Proyecto 1 - MCP Chatbot
- Protocol: Model Context Protocol (MCP), manual JSON-RPC 2.0, no SDK
- Transport: stdio for local servers, HTTP for the remote server
- LLM: Anthropic API (Claude)
- Integrated servers: pharmacy (local and remote), official Filesystem, official Git

### Author
- Paula De León


## Components

| Folder | Contents |
|---|---|
| `mcp-server-local/` | Pharmacy server, stdio and HTTP transport, same protocol.py |
| `chatbot/` | Host, Anthropic API client, stdio and HTTP MCP clients |
| `wireshark/` | Remote traffic capture and its analysis |
| `Proyecto1_Reporte_Avance.pdf` | Report, incisos 8 and 10, partial delivery |
| `Proyecto1_Reporte_Final.pdf` | Report, inciso 8 expanded, 9, and final 10 |

## Requirements

- Python 3.10+
- Node.js, for the official Filesystem server via npx
- ANTHROPIC_API_KEY environment variable

Note, on Windows use `python` instead of `python3` in the commands
below, depending on how your installation resolves it.

## Running the local pharmacy server standalone

    cd mcp-server-local
    python test_client.py

## Running the local pharmacy server over HTTP

    cd mcp-server-local
    python server_http.py

## Running the chatbot

    $env:ANTHROPIC_API_KEY="your_key_here"
    cd chatbot
    python host.py

Requires the official servers installed:

    npm install -g @modelcontextprotocol/server-filesystem
    pip install mcp-server-git --break-system-packages

## Running the filesystem and git demo scenario

    cd chatbot
    python demo_filesystem_git.py

## Running tests

    cd chatbot
    python -m unittest test_host.py -v
    python -m unittest test_remote.py -v

test_remote.py can use the PHARMACY_REMOTE_URL environment variable to
point at a different deployment.

## Deploying the remote server

Deployed on Render (https://proyecto1-redes-chatbot.onrender.com), connected
directly to this GitHub repository, with `mcp-server-local` set as the
service root directory and Docker as the environment.

## Capturing MCP traffic with Wireshark

See wireshark/README.md for the full procedure, including the
SSLKEYLOGFILE setup needed to decrypt TLS.

## Note on business errors

Business failures (no stock, prescription required, unknown
medication) are not JSON-RPC errors. The call resolves successfully
and the result carries isError true with an explanatory text, since
the LLM needs to read it to inform the user.