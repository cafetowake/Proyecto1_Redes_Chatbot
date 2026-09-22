"""
Universidad del Valle de Guatemala
Facultad de Ingenieria
Departamento de Ciencias de la Computacion
CC3067 - Redes de Computadoras
Ciclo 02, 2026

Proyecto 1 - Uso de un protocolo existente
Scripted demo, Filesystem and Git tool usage

Name: Paula Daniela De Leon Godoy
Carnet: 23202
Date: 09/21/2026

Description:
Sends a single natural language instruction to the chatbot to create a
repository, a README, stage it, and commit, resolved through chained
calls to the Filesystem and Git MCP tools.
"""

from llm_client import LlmClient
from conversation import Conversation
from mcp_logger import McpLogger
from host import build_server_configs, start_servers, mcp_tools_to_anthropic_format

DEMO_INSTRUCTION = (
    "Crea un repositorio git en la carpeta actual, crea un archivo README.md "
    "con el titulo 'Demo Proyecto 1', agregalo al staging y realiza un commit "
    "con el mensaje 'Initial commit desde el chatbot'."
)


def run_demo():
    logger = McpLogger(path="demo_mcp_interactions.log")
    servers, all_tools, tool_clients = start_servers(build_server_configs(), logger)
    tools_for_llm = mcp_tools_to_anthropic_format(all_tools)

    llm = LlmClient()
    conversation = Conversation(system="Eres un asistente que ejecuta tareas de archivos y control de versiones usando las herramientas disponibles.")
    conversation.add_user_message(DEMO_INSTRUCTION)

    response = llm.send(conversation.get_messages(), tools=tools_for_llm, system=conversation.system)

    while response.stop_reason == "tool_use":
        assistant_blocks = [block.model_dump() for block in response.content]
        conversation.add_assistant_message(assistant_blocks)

        tool_result_blocks = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"Llamando a {block.name} con {block.input}")
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
    print("\nRespuesta final del chatbot:")
    print(final_text)

    for server in servers:
        server.stop()


if __name__ == "__main__":
    run_demo()