"""
Universidad del Valle de Guatemala
Facultad de Ingeniería
Departamento de Ciencias de la Computación
CC3067 - Redes de Computadoras
Ciclo 02, 2026

Proyecto 1 - MCP Chatbot
Servidor MCP local

Nombre: Paula Daniela De León Godoy
Carnet: 23202
Fecha: 19/08/2026

Descripcion:
Implementacion manual del protocolo MCP sobre JSON-RPC 2.0, sin utilizar SDKs como FastMCP. El transporte es stdio: cada mensaje es un JSON en una
sola linea, sin saltos de linea embebidos. Expone tres tools relacionadas a una farmacia: busqueda de medicamentos por sintoma, consulta de detalle
de un medicamento y compra con validacion de stock y receta. """

import sys
import json

from protocol import process_request


def write_message(obj):
    sys.stdout.write(json.dumps(obj) + "\n")
    sys.stdout.flush()


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
        except json.JSONDecodeError:
            write_message({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Parse error"}})
            continue

        if "id" not in request:
            continue

        response = process_request(request)
        write_message(response)


if __name__ == "__main__":
    main()