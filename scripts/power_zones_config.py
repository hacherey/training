POWER_ZONES = [
    {"key": "Z1", "min": 0, "max": 105, "label": "Recuperacion", "color": "#94a3b8"},
    {"key": "Z2", "min": 106, "max": 143, "label": "Aerobico", "color": "#38bdf8"},
    {"key": "Z3", "min": 144, "max": 171, "label": "Tempo", "color": "#4ade80"},
    {"key": "Z4", "min": 172, "max": 200, "label": "Umbral", "color": "#fb923c"},
    {"key": "Z5", "min": 201, "max": 228, "label": "VO2max", "color": "#f43f5e"},
    {"key": "Z6", "min": 229, "max": 263, "label": "Anaerobico", "color": "#a855f7"},
    {"key": "Z7", "min": 264, "max": None, "label": "Neuromuscular", "color": "#eab308"},
]


def get_power_zone(watts):
    for zone in POWER_ZONES:
        max_watts = zone["max"]
        if max_watts is None:
            if watts >= zone["min"]:
                return zone["key"]
            continue
        if zone["min"] <= watts <= max_watts:
            return zone["key"]
    return POWER_ZONES[0]["key"]
