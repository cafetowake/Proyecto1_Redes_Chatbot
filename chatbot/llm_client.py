"""
Universidad del Valle de Guatemala
Facultad de Ingenieria
Departamento de Ciencias de la Computacion
CC3067 - Redes de Computadoras
Ciclo 02, 2026

Proyecto 1 - Uso de un protocolo existente
Chatbot host - Anthropic API client

Name: Paula Daniela De Leon Godoy
Carnet: 23202
Date: 09/21/2026

Description:
Wraps the call to the Anthropic API, without handling conversation
state or tool logic, that lives in conversation.py and host.py.
"""

import os
import anthropic

MODEL = "claude-haiku-4-5-20251001"
MAX_TOKENS = 512


class LlmClient:
    def __init__(self, api_key=None):
        self.client = anthropic.Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))

    def send(self, messages, tools=None, system=None):
        kwargs = {
            "model": MODEL,
            "max_tokens": MAX_TOKENS,
            "messages": messages,
        }
        if tools:
            kwargs["tools"] = tools
        if system:
            kwargs["system"] = system
        return self.client.messages.create(**kwargs)