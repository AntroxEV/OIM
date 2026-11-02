# concrete.py

CONCRETE_MATERIALS = {
    "Concrete01": {
        "class": "Concrete",
        "label": "Concrete01",
        "parameters": [
            {"name": "fpc", "type": float, "unit": "Pa", "required": True},
            {"name": "epsc0", "type": float, "required": True},
            {"name": "fpcu", "type": float},
            {"name": "epsU", "type": float}
        ]
    }
}
