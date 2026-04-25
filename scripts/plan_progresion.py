#!/usr/bin/env python3
"""
Genera sesión de hoy + plan de progresión 8 semanas.
FTP: 180W. Objetivo: pasar de intervalos cortos a bloques sostenidos.
4 sesiones/semana.
"""

FTP = 180

def pct(p): return round(p, 3)

# ─────────────────────────────────────────────────────────────
# TIPOS DE SESIÓN DE LA SEMANA
# ─────────────────────────────────────────────────────────────
# Sesión A: Intervalos de calidad (progresión principal)
# Sesión B: Base aeróbica Z2 (recuperación activa + resistencia)
# Sesión C: Cadencia / neuromuscular suave
# Sesión D: Sesión larga (exterior si no llueve, virtual si llueve)

def zwo_sesion_a(semana, reps, dur_min, potencia_pct, rec_min, desc_extra=""):
    """Sesión de intervalos — la que va progresando cada semana"""
    dur_s = int(dur_min * 60)
    rec_s = int(rec_min * 60)
    pow_val = pct(potencia_pct)
    watts = int(FTP * potencia_pct)
    watts_rec = int(FTP * 0.54)

    # Calentamiento + enfriamiento fijos
    cal_s = 600   # 10 min
    cool_s = 480  # 8 min

    total_min = (cal_s + reps * dur_s + (reps - 1) * rec_s + cool_s) // 60

    steps = [f'    <Warmup Duration="{cal_s}" PowerLow="0.5" PowerHigh="0.65"/>']
    for i in range(reps):
        steps.append(f'    <SteadyState Duration="{dur_s}" Power="{pow_val}" Cadence="92"/>')
        if i < reps - 1:
            steps.append(f'    <SteadyState Duration="{rec_s}" Power="0.54"/>')
    steps.append(f'    <Cooldown Duration="{cool_s}" PowerLow="0.4" PowerHigh="0.5"/>')

    steps_xml = "\n".join(steps)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<workout_file>\n'
        '  <author>Plan Progresion Hugo</author>\n'
        f'  <name>S{semana:02d}A Intervalos {reps}x{dur_min}min</name>\n'
        f'  <description>S{semana} · {reps}x{dur_min}min @ {int(potencia_pct*100)}% FTP ({watts}W) · rec {rec_min}min · Total ~{total_min}min. {desc_extra}</description>\n'
        '  <sportType>cycling</sportType>\n'
        '  <tags/>\n'
        '  <workout>\n'
        f'{steps_xml}\n'
        '  </workout>\n'
        '</workout_file>'
    )

def zwo_sesion_b(semana):
    """Base aeróbica Z2 — 45 min constante, cadencia libre"""
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<workout_file>
  <author>Plan Progresion Hugo</author>
  <name>S{semana:02d}B Base Aerobica Z2</name>
  <description>S{semana} · 45min Z2 constante ({int(FTP*0.65)}-{int(FTP*0.75)}W) · Cadencia libre · Conversacional</description>
  <sportType>cycling</sportType>
  <tags/>
  <workout>
    <Warmup Duration="300" PowerLow="0.45" PowerHigh="0.60"/>
    <SteadyState Duration="2100" Power="0.68"/>
    <Cooldown Duration="300" PowerLow="0.45" PowerHigh="0.55"/>
  </workout>
</workout_file>'''

def zwo_sesion_c(semana):
    """Cadencia neuromuscular — series de alta cadencia, baja potencia"""
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<workout_file>
  <author>Plan Progresion Hugo</author>
  <name>S{semana:02d}C Cadencia Neuromuscular</name>
  <description>S{semana} · Trabajo de cadencia alta 95-105rpm · Baja potencia · 50min · Mejora eficiencia de pedalada</description>
  <sportType>cycling</sportType>
  <tags/>
  <workout>
    <Warmup Duration="600" PowerLow="0.45" PowerHigh="0.60"/>
    <SteadyState Duration="300" Power="0.62" Cadence="95"/>
    <SteadyState Duration="120" Power="0.50"/>
    <SteadyState Duration="300" Power="0.62" Cadence="100"/>
    <SteadyState Duration="120" Power="0.50"/>
    <SteadyState Duration="300" Power="0.62" Cadence="105"/>
    <SteadyState Duration="120" Power="0.50"/>
    <SteadyState Duration="300" Power="0.62" Cadence="100"/>
    <SteadyState Duration="120" Power="0.50"/>
    <SteadyState Duration="300" Power="0.62" Cadence="95"/>
    <Cooldown Duration="600" PowerLow="0.40" PowerHigh="0.55"/>
  </workout>
</workout_file>'''

def zwo_sesion_d(semana, dur_min=75):
    """Sesión larga — Z2 con picos. Para exterior o virtual"""
    dur_s = dur_min * 60 - 1200
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<workout_file>
  <author>Plan Progresion Hugo</author>
  <name>S{semana:02d}D Larga {dur_min}min</name>
  <description>S{semana} · {dur_min}min · Z2 base con 3 picos breves · Resistencia general</description>
  <sportType>cycling</sportType>
  <tags/>
  <workout>
    <Warmup Duration="600" PowerLow="0.45" PowerHigh="0.65"/>
    <SteadyState Duration="{dur_s // 4}" Power="0.67"/>
    <SteadyState Duration="180" Power="0.82"/>
    <SteadyState Duration="{dur_s // 4}" Power="0.67"/>
    <SteadyState Duration="180" Power="0.82"/>
    <SteadyState Duration="{dur_s // 4}" Power="0.67"/>
    <SteadyState Duration="180" Power="0.82"/>
    <SteadyState Duration="{dur_s // 4}" Power="0.67"/>
    <Cooldown Duration="600" PowerLow="0.40" PowerHigh="0.55"/>
  </workout>
</workout_file>'''

# ─────────────────────────────────────────────────────────────
# PLAN DE 8 SEMANAS
# ─────────────────────────────────────────────────────────────
# Progresión de la Sesión A (la clave):
#   S1:  6x4min  @ 80%  rec 2min  → base, familiarizarse
#   S2:  6x5min  @ 80%  rec 2min  → un min más por bloque
#   S3:  5x6min  @ 82%  rec 2min  → sube intensidad
#   S4:  5x7min  @ 82%  rec 2min  → más duración
#   S5:  4x8min  @ 83%  rec 3min  → bloques más largos
#   S6:  4x9min  @ 83%  rec 3min  → consolida
#   S7:  4x10min @ 84%  rec 3min  → acercándose al objetivo
#   S8:  3x12min @ 85%  rec 4min  → objetivo cumplido

PLAN = [
    # (reps, dur_min, pct_ftp, rec_min, notas)
    (1,  6, 4, 0.80, 2.0, "Primera sesion. Mantén cadencia 88-92rpm en cada bloque"),
    (2,  6, 5, 0.80, 2.0, "Un minuto más por bloque. Si pudo la semana pasada, puedes hoy"),
    (3,  5, 6, 0.82, 2.0, "Subimos 2% de potencia. 5 bloques, más intensidad"),
    (4,  5, 7, 0.82, 2.0, "7 min ya es territorio de resistencia real. Respira profundo"),
    (5,  4, 8, 0.83, 3.0, "Solo 4 bloques pero 8 min cada uno. Más recuperación"),
    (6,  4, 9, 0.83, 3.0, "9 min. Si llegas bien aquí, la semana 7 será cómoda"),
    (7,  4,10, 0.84, 3.0, "10 minutos sostenidos. El umbral empieza a ceder"),
    (8,  3,12, 0.85, 4.0, "3x12min — el objetivo original. Ahora lo puedes sostener"),
]

CALENDARIO = """
╔══════════════════════════════════════════════════════════════════════════╗
║           PLAN DE PROGRESIÓN 8 SEMANAS — 4 sesiones/semana             ║
║           FTP: 180W  ·  Objetivo: resistencia + cadencia               ║
╚══════════════════════════════════════════════════════════════════════════╝

ESTRUCTURA SEMANAL:
  Martes  → Sesión A: Intervalos de calidad (la que progresa)
  Jueves  → Sesión B: Base aeróbica Z2 (45 min, cómodo)
  Sábado  → Sesión C: Cadencia neuromuscular (50 min, técnica)
  Domingo → Sesión D: Larga (75-90 min, exterior o virtual)

  ⚠ Si no puedes 4 días, prioriza en este orden: A → D → B → C
  ⚠ Siempre al menos 1 día de descanso entre sesiones A

PROGRESIÓN SESIÓN A (intervalos — el núcleo del plan):
─────────────────────────────────────────────────────────────────────────
 S1  │ 6×4min  @ 80% (144W) │ rec 2min │ 42min total │ familiarizarse
 S2  │ 6×5min  @ 80% (144W) │ rec 2min │ 50min total │ +1min por bloque
 S3  │ 5×6min  @ 82% (148W) │ rec 2min │ 50min total │ +2% potencia
 S4  │ 5×7min  @ 82% (148W) │ rec 2min │ 55min total │ +1min por bloque
 S5  │ 4×8min  @ 83% (149W) │ rec 3min │ 52min total │ más recuperación
 S6  │ 4×9min  @ 83% (149W) │ rec 3min │ 56min total │ consolida
 S7  │ 4×10min @ 84% (151W) │ rec 3min │ 60min total │ territorio real
 S8  │ 3×12min @ 85% (153W) │ rec 4min │ 60min total │ OBJETIVO CUMPLIDO
─────────────────────────────────────────────────────────────────────────

SESIONES FIJAS (no cambian, son soporte):
  B: 45min Z2 constante · {z2_lo}-{z2_hi}W · conversacional
  C: 50min cadencia alta 95-105rpm · baja potencia
  D: 75min+ salida larga con 3 picos suaves

REGLA DE ORO:
  Si en la Sesión A no puedes completar el último bloque,
  repite esa semana antes de avanzar. No pases a la siguiente
  hasta terminar los reps completos.

ARCHIVOS ZWO GENERADOS:
""".format(z2_lo=int(FTP*0.65), z2_hi=int(FTP*0.75))


def main():
    import os
    os.makedirs("workouts", exist_ok=True)

    print("Generando workouts...")
    archivos = []

    for semana, reps, dur, pot, rec, nota in PLAN:
        # Sesión A
        fname = f"workouts/S{semana:02d}A_{reps}x{dur}min_{int(pot*100)}pct.zwo"
        content = zwo_sesion_a(semana, reps, dur, pot, rec, nota)
        with open(fname, 'w') as f:
            f.write(content)
        archivos.append(fname)

        # Sesiones B, C, D (solo generamos una vez, valen para todas las semanas)
        if semana == 1:
            for letra, fn in [("B", zwo_sesion_b), ("C", zwo_sesion_c)]:
                fname2 = f"workouts/S{semana:02d}{letra}_base.zwo"
                with open(fname2, 'w') as f:
                    f.write(fn(semana))
                archivos.append(fname2)

            fname3 = f"workouts/S{semana:02d}D_larga_75min.zwo"
            with open(fname3, 'w') as f:
                f.write(zwo_sesion_d(semana, 75))
            archivos.append(fname3)

    # Sesión de HOY (semana 1, sesión A)
    hoy = zwo_sesion_a(1, 6, 4, 0.80, 2.0, "Primera sesion. Mantén cadencia 88-92rpm")
    with open("sabado_resistencia_cadencia.zwo", 'w') as f:
        f.write(hoy)
    print("✓ sabado_resistencia_cadencia.zwo  ← SESIÓN DE HOY (actualizada)")

    print()
    print(CALENDARIO)
    for a in archivos:
        semana = int(a.split('/S')[1][:2])
        s, reps, dur, pot, rec, nota = next(x for x in PLAN if x[0] == semana)
        if 'A_' in a:
            watts = int(FTP * pot)
            print(f"  {a}  ({reps}x{dur}min @ {watts}W)")
        else:
            print(f"  {a}")

    print(f"""
CÓMO USAR:
  Cada semana importa el archivo S0xA en Hammerhead para el martes.
  Los archivos B, C, D los reutilizas todas las semanas (no cambian).
  Todos están en la carpeta workouts/
""")


if __name__ == '__main__':
    main()
