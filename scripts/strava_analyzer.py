#!/usr/bin/env python3
import requests
import json
from datetime import datetime, timedelta, timezone
import statistics
from collections import defaultdict

# Cargar keys desde el archivo
def load_keys():
    keys = {}
    with open('data_key.properties', 'r') as f:
        for line in f:
            line = line.strip()
            if ':' in line and not line.startswith('#'):
                key, value = line.split(':', 1)
                keys[key.strip()] = value.strip()
    return keys

# Obtener access token
def get_access_token(token):
    """Usar el access token directamente"""
    return token

# Descargar entrenamientos
def get_activities(access_token, per_page=200):
    """Descargar todos los entrenamientos"""
    activities = []
    url = "https://www.strava.com/api/v3/athlete/activities"

    page = 1
    while True:
        params = {
            'per_page': per_page,
            'page': page,
            'sort': 'start_date_local',
            'direction': 'desc'
        }
        headers = {'Authorization': f'Bearer {access_token}'}

        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(f"Respuesta: {response.text}")
            break

        data = response.json()
        if not data:
            break

        activities.extend(data)
        page += 1
        print(f"Descargadas {len(activities)} actividades...")

    return activities

def analyze_activities(activities):
    """Analizar los entrenamientos"""
    if not activities:
        print("No hay actividades para analizar")
        return None

    # Filtrar solo entrenamientos válidos (con distancia y tiempo)
    valid_activities = [a for a in activities if a.get('distance', 0) > 0 and a.get('moving_time', 0) > 0]

    print(f"\n{'='*60}")
    print(f"ANÁLISIS DE ENTRENAMIENTOS STRAVA")
    print(f"{'='*60}\n")

    # Estadísticas generales
    distances = [a['distance'] / 1000 for a in valid_activities]  # Convertir a km
    times = [a['moving_time'] / 3600 for a in valid_activities]  # Convertir a horas
    activities_by_type = defaultdict(list)

    for activity in valid_activities:
        activities_by_type[activity['type']].append(activity)

    print(f"Total de entrenamientos: {len(valid_activities)}")
    print(f"Periodo: {valid_activities[-1]['start_date_local'][:10]} a {valid_activities[0]['start_date_local'][:10]}")
    print(f"\nDistancia total: {sum(distances):.1f} km")
    print(f"Tiempo total: {sum(times):.1f} horas")
    print(f"Distancia promedio: {statistics.mean(distances):.2f} km")
    print(f"Tiempo promedio: {statistics.mean(times):.2f} horas")
    print(f"Velocidad promedio: {sum(distances)/sum(times):.2f} km/h")

    # Por tipo de actividad
    print(f"\n{'ENTRENAMIENTOS POR TIPO:'}")
    print("-" * 60)
    for activity_type, acts in sorted(activities_by_type.items()):
        type_distances = [a['distance'] / 1000 for a in acts]
        type_times = [a['moving_time'] / 3600 for a in acts]
        avg_speed = sum(type_distances) / sum(type_times) if sum(type_times) > 0 else 0

        print(f"\n{activity_type}:")
        print(f"  - Cantidad: {len(acts)}")
        print(f"  - Distancia total: {sum(type_distances):.1f} km")
        print(f"  - Distancia promedio: {statistics.mean(type_distances):.2f} km")
        print(f"  - Velocidad promedio: {avg_speed:.2f} km/h")
        print(f"  - Tiempo promedio: {statistics.mean(type_times):.2f} horas")

    # Frecuencia
    print(f"\n{'FRECUENCIA DE ENTRENAMIENTO:'}")
    print("-" * 60)

    # Últimas 4 semanas
    four_weeks_ago = datetime.now(timezone.utc) - timedelta(days=28)
    recent = [a for a in valid_activities if datetime.fromisoformat(a['start_date_local'].replace('Z', '+00:00')) > four_weeks_ago]

    print(f"Entrenamientos en últimas 4 semanas: {len(recent)}")
    if len(recent) > 0:
        avg_freq = len(recent) / 4
        print(f"Frecuencia promedio: {avg_freq:.1f} entrenamientos/semana")

    # Intensidad (usando elevation gain como proxy)
    elevations = [a.get('total_elevation_gain', 0) for a in valid_activities if a.get('total_elevation_gain', 0) > 0]
    if elevations:
        print(f"\nGanancia de elevación promedio: {statistics.mean(elevations):.0f} m")

    return {
        'total_activities': len(valid_activities),
        'activities_by_type': activities_by_type,
        'distances': distances,
        'times': times,
        'recent_count': len(recent)
    }

def main():
    # Cargar keys
    keys = load_keys()

    token = keys.get('token')

    if not token:
        print("Error: Falta 'token' en el archivo data_key.properties")
        return

    print("Conectando a Strava...")

    # Usar el token directamente
    access_token = get_access_token(token)
    if not access_token:
        return

    print("Descargando entrenamientos...")

    # Descargar actividades
    activities = get_activities(access_token)

    # Guardar datos en JSON para referencia
    with open('strava_activities.json', 'w') as f:
        json.dump(activities, f, indent=2)
    print(f"\nDatos guardados en strava_activities.json")

    # Analizar
    analysis = analyze_activities(activities)

if __name__ == '__main__':
    main()
