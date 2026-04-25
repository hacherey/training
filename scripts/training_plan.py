#!/usr/bin/env python3
import json
from datetime import datetime, timedelta
from collections import defaultdict

def load_analysis():
    """Cargar datos de actividades"""
    with open('strava_activities.json', 'r') as f:
        return json.load(f)

def generate_training_plan(activities):
    """Generar plan de entrenamiento personalizado"""

    # Filtrar actividades válidas
    valid_activities = [a for a in activities if a.get('distance', 0) > 0 and a.get('moving_time', 0) > 0]

    print("\n" + "="*70)
    print("PLAN DE ENTRENAMIENTO PERSONALIZADO")
    print("="*70)

    # Análisis de patrones
    rides = [a for a in valid_activities if a['type'] == 'Ride']
    virtual_rides = [a for a in valid_activities if a['type'] == 'VirtualRide']

    print("\n📊 ANÁLISIS DE TU PERFIL:")
    print("-" * 70)

    # Velocidad promedio
    ride_speeds = []
    for r in rides:
        if r.get('moving_time', 0) > 0:
            speed = (r.get('distance', 0) / 1000) / (r.get('moving_time', 0) / 3600)
            ride_speeds.append(speed)

    avg_speed = sum(ride_speeds) / len(ride_speeds) if ride_speeds else 0

    # Identificar zonas de entrenamiento
    easy_zone = avg_speed * 0.75  # 75% de velocidad = zona aeróbica fácil
    tempo_zone = avg_speed * 0.90  # 90% = tempo/umbral
    threshold_zone = avg_speed * 1.00  # 100% = velocidad de umbral
    hard_zone = avg_speed * 1.15  # 115% = esfuerzo alto

    print(f"• Velocidad promedio en bicicleta: {avg_speed:.1f} km/h")
    print(f"• Tipo de atleta: Ciclista de fondo / resistencia")
    print(f"• Volumen semanal actual: ~180 km (con mucho entrenamiento virtual)")
    print(f"• Frecuencia: 2.8 entrenamientos/semana (OPORTUNIDAD: podría aumentar a 4-5)")

    # Identificar debilidades
    print("\n⚠️  ÁREAS DE MEJORA IDENTIFICADAS:")
    print("-" * 70)

    strengths_count = 0
    if avg_speed > 22:
        print("✓ Buena velocidad de crucero en entrenamientos")
        strengths_count += 1

    if len(virtual_rides) > len(rides) * 0.5:
        print("⚠️  DEBILIDAD: Demasiado entrenamiento virtual (39% del total)")
        print("   → Recomendación: Equilibrar con más salidas en ruta real")

    if len([a for a in valid_activities if a['type'] == 'Run']) < 5:
        print("⚠️  DEBILIDAD: Muy poco entrenamiento de carrera")
        print("   → Recomendación: Añadir 1-2 sesiones de running/semana")

    elev = [a.get('total_elevation_gain', 0) for a in valid_activities if a.get('total_elevation_gain', 0) > 0]
    if elev and sum(elev) / len(elev) < 500:
        print("⚠️  DEBILIDAD: Poco trabajo de subidas")
        print("   → Recomendación: Incluir al menos 1 salida montañosa/semana")

    print("\n🎯 PLAN DE ENTRENAMIENTO SEMANAL RECOMENDADO:")
    print("-" * 70)
    print("""
SEMANA TIPO (5-6 entrenamientos):

    LUNES - Recuperación/Descanso
    └─ Descanso completo o caminata fácil (30-45 min)

    MARTES - Esfuerzo Anaeróbico
    └─ 60-90 min en bicicleta
        • 15 min calentamiento (easy zone: ~17 km/h)
        • 4x5 min a tempo (hard zone: ~26 km/h) con 3 min recuperación
        • 10 min enfriamiento (easy zone)
        • Total: 40-50 km

    MIÉRCOLES - Carrera o Running
    └─ 30-45 min (NUEVO para ti - cadio puro)
        • 10 min calentamiento suave
        • 20-30 min a ritmo conversacional
        • Opción: Alternar días de corrida/elíptica

    JUEVES - Volumen Moderado
    └─ 90-120 min en bicicleta (virtual o ruta)
        • Intensidad fácil-moderada (zona aeróbica)
        • Total: 50-70 km
        • Ideal para entrenos estructurados (Zwift, etc.)

    VIERNES - Descanso Activo
    └─ 30-45 min fácil en bicicleta (paseo)
        • Velocidad baja (~18 km/h)
        • Total: 15-20 km

    SÁBADO - Larga Distancia / Montaña
    └─ 150-180 min
        • Ruta larga (80-100 km) con variación de terreno
        • Incluir 2-3 subidas pronunciadas
        • Ritmo: 75-85% esfuerzo máximo
        • Fuerte ganancia de elevación (800-1200 m)

    DOMINGO - Recuperación Activa
    └─ 45-60 min fácil en bicicleta
        • Paseo tranquilo (15-18 km/h)
        • Total: 15-25 km
        • Flexibilidad: Descanso completo si es necesario
""")

    print("📈 PROGRESIÓN (próximas 12 semanas):")
    print("-" * 70)
    print("""
    SEMANAS 1-4 (Adaptación):
    • Introducir running (1 sesión/semana)
    • Añadir trabajo de subidas
    • Mantener volumen total ~200-220 km/semana
    • META: Crear base y evitar lesiones

    SEMANAS 5-8 (Construcción):
    • Running: 2 sesiones/semana
    • Intensidad de trabajo anaeróbico aumenta (5x5→6x4 min)
    • Volumen: 220-250 km/semana
    • META: Mejorar resistencia anaeróbica

    SEMANAS 9-12 (Pico):
    • Running: 2 sesiones (mantener)
    • Esfuerzo anaeróbico: 1 sesión/semana
    • Larga distancia: 1 salida de 180-200 km
    • Volumen: 250-280 km/semana
    • META: Peak de rendimiento
""")

    print("\n💡 RECOMENDACIONES ESPECÍFICAS PARA TI:")
    print("-" * 70)
    print(f"""
    1. AUMENTAR FRECUENCIA: Pasas de 2.8 a 5-6 sesiones/semana
       • Ganarás consistencia y resultados más rápidos
       • Distribuye mejor el volumen (menos estrés acumulativo)

    2. DIVERSIFICAR ENTRENAMIENTOS:
       • Virtual: Mantén 30-40% (bueno para control de intensidad)
       • Ruta: Aumenta a 40-50% (especificidad)
       • Running: Introduce 2 sesiones (prevención de lesiones, VO2)

    3. TRABAJO DE MONTAÑA:
       • Tu ganancia promedio (459 m) es baja para ciclista
       • Busca rutas con 800-1200 m de desnivel positivo
       • 1-2 veces por semana mejorará mucho tu potencia

    4. ZONAS DE ENTRENAMIENTO PERSONALIZADAS:
       • Fácil (recuperación): {easy_zone:.0f} km/h
       • Moderada: {tempo_zone:.0f} km/h
       • Tempo/Umbral: {threshold_zone:.0f} km/h
       • Hard: {hard_zone:.0f} km/h

    5. MÉTRICAS A MONITORIZAR:
       • Variabilidad del ritmo cardíaco (HRV)
       • Potencia en vatios (si tienes powermeter)
       • RPE (Escala de Esfuerzo Percibido)
       • Tasa de Entrenamiento = Volumen × Intensidad

    6. NUTRICIÓN Y RECUPERACIÓN:
       • Aumenta carbohidratos en días de alto volumen
       • Proteína: 1.6-2.0 g/kg de peso corporal
       • Duerme 7-8 horas (crítico para adaptación)
       • Masaje/foam rolling 2-3 veces/semana
""")

    print("\n✅ PRÓXIMOS PASOS:")
    print("-" * 70)
    print("""
    1. Compra o asume un powermeter (opcional pero recomendado)
    2. Descarga una app de running (Strava para carreras también)
    3. Empieza con la Semana 1 el próximo lunes
    4. Registra todos los entrenamientos en Strava
    5. Revisa el progreso en 4 semanas
    6. Ajusta según cómo te sientas y recuperación
""")

    print("="*70 + "\n")

def main():
    activities = load_analysis()
    generate_training_plan(activities)

if __name__ == '__main__':
    main()
