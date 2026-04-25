#!/usr/bin/env python3
"""
Sesión 60 min para rodillo inteligente con control de potencia (modo ERG).
FTP real estimado: 155W (basado en mejor esfuerzo de 57 min = 163W × 0.95)

Zonas de potencia:
  Z1 recuperación:  <93W   (<60% FTP)
  Z2 aeróbico:      93-124W (60-80%)
  Z3 sweet spot:    124-140W (80-90%)  ← sesión de hoy
  Z4 umbral:        140-163W (90-105%)
  Z5 VO2max:        >163W
"""

from fit_tool.fit_file_builder import FitFileBuilder
from fit_tool.profile.messages.file_id_message import FileIdMessage
from fit_tool.profile.messages.workout_message import WorkoutMessage
from fit_tool.profile.messages.workout_step_message import WorkoutStepMessage
from fit_tool.profile.profile_type import (
    FileType, Sport, WorkoutStepDuration, WorkoutStepTarget, Intensity, Manufacturer
)
import time

FTP = 180  # Watts — confirmado por el usuario

def pct(p):
    """Potencia en watts como % del FTP"""
    return int(FTP * p)

def build_fit():
    builder = FitFileBuilder(auto_define=True)

    file_id = FileIdMessage()
    file_id.type = FileType.WORKOUT
    file_id.manufacturer = Manufacturer.DEVELOPMENT
    file_id.product = 0
    builder.add(file_id)

    wkt = WorkoutMessage()
    wkt.sport = Sport.CYCLING
    wkt.num_valid_steps = 8
    wkt.wkt_name = "Sab Resistencia Cadencia 60min"
    builder.add(wkt)

    def step(name, secs, intensity, watts_low, watts_high):
        s = WorkoutStepMessage()
        s.wkt_step_name = name
        s.duration_type = WorkoutStepDuration.TIME
        s.duration_value = secs * 1000          # milisegundos
        s.intensity = intensity
        s.target_type = WorkoutStepTarget.POWER
        s.custom_target_value_low  = watts_low  + 1000  # FIT offset para watts
        s.custom_target_value_high = watts_high + 1000
        builder.add(s)

    #  Segmento             duración  intensidad         watts low   watts high
    step("Calentamiento",   10*60, Intensity.WARMUP,    pct(0.50), pct(0.65))
    step("Bloque1 Z3",      12*60, Intensity.ACTIVE,    pct(0.80), pct(0.87))
    step("Recuperacion 1",   3*60, Intensity.REST,       pct(0.50), pct(0.58))
    step("Bloque2 Z3+",     12*60, Intensity.ACTIVE,    pct(0.84), pct(0.90))
    step("Recuperacion 2",   3*60, Intensity.REST,       pct(0.50), pct(0.58))
    step("Bloque3 Z3",      12*60, Intensity.ACTIVE,    pct(0.80), pct(0.87))
    step("Recuperacion 3",   3*60, Intensity.REST,       pct(0.50), pct(0.58))
    step("Enfriamiento",     5*60, Intensity.COOLDOWN,   pct(0.40), pct(0.55))

    fit = builder.build()
    fname = "sabado_resistencia_cadencia.fit"
    fit.to_file(fname)
    return fname

def print_guide():
    z = {
        "cal_lo":  pct(0.50), "cal_hi":  pct(0.65),
        "b1_lo":   pct(0.80), "b1_hi":   pct(0.87),
        "b2_lo":   pct(0.84), "b2_hi":   pct(0.90),
        "rec_lo":  pct(0.50), "rec_hi":  pct(0.58),
        "cool_lo": pct(0.40), "cool_hi": pct(0.55),
    }

    print(f"""
╔══════════════════════════════════════════════════════════════════╗
║   SESIÓN HOY — SÁBADO  · Rodillo inteligente (ERG)             ║
║   60 min  ·  Resistencia + Cadencia Alta  ·  FTP: {FTP}W       ║
╚══════════════════════════════════════════════════════════════════╝

TUS DATOS (Strava):
  Cadencia habitual: 79 rpm  → hoy apuntamos a 88-95 rpm
  Potencia media:    110 W   (la mayoría vas por debajo del FTP)
  FTP estimado:      {FTP} W (basado en mejor esfuerzo 57min: 163W)

ESTRUCTURA — 60 MINUTOS:
──────────────────────────────────────────────────────────────────
 0:00  CALENTAMIENTO       10 min
       Potencia: {z["cal_lo"]}-{z["cal_hi"]} W  |  Cadencia: libre
       → El rodillo aplica resistencia baja automáticamente (ERG)

10:00  BLOQUE 1  Z3        12 min
       Potencia: {z["b1_lo"]}-{z["b1_hi"]} W  |  Cadencia: 88-95 rpm  |  RPE: 6/10
       → El truco: sube la cadencia para alcanzar los watts,
         no "pises" más fuerte. Así entrenas resistencia sin fuerza.

22:00  RECUPERACIÓN         3 min
       Potencia: {z["rec_lo"]}-{z["rec_hi"]} W  |  Cadencia: libre

25:00  BLOQUE 2  Z3+       12 min  ← un escalón más
       Potencia: {z["b2_lo"]}-{z["b2_hi"]} W  |  Cadencia: 88-95 rpm  |  RPE: 7/10
       → Si la cadencia baja de 88, baja marcha en el rodillo.
         El objetivo es mantener rpm, no luchar con la resistencia.

37:00  RECUPERACIÓN         3 min
       Potencia: {z["rec_lo"]}-{z["rec_hi"]} W

40:00  BLOQUE 3  Z3        12 min  ← consolida lo aprendido
       Potencia: {z["b1_lo"]}-{z["b1_hi"]} W  |  Cadencia: 88-95 rpm  |  RPE: 6-7/10
       → Aquí verás si la resistencia aguanta. Mantén cadencia
         aunque las piernas estén cansadas.

52:00  RECUPERACIÓN         3 min

55:00  ENFRIAMIENTO         5 min
       Potencia: {z["cool_lo"]}-{z["cool_hi"]} W  |  Cadencia: libre
──────────────────────────────────────────────────────────────────
Total: 36 min en zona Z3 · 9 min recuperación · 15 min cal/enfr

POR QUÉ ESTO MEJORA TUS DEBILIDADES:
  RESISTENCIA:   3 bloques de 12 min en sweet spot (80-90% FTP)
                 quema carbohidratos eficientemente, adapta
                 las fibras musculares a esfuerzo sostenido
  FUERZA:        NO la trabajamos hoy. La cadencia alta reduce
                 el torque por pedalada → protege tus piernas
                 y te permite acumular más minutos de calidad
  CADENCIA:      Usas tu punto fuerte para sostener la potencia
                 → ganas confianza y técnica de pedalada

CÓMO IMPORTAR EN HAMMERHEAD KAROO:
  Opción A — Directo:
    1. account.hammerhead.io → Library → Workouts → Import
    2. Sube: sabado_resistencia_cadencia.fit
    3. En el Karoo: Plan a Ride → Workout

  Opción B — Vía TrainingPeaks (si tienes cuenta):
    1. Sube el .fit a TrainingPeaks
    2. Karoo → Settings → Connected Accounts → TrainingPeaks
    3. Sincroniza y el workout aparece automáticamente

  ⚠ En el Karoo activa modo ERG para que el rodillo
    controle la potencia automáticamente.
""")

def pct(p):
    return int(FTP * p)

if __name__ == '__main__':
    print("Generando workout con potencia...")
    try:
        fname = build_fit()
        print(f"✓ {fname}  listo para importar en Hammerhead")
    except Exception as e:
        print(f"Error: {e}")
    print_guide()
