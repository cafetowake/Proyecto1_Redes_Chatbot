"""
Universidad del Valle de Guatemala
Facultad de Ingenieria
Departamento de Ciencias de la Computacion
CC3067 - Redes de Computadoras
Ciclo 02, 2026

Proyecto 1 - Uso de un protocolo existente
Chatbot host - Conversation context

Name: Paula Daniela De Leon Godoy
Carnet: 23202
Date: 09/21/2026

Description:
Keeps the message history for a session, so the Anthropic API
receives the full context on every call.
"""

class Conversation:
    def __init__(self, system=None):
        self.system = system
        self.messages = []

    def add_user_message(self, content):
        self.messages.append({"role": "user", "content": content})

    def add_assistant_message(self, content):
        self.messages.append({"role": "assistant", "content": content})

    def get_messages(self):
        return self.messages