"""
Universidad del Valle de Guatemala
Facultad de Ingenieria
Departamento de Ciencias de la Computacion
CC3067 - Redes de Computadoras
Ciclo 02, 2026

Proyecto 1 - Uso de un protocolo existente
End-to-end tests against the remote MCP server

Name: Paula Daniela De Leon Godoy
Carnet: 23202
Date: 09/21/2026

Description:
Verifies the deployed server on Render responds correctly over HTTP,
covering the same business rules already tested on the local server.
"""

import os
import unittest

from mcp_http_client import McpHttpClient
from mcp_logger import McpLogger

REMOTE_URL = os.environ.get("PHARMACY_REMOTE_URL", "https://proyecto1-redes-chatbot.onrender.com")


class TestRemoteServer(unittest.TestCase):

    def setUp(self):
        self.logger = McpLogger(path="test_remote_interactions.log")
        self.client = McpHttpClient("pharmacy-remote", REMOTE_URL, logger=self.logger)
        self.client.initialize()
        self.client.list_tools()

    def test_tools_list_matches_local_server(self):
        tool_names = {tool["name"] for tool in self.client.tools}
        self.assertEqual(tool_names, {"search_by_symptom", "get_medication_details", "purchase_medication"})

    def test_search_by_symptom_over_http(self):
        result = self.client.call_tool("search_by_symptom", {"symptom": "fiebre"})
        self.assertFalse(result["isError"])
        self.assertIn("paracetamol", result["content"][0]["text"].lower())

    def test_purchase_requiring_prescription_is_rejected(self):
        result = self.client.call_tool("purchase_medication", {"name": "amoxicilina", "quantity": 1})
        self.assertTrue(result["isError"])
        self.assertIn("receta", result["content"][0]["text"].lower())


if __name__ == "__main__":
    unittest.main()