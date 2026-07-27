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