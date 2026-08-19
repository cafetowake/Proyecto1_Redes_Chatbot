"""
Universidad del Valle de Guatemala
Facultad de Ingeniería
Departamento de Ciencias de la Computación
CC3067 - Redes de Computadoras
Ciclo 02, 2026

Proyecto 1 - MCP Chatbot
Cliente de prueba para el servidor MCP local

Nombre: Paula Daniela De León Godoy
Carnet: 23202
Fecha: 19/08/2026

Descripcion:
Levanta server.py como subproceso y ejecuta el handshake completo para verificar el servidor de forma standalone, sin depender del chatbot.
"""

import json
import subprocess

import sys

proc = subprocess.Popen(
    [sys.executable, "server.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    text=True,
    bufsize=1,
)

messages = [
    {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "test-client", "version": "1.0"}}},
    {"jsonrpc": "2.0", "method": "notifications/initialized"},
    {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
    {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "search_by_symptom", "arguments": {"symptom": "dolor de cabeza"}}},
    {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "purchase_medication", "arguments": {"name": "paracetamol", "quantity": 2}}},
    {"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "purchase_medication", "arguments": {"name": "amoxicilina", "quantity": 1}}},
    {"jsonrpc": "2.0", "id": 6, "method": "tools/call", "params": {"name": "get_medication_details", "arguments": {"name": "ibuprofeno"}}},
]

for msg in messages:
    if proc.stdin:
        proc.stdin.write(json.dumps(msg) + "\n")
        proc.stdin.flush()
    if isinstance(msg, dict) and msg.get("id") is not None:
        if proc.stdout:
            line = proc.stdout.readline()
            print(json.dumps(json.loads(line), indent=2, ensure_ascii=False))
            print("---")

proc.terminate()