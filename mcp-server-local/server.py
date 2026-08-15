import sys
import json
from catalog import MEDICATIONS, SYMPTOM_MAP

PROTOCOL_VERSION = "2025-06-18"
SERVER_NAME = "pharmacy-mcp"
SERVER_VERSION = "1.0.0"

class McpError(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code
        self.message = message

def handle_initialize(params):
    return {
        "protocolVersion": PROTOCOL_VERSION,
        "capabilities": {"tools": {}},
        "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
    }

TOOLS = [
    {
        "name": "search_by_symptom",
        "description": "Busca medicamentos recomendados segun un sintoma reportado por el cliente",
        "inputSchema": {
            "type": "object",
            "properties": {
                "symptom": {"type": "string", "description": "Sintoma en lenguaje natural, ej. 'dolor de cabeza'"}
            },
            "required": ["symptom"],
        },
    },
    {
        "name": "get_medication_details",
        "description": "Obtiene la informacion completa de un medicamento por su nombre",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Nombre del medicamento"}
            },
            "required": ["name"],
        },
    },
    {
        "name": "purchase_medication",
        "description": "Realiza la compra de un medicamento y descuenta del inventario",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Nombre del medicamento"},
                "quantity": {"type": "integer", "description": "Cantidad a comprar", "minimum": 1},
            },
            "required": ["name", "quantity"],
        },
    },
]


def text_result(text, is_error=False):
    return {"content": [{"type": "text", "text": text}], "isError": is_error}


def handle_search_by_symptom(args):
    symptom = args.get("symptom", "").strip().lower()
    matches = SYMPTOM_MAP.get(symptom)
    if not matches:
        return text_result(f"No se encontraron medicamentos para el sintoma '{symptom}'.")
    lines = [f"Medicamentos recomendados para '{symptom}':"]
    for name in matches:
        med = MEDICATIONS[name]
        lines.append(f"- {name}: {med['description']} (Q{med['price']})")
    return text_result("\n".join(lines))


def handle_get_medication_details(args):
    name = args.get("name", "").strip().lower()
    med = MEDICATIONS.get(name)
    if not med:
        return text_result(f"El medicamento '{name}' no existe en el catalogo.", is_error=True)
    rx = "si" if med["requires_prescription"] else "no"
    text = (
        f"Nombre: {name}\n"
        f"Descripcion: {med['description']}\n"
        f"Precio: Q{med['price']}\n"
        f"Stock disponible: {med['stock']}\n"
        f"Requiere receta: {rx}"
    )
    return text_result(text)


def handle_purchase_medication(args):
    name = args.get("name", "").strip().lower()
    quantity = args.get("quantity", 0)

    med = MEDICATIONS.get(name)
    if not med:
        return text_result(f"El medicamento '{name}' no existe en el catalogo.", is_error=True)
    if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity <= 0:
        return text_result("La cantidad debe ser un entero mayor a 0.", is_error=True)
    if med["requires_prescription"]:
        return text_result(f"'{name}' requiere receta medica, no se puede comprar por este medio.", is_error=True)
    if med["stock"] < quantity:
        return text_result(f"Stock insuficiente. Disponible: {med['stock']} unidades.", is_error=True)

    med["stock"] -= quantity
    total = round(med["price"] * quantity, 2)
    return text_result(f"Compra confirmada: {quantity}x {name} por Q{total}. Stock restante: {med['stock']}.")


TOOL_HANDLERS = {
    "search_by_symptom": handle_search_by_symptom,
    "get_medication_details": handle_get_medication_details,
    "purchase_medication": handle_purchase_medication,
}

def handle_tools_list(params):
    return {"tools": TOOLS}

def handle_tools_call(params):
    
    name = params.get("name")
    arguments = params.get("arguments", {})
    handler = TOOL_HANDLERS.get(name)
    if not handler:
        raise McpError(-32602, f"Unknown tool: {name}")
    return handler(arguments)

METHODS = {
    "initialize": handle_initialize,
    "tools/list": handle_tools_list,
    "tools/call": handle_tools_call,
}

def write_message(obj):
    sys.stdout.write(json.dumps(obj) + "\n")
    sys.stdout.flush()

def process_request(request):
    req_id = request.get("id")
    method = request.get("method")
    params = request.get("params", {})

    if method not in METHODS:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method not found: {method}"}}

    try:
        result = METHODS[method](params)
        return {"jsonrpc": "2.0", "id": req_id, "result": result}
    except McpError as e:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": e.code, "message": e.message}}
    except Exception as e:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32603, "message": str(e)}}

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