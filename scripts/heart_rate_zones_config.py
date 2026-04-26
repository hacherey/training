HEART_RATE_ZONES = [
    {"key": "Z1", "min_pct": 0.00, "max_pct": 0.60, "label": "Reposo", "color": "#94a3b8"},
    {"key": "Z2", "min_pct": 0.60, "max_pct": 0.70, "label": "Aerobico", "color": "#38bdf8"},
    {"key": "Z3", "min_pct": 0.70, "max_pct": 0.80, "label": "Tempo", "color": "#4ade80"},
    {"key": "Z4", "min_pct": 0.80, "max_pct": 0.90, "label": "Umbral", "color": "#fb923c"},
    {"key": "Z5", "min_pct": 0.90, "max_pct": None, "label": "Maximo", "color": "#f43f5e"},
]


def get_heart_rate_zone(bpm, hrmax):
    ratio = bpm / hrmax if hrmax else 0
    for zone in HEART_RATE_ZONES:
        max_pct = zone["max_pct"]
        if max_pct is None:
            if ratio >= zone["min_pct"]:
                return zone["key"]
            continue
        if zone["min_pct"] <= ratio < max_pct:
            return zone["key"]
    return HEART_RATE_ZONES[0]["key"]
