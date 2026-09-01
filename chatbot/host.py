import sys
from llm_client import LlmClient
from conversation import Conversation
from mcp_client import McpClient
from mcp_logger import McpLogger


def mcp_tools_to_anthropic_format(mcp_tools):
    return [
        {
            "name": tool["name"],
            "description": tool["description"],
            "input_schema": tool["inputSchema"],
        }
        for tool in mcp_tools
    ]

def run():
    logger = McpLogger()

    pharmacy = McpClient("pharmacy-local", [sys.executable,"../mcp-server-local/server.py"], logger=logger)
    pharmacy.start()
    pharmacy.initialize()
    pharmacy.list_tools()

    tools_for_llm = mcp_tools_to_anthropic_format(pharmacy.tools)
    tool_clients = {tool["name"]: pharmacy for tool in pharmacy.tools}

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

    pharmacy.stop()


if __name__ == "__main__":
    run()