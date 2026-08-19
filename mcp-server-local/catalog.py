"""
Universidad del Valle de Guatemala
Facultad de Ingeniería
Departamento de Ciencias de la Computación
CC3067 - Redes de Computadoras
Ciclo 02, 2026

Proyecto 1 - MCP Chatbot
Servidor MCP local - Catalogo de datos

Nombre: Paula Daniela De León Godoy
Carnet: 23202
Fecha: 19/08/2026

Descripcion:
Datos del catalogo de medicamentos y el mapeo de sintomas a medicamentos recomendados, utilizados por el servidor MCP local para responder a las
tools search_by_symptom, get_medication_details y purchase_medication.
"""

# Catalogo de medicamentos: precio en quetzales, stock disponible y si requiere receta medica para poder comprarse.

MEDICATIONS = {
    "paracetamol": {
        "description": "Analgesico y antipiretico, alivia dolor leve a moderado y fiebre",
        "price": 15.50,
        "stock": 120,
        "requires_prescription": False,
    },
    "ibuprofeno": {
        "description": "Antiinflamatorio no esteroideo, util para dolor, fiebre e inflamacion",
        "price": 18.00,
        "stock": 80,
        "requires_prescription": False,
    },
    "loratadina": {
        "description": "Antihistaminico para alergias, rinitis y urticaria",
        "price": 22.75,
        "stock": 45,
        "requires_prescription": False,
    },
    "omeprazol": {
        "description": "Inhibidor de bomba de protones, reduce acidez estomacal",
        "price": 30.00,
        "stock": 60,
        "requires_prescription": False,
    },
    "amoxicilina": {
        "description": "Antibiotico de amplio espectro para infecciones bacterianas",
        "price": 45.25,
        "stock": 25,
        "requires_prescription": True,
    },
    "dextrometorfano": {
        "description": "Antitusivo para tos seca",
        "price": 20.00,
        "stock": 50,
        "requires_prescription": False,
    },
}

# Mapeo de sintoma a lista de medicamentos recomendados, ordenados por prioridad de recomendacion.

SYMPTOM_MAP = {
    "dolor de cabeza": ["paracetamol", "ibuprofeno"],
    "fiebre": ["paracetamol", "ibuprofeno"],
    "dolor muscular": ["ibuprofeno", "paracetamol"],
    "alergia": ["loratadina"],
    "rinitis": ["loratadina"],
    "acidez": ["omeprazol"],
    "gastritis": ["omeprazol"],
    "infeccion": ["amoxicilina"],
    "tos": ["dextrometorfano"],
    "tos seca": ["dextrometorfano"],
}