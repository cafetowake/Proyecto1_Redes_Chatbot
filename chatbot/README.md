# Chatbot Host

Connects to the Anthropic API and coordinates four MCP clients, the
local pharmacy server, its remote deployment on Render, and the
official Filesystem and Git MCP servers.

## Files

- `host.py` - main program, entry point
- `llm_client.py` - Anthropic API wrapper
- `conversation.py` - conversation context across turns
- `mcp_client.py` - generic MCP client over stdio
- `mcp_http_client.py` - generic MCP client over HTTP
- `mcp_logger.py` - logs every MCP request and response
- `test_host.py` - automated tests, local server and cross-platform paths
- `test_remote.py` - end-to-end tests against the remote server
- `demo_filesystem_git.py` - scripted demo, repo creation via chatbot

See the root README.md for setup and running instructions.