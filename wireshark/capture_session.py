"""
Universidad del Valle de Guatemala
Facultad de Ingenieria
Departamento de Ciencias de la Computacion
CC3067 - Redes de Computadoras
Ciclo 02, 2026

Proyecto 1 - Uso de un protocolo existente
Traffic generator for Wireshark capture

Name: Paula Daniela De Leon Godoy
Carnet: 23202
Date: 09/21/2026

Description:
Sends a fixed sequence of JSON-RPC messages to the remote MCP server
over HTTPS, exporting TLS session keys via SSLKEYLOGFILE so the
resulting capture can be decrypted and analyzed in Wireshark.
"""

import os
import ssl
import json
import http.client
from urllib.parse import urlparse

REMOTE_URL = os.environ.get("PHARMACY_REMOTE_URL", "https://proyecto1-redes-chatbot.onrender.com")
KEYLOG_PATH = os.environ.get("SSLKEYLOGFILE", "tls_keys.log")

parsed = urlparse(REMOTE_URL)

context = ssl.create_default_context()
context.keylog_filename = KEYLOG_PATH


def send(conn, message):
    body = json.dumps(message)
    conn.request("POST", parsed.path or "/", body=body, headers={"Content-Type": "application/json"})
    resp = conn.getresponse()
    data = resp.read()
    print(f"-> {message}")
    if data:
        print(f"<- {data.decode('utf-8')}")
    else:
        print(f"<- (status {resp.status}, sin body)")
    return data


def main():
    conn = http.client.HTTPSConnection(parsed.hostname, parsed.port or 443, context=context)

    send(conn, {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
        "protocolVersion": "2025-06-18", "capabilities": {},
        "clientInfo": {"name": "wireshark-capture", "version": "1.0"},
    }})
    send(conn, {"jsonrpc": "2.0", "method": "notifications/initialized"})
    send(conn, {"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
    send(conn, {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {
        "name": "search_by_symptom", "arguments": {"symptom": "fiebre"},
    }})
    send(conn, {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {
        "name": "purchase_medication", "arguments": {"name": "amoxicilina", "quantity": 1},
    }})

    conn.close()


if __name__ == "__main__":
    main()