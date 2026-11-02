# steel.py

STEEL_MATERIALS = {
    "Steel01": {
        "class": "Steel",
        "label": "Steel01",
        "parameters": [
            {"name": "Fy", "type": float, "unit": "Pa", "required": True},
            {"name": "E0", "type": float, "unit": "Pa", "required": True},
            {"name": "b_strainhardratio",  "type": float, "unit": "-",  "required": True},
            {"name": "a1_isohard",  "type": float, "required": False},
            {"name": "a2_isohard",  "type": float, "required": False},
            {"name": "a3_isohard",  "type": float, "required": False},
            {"name": "a4_isohard",  "type": float, "required": False},
        ]
    },
    "Steel02": {
        "class": "Steel",
        "label": "Steel02",
        "parameters": [
            {"name": "Fy", "type": float, "unit": "Pa", "required": True},
            {"name": "E0", "type": float, "unit": "Pa", "required": True},
            {"name": "b_strainhardratio",  "type": float, "required": True},
            {"name": "R0", "type": float, "required": True},
            {"name": "cR1", "type": float, "required": True},
            {"name": "cR2", "type": float, "required": True},
            {"name": "a1_isohard",  "type": float, "required": False},
            {"name": "a2_isohard",  "type": float, "required": False},
            {"name": "a3_isohard",  "type": float, "required": False},
            {"name": "a4_isohard",  "type": float, "required": False},
            {"name": "sigInit",  "type": float, "required": False},
        ]
    },
    "Steel4": {
        "class": "Steel",
        "label": "Steel4",
        "parameters": [
            {"name": "Fy", "type": float, "unit": "Pa", "required": True},
            {"name": "E0", "type": float, "unit": "Pa", "required": True},
            {"name": "b_k",  "type": float, "unit": "-",  "required": True},
            {"name": "R0", "type": float, "required": True},
            {"name": "cR1", "type": float, "required": True},
            {"name": "cR2", "type": float, "required": True},
            {"name": "b_i",  "type": float, "unit": "-",  "required": True},
            {"name": "b_l",  "type": float, "unit": "-",  "required": True},
            {"name": "rho_i",  "type": float, "unit": "-",  "required": True},
            {"name": "R_i",  "type": float, "unit": "-",  "required": True},
            {"name": "l_yp",  "type": float, "unit": "-",  "required": True},
            {"name": "f_u",  "type": float, "unit": "-",  "required": True},
            {"name": "R_u",  "type": float, "unit": "-",  "required": True},
            {"name": "asym", "type": bool, "rewuired": False},
            {"name": "sig_init",  "type": float, "unit": "Pa",  "required": True},
            {"name": "cycNum",  "type": float, "unit": "-",  "required": True},
        ]
    },
    "ReinforcingSteel": {
        "class": "Steel",
        "label": "ReinforcingSteel",
        "parameters": [
            {"name": "Fy", "type": float, "unit": "Pa", "required": True},
            {"name": "E0", "type": float, "unit": "Pa", "required": True},
            {"name": "b_strainhardratio",  "type": float, "unit": "-",  "required": True},
            {"name": "a1_isohard",  "type": float, "required": False},
            {"name": "a2_isohard",  "type": float, "required": False},
            {"name": "a3_isohard",  "type": float, "required": False},
            {"name": "a4_isohard",  "type": float, "required": False},
        ]
    },

}
