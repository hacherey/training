#!/usr/bin/env python3
import json
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, ElementTree

def create_zwift_workout():
    """Crear un workout en formato Zwift (.zwo)"""
    # Parámetros basados en tu análisis
    ftp = 250  # FTP estimado (ajusta según tu potencia)

    zwift_workout = """<?xml version="1.0" encoding="UTF-8"?>
<workout_file>
  <author>Training Plan Hugo</author>
  <name>Martes - Esfuerzo Anaeróbico</name>
  <description>Sesión de esfuerzo a ritmo tempo - 4x5 minutos de high intensity</description>
  <sportType>cycling</sportType>
  <tags>
    <tag>anaerobic</tag>
    <tag>tempo</tag>
    <tag>indoor</tag>
  </tags>
  <workout>
    <!-- Calentamiento: 15 minutos -->
    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65" pace="0.8">
      <label>Calentamiento: 15 min</label>
      <description>Ritmo fácil, deja que el cuerpo se adapte</description>
    </Warmup>

    <!-- Bloque 1: 5 min a tempo -->
    <SteadyState Duration="300" Power="0.90" pace="1.0">
      <label>Tempo 1 de 4: 5 min</label>
      <description>Ritmo fuerte pero controlado (~23 km/h)</description>
    </SteadyState>

    <!-- Recuperación: 3 minutos -->
    <SteadyState Duration="180" Power="0.55" pace="0.75">
      <label>Recuperación: 3 min</label>
      <description>Vuelta a ritmo fácil</description>
    </SteadyState>

    <!-- Bloque 2: 5 min a tempo -->
    <SteadyState Duration="300" Power="0.90" pace="1.0">
      <label>Tempo 2 de 4: 5 min</label>
      <description>Mantén el ritmo, respira profundo</description>
    </SteadyState>

    <!-- Recuperación: 3 minutos -->
    <SteadyState Duration="180" Power="0.55" pace="0.75">
      <label>Recuperación: 3 min</label>
    </SteadyState>

    <!-- Bloque 3: 5 min a tempo -->
    <SteadyState Duration="300" Power="0.90" pace="1.0">
      <label>Tempo 3 de 4: 5 min</label>
      <description>Ya estamos en la mitad! Aguanta el ritmo</description>
    </SteadyState>

    <!-- Recuperación: 3 minutos -->
    <SteadyState Duration="180" Power="0.55" pace="0.75">
      <label>Recuperación: 3 min</label>
    </SteadyState>

    <!-- Bloque 4: 5 min a tempo -->
    <SteadyState Duration="300" Power="0.90" pace="1.0">
      <label>Tempo 4 de 4: 5 min</label>
      <description>¡Último bloque! Fuerte hasta el final</description>
    </SteadyState>

    <!-- Recuperación: 3 minutos -->
    <SteadyState Duration="180" Power="0.55" pace="0.75">
      <label>Recuperación: 3 min</label>
    </SteadyState>

    <!-- Enfriamiento: 10 minutos -->
    <Cooldown Duration="600" PowerLow="0.60" PowerHigh="0.40" pace="0.75">
      <label>Enfriamiento: 10 min</label>
      <description>Vuelta a ritmo muy fácil, recuperate</description>
    </Cooldown>
  </workout>
</workout_file>"""

    return zwift_workout

def create_training_peaks_tcx():
    """Crear un workout en formato TrainingPeaks (.tcx)"""
    # FTP estimado basado en velocidad
    ftp = 250

    tcx_workout = """<?xml version="1.0" encoding="UTF-8"?>
<TrainingCenterDatabase xmlns="http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2">
  <Workouts>
    <Workout Sport="Biking">
      <Name>Martes - Esfuerzo Anaeróbico</Name>
      <Step>
        <Name>Calentamiento</Name>
        <Duration>600</Duration>
        <Intensity>Easy</Intensity>
        <Target Zone="1"/>
      </Step>
      <Step>
        <Name>Tempo 1/4</Name>
        <Duration>300</Duration>
        <Intensity>Hard</Intensity>
        <Target Zone="4"/>
      </Step>
      <Step>
        <Name>Recuperación</Name>
        <Duration>180</Duration>
        <Intensity>Easy</Intensity>
        <Target Zone="1"/>
      </Step>
      <Step>
        <Name>Tempo 2/4</Name>
        <Duration>300</Duration>
        <Intensity>Hard</Intensity>
        <Target Zone="4"/>
      </Step>
      <Step>
        <Name>Recuperación</Name>
        <Duration>180</Duration>
        <Intensity>Easy</Intensity>
        <Target Zone="1"/>
      </Step>
      <Step>
        <Name>Tempo 3/4</Name>
        <Duration>300</Duration>
        <Intensity>Hard</Intensity>
        <Target Zone="4"/>
      </Step>
      <Step>
        <Name>Recuperación</Name>
        <Duration>180</Duration>
        <Intensity>Easy</Intensity>
        <Target Zone="1"/>
      </Step>
      <Step>
        <Name>Tempo 4/4</Name>
        <Duration>300</Duration>
        <Intensity>Hard</Intensity>
        <Target Zone="4"/>
      </Step>
      <Step>
        <Name>Recuperación</Name>
        <Duration>180</Duration>
        <Intensity>Easy</Intensity>
        <Target Zone="1"/>
      </Step>
      <Step>
        <Name>Enfriamiento</Name>
        <Duration>600</Duration>
        <Intensity>Easy</Intensity>
        <Target Zone="1"/>
      </Step>
    </Workout>
  </Workouts>
</TrainingCenterDatabase>"""

    return tcx_workout

def create_json_workout():
    """Crear un workout en formato JSON para referencia"""
    workout = {
        "name": "Martes - Esfuerzo Anaeróbico",
        "type": "anaerobic",
        "duration_minutes": 77,
        "total_distance_km": 45,
        "difficulty": "Hard",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "description": "Sesión de esfuerzo a ritmo tempo con 4x5 minutos de high intensity",
        "zones": {
            "easy": "~17 km/h",
            "moderate": "~20 km/h",
            "tempo": "~23 km/h",
            "hard": "~26 km/h"
        },
        "segments": [
            {
                "name": "Calentamiento",
                "duration_minutes": 15,
                "intensity": "Easy",
                "zone": "Z1-Z2",
                "speed_kmh": "17-20",
                "description": "Ritmo fácil, deja que el cuerpo se adapte"
            },
            {
                "name": "Tempo 1/4",
                "duration_minutes": 5,
                "intensity": "Hard",
                "zone": "Z4",
                "speed_kmh": "26",
                "description": "Ritmo fuerte pero controlado"
            },
            {
                "name": "Recuperación",
                "duration_minutes": 3,
                "intensity": "Easy",
                "zone": "Z2",
                "speed_kmh": "17"
            },
            {
                "name": "Tempo 2/4",
                "duration_minutes": 5,
                "intensity": "Hard",
                "zone": "Z4",
                "speed_kmh": "26"
            },
            {
                "name": "Recuperación",
                "duration_minutes": 3,
                "intensity": "Easy",
                "zone": "Z2",
                "speed_kmh": "17"
            },
            {
                "name": "Tempo 3/4",
                "duration_minutes": 5,
                "intensity": "Hard",
                "zone": "Z4",
                "speed_kmh": "26"
            },
            {
                "name": "Recuperación",
                "duration_minutes": 3,
                "intensity": "Easy",
                "zone": "Z2",
                "speed_kmh": "17"
            },
            {
                "name": "Tempo 4/4",
                "duration_minutes": 5,
                "intensity": "Hard",
                "zone": "Z4",
                "speed_kmh": "26"
            },
            {
                "name": "Recuperación",
                "duration_minutes": 3,
                "intensity": "Easy",
                "zone": "Z2",
                "speed_kmh": "17"
            },
            {
                "name": "Enfriamiento",
                "duration_minutes": 10,
                "intensity": "Easy",
                "zone": "Z1-Z2",
                "speed_kmh": "15-18",
                "description": "Vuelta a ritmo muy fácil"
            }
        ],
        "total_time_minutes": 77,
        "estimated_distance_km": 45,
        "equipment": "Bicicleta (ruta o rodillo)",
        "notes": "Esta es tu primera sesión del nuevo plan. Mantén un ritmo controlado."
    }

    return json.dumps(workout, indent=2, ensure_ascii=False)

def create_readable_guide():
    """Crear una guía legible del entrenamiento"""
    guide = """
╔══════════════════════════════════════════════════════════════════════════╗
║                 SESIÓN: MARTES - ESFUERZO ANAERÓBICO                    ║
║                                                                          ║
║  Primera sesión del nuevo plan - Hoy: Sábado (por la lluvia)           ║
╚══════════════════════════════════════════════════════════════════════════╝

📊 RESUMEN:
  • Duración total: 77 minutos
  • Distancia estimada: 45-50 km
  • Tipo: Entrenamiento de intensidad
  • Intensidad: DURA (pero manejable)
  • Equipo: Bicicleta en rodillo/trainer o ruta con control de ritmo
  • Objetivo: Mejorar resistencia anaeróbica y velocidad de umbral

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 ESTRUCTURA DEL ENTRENAMIENTO:

┌─────────────────────────────────────────────────────────────────────────┐
│ FASE 1: CALENTAMIENTO (15 minutos)                                      │
├─────────────────────────────────────────────────────────────────────────┤
│ Ritmo:        FÁCIL - 17-20 km/h                                        │
│ Sensación:    Puedes hablar sin problemas                               │
│ Watts:        50-65% FTP (130-160 watts aprox.)                         │
│ Objetivo:     Aumentar frecuencia cardíaca gradualmente                 │
│ Tips:         • Mueve las piernas lentamente                            │
│               • Aumenta cadencia gradualmente                           │
│               • Siente el cuerpo adaptándose                            │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│ FASE 2: BLOQUE DE TEMPO x4 (32 minutos total)                           │
├─────────────────────────────────────────────────────────────────────────┤
│ CICLO REPETIDO 4 VECES:                                                 │
│                                                                         │
│   Tempo (5 min):     FUERTE - 26 km/h                                   │
│   ├─ Ritmo:          Tempo/Umbral                                       │
│   ├─ Sensación:      Puedes hablar pero con esfuerzo                    │
│   ├─ Watts:          90% FTP (225 watts aprox.)                         │
│   ├─ RPE:            7-8 de 10                                          │
│   └─ Tips:           • Mantén cadencia constante                        │
│                      • Respira profundo                                 │
│                      • Focal: piernas, no brazos                        │
│                                                                         │
│   Recuperación (3 min): FÁCIL - 17 km/h                                 │
│   ├─ Ritmo:          Muy suave                                          │
│   ├─ Sensación:      Recuperación                                       │
│   ├─ Watts:          55% FTP (140 watts aprox.)                         │
│   └─ Tips:           • Baja cadencia                                    │
│                      • Deja que FC baje un poco                         │
│                      • Prepárate para el siguiente tempo                │
│                                                                         │
│ DISTRIBUCIÓN:                                                           │
│   Rep 1:  Tempo → Recup (8 min)  |  Rep 3:  Tempo → Recup (8 min)      │
│   Rep 2:  Tempo → Recup (8 min)  |  Rep 4:  Tempo → Recup (8 min)      │
│                                                                         │
│ Progresión mental:                                                      │
│   Rep 1: "Fácil, voy a poder"                                          │
│   Rep 2: "Ahora pesa más, pero sigo"                                   │
│   Rep 3: "La mitad! Aguanta"                                           │
│   Rep 4: "¡Último! Fuerte al final"                                    │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│ FASE 3: ENFRIAMIENTO (10 minutos)                                       │
├─────────────────────────────────────────────────────────────────────────┤
│ Ritmo:        MUY FÁCIL - 15-18 km/h                                    │
│ Sensación:    Recuperación completa                                     │
│ Watts:        40-60% FTP (100-150 watts aprox.)                         │
│ Objetivo:     Bajar frecuencia cardíaca lentamente                      │
│ Tips:         • Pedala suave                                            │
│               • Baja cadencia                                           │
│               • Hidratación                                             │
│               • Deja que el cuerpo se recupere                          │
└─────────────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💪 CONSEJOS PRÁCTICOS:

✓ ANTES DEL ENTRENAMIENTO:
  • Come algo ligero 60-90 min antes
  • Hidratación: 500ml de agua
  • Estiramiento dinámico (5 min)
  • Verifica tu equipo

✓ DURANTE:
  • Usa una botella de agua en el rodillo
  • Ten una toalla cerca
  • Mantén la cadencia 90-100 rpm
  • No mires TV (foco en el esfuerzo)
  • Si sientes mareos, baja intensidad

✓ DESPUÉS:
  • Enfriamiento activo (5-10 min más fácil)
  • Hidratación: 1L de agua + electrolitos
  • Come proteína + carbohidrato en 30 min
  • Estiramiento suave (10 min)
  • Registra en Strava

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📱 CÓMO IMPORTAR EN APPS:

ZWIFT:
  1. Descarga: "martes_anaerobic.zwo"
  2. Ve a: Documentos/Zwift/Workouts/
  3. Pega el archivo
  4. En Zwift: Busca "Martes - Esfuerzo Anaeróbico"

TRAINING PEAKS / GARMIN:
  1. Descarga: "martes_anaerobic.tcx"
  2. En TrainingPeaks: Click en "Import Workout"
  3. Sube el archivo .tcx
  4. El entrenamiento aparecerá en tu calendario

WAHOO (Elemnt/KICKR):
  1. Usa el archivo .tcx
  2. Sube en Wahoo Fitness app
  3. Sincroniza con tu Elemnt

MANUAL (en cualquier app):
  1. Sigue los tiempos y ritmos de la guía
  2. Registra manualmente cada segmento
  3. Nota: Menos preciso pero funciona

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 OBJETIVOS DE ESTA SESIÓN:

✓ Primaria: Acostumbrarte al nuevo sistema de entrenamiento
✓ Secundaria: Mejorar tu potencia en zona Z4 (umbral)
✓ Mental: Ganar confianza en seguir un plan estructurado

Después de esto, tendrás 6 días de recuperación antes de la próxima.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  NOTAS IMPORTANTES:

• Este es tu PRIMER día del plan nuevo - ¡No hagas más del 100%!
• Si sientes dolor (no fatiga), detente
• Las respiraciones profundas son clave en tempo
• Registra cómo te sientes (RPE, FC, cadencia)
• Ajustaremos el plan basado en tu feedback

¡Que disfrutes! 💪

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    return guide

def main():
    print("Generando archivos de entrenamiento...\n")

    # Generar Zwift
    zwift_content = create_zwift_workout()
    with open('martes_anaerobic.zwo', 'w') as f:
        f.write(zwift_content)
    print("✓ martes_anaerobic.zwo (para Zwift)")

    # Generar TrainingPeaks/Garmin
    tcx_content = create_training_peaks_tcx()
    with open('martes_anaerobic.tcx', 'w') as f:
        f.write(tcx_content)
    print("✓ martes_anaerobic.tcx (para TrainingPeaks, Garmin, Wahoo)")

    # Generar JSON
    json_content = create_json_workout()
    with open('martes_anaerobic.json', 'w') as f:
        f.write(json_content)
    print("✓ martes_anaerobic.json (referencia estructurada)")

    # Generar guía legible
    guide_content = create_readable_guide()
    with open('MARTES_GUIA_ENTRENAMIENTO.txt', 'w') as f:
        f.write(guide_content)
    print("✓ MARTES_GUIA_ENTRENAMIENTO.txt (guía para leer)")

    # Mostrar la guía en pantalla
    print("\n" + guide_content)

if __name__ == '__main__':
    main()
