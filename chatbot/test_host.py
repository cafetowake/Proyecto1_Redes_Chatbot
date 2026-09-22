"""
Universidad del Valle de Guatemala
Facultad de Ingenieria
Departamento de Ciencias de la Computacion
CC3067 - Redes de Computadoras
Ciclo 02, 2026

Proyecto 1 - Uso de un protocolo existente
Chatbot host - Automated tests

Name: Paula Daniela De Leon Godoy
Carnet: 23202
Date: 09/21/2026

Description:
Tests multi-turn context and tool call handling against the real local
pharmacy server, with the LLM response mocked. Also verifies that
server launch commands resolve to Windows-compatible paths.
"""

import sys
import unittest

from unittest.mock import MagicMock

from conversation import Conversation
from host import build_server_configs
from mcp_client import McpClient
from mcp_logger import McpLogger


def fake_text_block(text):
    block = MagicMock()
    block.type = "text"
    block.text = text
    block.model_dump.return_value = {"type": "text", "text": text}
    return block


def fake_tool_use_block(tool_name, tool_input, tool_id="call_1"):
    block = MagicMock()
    block.type = "tool_use"
    block.name = tool_name
    block.input = tool_input
    block.id = tool_id
    block.model_dump.return_value = {"type": "tool_use", "id": tool_id, "name": tool_name, "input": tool_input}
    return block


def fake_response(content_blocks, stop_reason):
    response = MagicMock()
    response.content = content_blocks
    response.stop_reason = stop_reason
    return response

class TestHostFlow(unittest.TestCase):

    def setUp(self):
        self.logger = McpLogger(path="test_mcp_interactions.log")
        self.pharmacy = McpClient(
            "pharmacy-local",
            [sys.executable, "../mcp-server-local/server.py"],
            logger=self.logger,
        )
        self.pharmacy.start()
        self.pharmacy.initialize()
        self.pharmacy.list_tools()

    def tearDown(self):
        self.pharmacy.stop()

    def test_build_server_configs_uses_windows_compatible_paths(self):
        configs = build_server_configs()

        self.assertEqual(configs[0]["name"], "pharmacy-local")
        self.assertTrue(configs[0]["command"][0].endswith("python.exe"))
        self.assertTrue(configs[0]["command"][1].endswith("mcp-server-local\\server.py"))

        filesystem = next(config for config in configs if config["name"] == "filesystem")
        self.assertEqual(filesystem["command"][0].lower().endswith("npx.cmd"), True)
        self.assertTrue(filesystem["command"][3].startswith("C:"))

    def test_multi_turn_context_and_tool_call(self):
        conversation = Conversation(system="Eres un asistente de farmacia.")

        conversation.add_user_message("Quien fue Alan Turing")
        conversation.add_assistant_message([fake_text_block("Fue un matematico britanico.").model_dump()])

        conversation.add_user_message("Tengo fiebre, que me recomiendas")

        tool_call_response = fake_response(
            [fake_tool_use_block("search_by_symptom", {"symptom": "fiebre"})],
            stop_reason="tool_use",
        )
        final_response = fake_response(
            [fake_text_block("Te recomiendo paracetamol o ibuprofeno.")],
            stop_reason="end_turn",
        )

        response = tool_call_response
        while response.stop_reason == "tool_use":
            assistant_blocks = [block.model_dump() for block in response.content]
            conversation.add_assistant_message(assistant_blocks)

            tool_result_blocks = []
            for block in response.content:
                if block.type == "tool_use":
                    result = self.pharmacy.call_tool(block.name, block.input)
                    tool_result_blocks.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result["content"],
                        "is_error": result.get("isError", False),
                    })

            conversation.add_user_message(tool_result_blocks)
            response = final_response

        messages = conversation.get_messages()

        self.assertEqual(messages[0]["content"], "Quien fue Alan Turing")
        self.assertEqual(messages[2]["content"], "Tengo fiebre, que me recomiendas")

        tool_result_message = messages[4]
        self.assertEqual(tool_result_message["role"], "user")
        self.assertEqual(tool_result_message["content"][0]["type"], "tool_result")
        self.assertFalse(tool_result_message["content"][0]["is_error"])
        self.assertIn("paracetamol", tool_result_message["content"][0]["content"][0]["text"].lower())


if __name__ == "__main__":
    unittest.main()