"""
Universidad del Valle de Guatemala
Facultad de Ingenieria
Departamento de Ciencias de la Computacion
CC3067 - Redes de Computadoras
Ciclo 02, 2026

Proyecto 1 - Uso de un protocolo existente
Chatbot host - Main program

Name: Paula Daniela De Leon Godoy
Carnet: 23202
Date: 09/21/2026

Description:
Coordinates the Anthropic API client, the conversation context, and
the MCP clients for the four integrated servers, local, remote,
Filesystem, and Git.
"""

import shutil
import sys
from pathlib import Path
from mcp_http_client import McpHttpClient
from llm_client import LlmClient
from conversation import Conversation
from mcp_client import McpClient
from mcp_logger import McpLogger

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PHARMACY_SERVER = PROJECT_ROOT / "mcp-server-local" / "server.py"

def mcp_tools_to_anthropic_format(mcp_tools):
    return [
        {
            "name": tool["name"],
            "description": tool["description"],
            "input_schema": tool["inputSchema"],
        }
        for tool in mcp_tools
    ]

def build_server_configs():
    npx_path = shutil.which("npx") or "npx"

    return [
        {"name": "pharmacy-local", "transport": "stdio", "command": [sys.executable, str(PHARMACY_SERVER)]},
        {"name": "filesystem", "transport": "stdio", "command": [npx_path, "-y", "@modelcontextprotocol/server-filesystem", str(PROJECT_ROOT)]},
        {"name": "git", "transport": "stdio", "command": [sys.executable, "-m", "mcp_server_git", "--repository", str(PROJECT_ROOT)]},
        {"name": "pharmacy-remote", "transport": "http", "url": "https://pharmacy-mcp-xxxxx.run.app"},
    ]


def start_servers(configs, logger):
    servers = []
    tool_clients = {}
    all_tools = []

    for config in configs:
        try:
            if config["transport"] == "http":
                client = McpHttpClient(config["name"], config["url"], logger=logger)
            else:
                client = McpClient(config["name"], config["command"], logger=logger)

            client.start()
            client.initialize()
            client.list_tools()
        except (FileNotFoundError, OSError) as exc:
            print(f"Advertencia: se omite el servidor '{config['name']}' porque no está disponible: {exc}")
            continue

        servers.append(client)
        all_tools.extend(client.tools)
        for tool in client.tools:
            tool_clients[tool["name"]] = client

    return servers, all_tools, tool_clients


def run():
    logger = McpLogger()
    servers, all_tools, tool_clients = start_servers(build_server_configs(), logger)
    tools_for_llm = mcp_tools_to_anthropic_format(all_tools)

    llm = LlmClient()
    conversation = Conversation(system="Eres un asistente de farmacia. Usa las herramientas disponibles cuando el usuario mencione sintomas o quiera comprar un medicamento.")

    print("Chatbot listo. Escribe 'salir' para terminar.")
    while True:
        user_input = input("\nTu: ")
        if user_input.strip().lower() == "salir":
            break

        conversation.add_user_message(user_input)
        response = llm.send(conversation.get_messages(), tools=tools_for_llm, system=conversation.system)

        while response.stop_reason == "tool_use":
            # Claude can chain several tool calls before answering in
            # text, hence the while instead of an if
            assistant_blocks = [block.model_dump() for block in response.content]
            conversation.add_assistant_message(assistant_blocks)

            tool_result_blocks = []
            for block in response.content:
                if block.type == "tool_use":
                    client = tool_clients[block.name]
                    result = client.call_tool(block.name, block.input)
                    tool_result_blocks.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result["content"],
                        "is_error": result.get("isError", False),
                    })

            conversation.add_user_message(tool_result_blocks)
            response = llm.send(conversation.get_messages(), tools=tools_for_llm, system=conversation.system)

        final_text = "".join(block.text for block in response.content if block.type == "text")
        conversation.add_assistant_message(response.content)
        print(f"Bot: {final_text}")

    for server in servers:
        server.stop()


if __name__ == "__main__":
    run()