HEART_RATE_ZONES = [
    {"key": "Z1", "min": 49, "max": 118, "label": "Reposo", "color": "#94a3b8"},
    {"key": "Z2", "min": 119, "max": 142, "label": "Aerobico", "color": "#38bdf8"},
    {"key": "Z3", "min": 143, "max": 160, "label": "Tempo", "color": "#4ade80"},
    {"key": "Z4", "min": 161, "max": 179, "label": "Umbral", "color": "#fb923c"},
    {"key": "Z5", "min": 180, "max": 195, "label": "Maximo", "color": "#f43f5e"},
]


def get_heart_rate_zone(bpm, hrmax=None):
    for zone in HEART_RATE_ZONES:
        max_bpm = zone["max"]
        if max_bpm is None:
            if bpm >= zone["min"]:
                return zone["key"]
            continue
        if zone["min"] <= bpm <= max_bpm:
            return zone["key"]
    return HEART_RATE_ZONES[0]["key"]
