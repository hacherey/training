# 🚴 Training Analytics System

Personal cycling training platform que conecta con Strava, genera planes de entrenamiento personalizados y analiza cada sesión en detalle.

**Usuario:** Hugo | **FTP:** 180W | **Cyclocomputer:** Hammerhead Karoo

---

## 📁 Estructura

```
training/
├── scripts/          # Scripts ejecutables (análisis, OAuth, etc.)
├── workouts/         # Archivos .zwo para importar en Karoo
├── reports/          # Análisis HTML generados (uno por fecha)
│   └── YYYY-MM-DD/
│       └── analisis.html  ← Abierto en navegador/móvil
├── docs/             # Documentación
└── data_key.properties  (⚠️ NO subido a git — local only)
```

---

## 🚀 Quick Start

### 1. Primera vez — Setup

```bash
cd training
pip install -r scripts/requirements.txt
python3 scripts/strava_oauth.py
```

Se abrirá tu navegador → autoriza la app → el token se guarda automáticamente.

### 2. Después de cada entrenamiento

```bash
python3 run_analysis.py
```

Esto:
- Descarga tu último entrenamiento de Strava
- Genera `reports/YYYY-MM-DD/analisis.html`
- Abre el reporte en el navegador

### 3. Ver en el móvil

Abre tu navegador → `hugorey.github.io/training/reports/` → selecciona la fecha

---

## 📊 Plan de Entrenamiento

**8 semanas de progresión** con 4 sesiones/semana:

| Día | Sesión | Duración | Enfoque |
|-----|--------|----------|---------|
| **Mar** | A (intervalos) | 42-60 min | Progresa cada semana |
| **Jue** | B (base Z2) | 45 min | Aeróbico recuperativo |
| **Sab** | C (cadencia) | 50 min | Técnica neuromuscular |
| **Dom** | D (larga) | 75 min | Resistencia general |

**Estructura de archivos:**
- `workouts/S01A_*.zwo` → importa en Hammerhead cada martes
- `workouts/S0xB/C/D_base.zwo` → reutiliza toda la semana

---

## 📈 Análisis de Sesiones

Cada reporte HTML incluye:

- **Gráficas:** Potencia, Cadencia, FC en tiempo real
- **Métricas clave:**
  - **NP** = Potencia Normalizada (potencia equivalente sostenida)
  - **IF** = Intensity Factor (0.75 fácil, 0.95 competición)
  - **TSS** = Training Stress Score (carga acumulable)
  - **VAM** = Velocidad Ascensional Media (m/h)
- **Análisis de FC:** zonas, recuperación, alertas
- **Cadencia:** % tiempo en zona 88-95 rpm (objetivo)

---

## 🔐 Secrets (NO subir a git)

`data_key.properties` contiene:
- `client_id`, `client_secret` (app Strava)
- `token`, `refresh_token` (OAuth)

Está en `.gitignore`. Si necesitas regenerar:
```bash
python3 scripts/strava_oauth.py
```

---

## 🌍 GitHub Pages (Seguimiento en móvil)

Los reportes se publican automáticamente en:
```
https://hugorey.github.io/training/reports/
```

Cada análisis queda en su carpeta por fecha, accesible desde el celular.

---

## 🛠️ Desarrollo

Ver `docs/setup.md` para:
- Cómo regenerar plans de entrenamiento
- Cómo ajustar FTP o zonas
- Scripts disponibles en `scripts/`
- Formatos de archivo (.zwo, .fit)

---

**Última actualización:** 2026-04-25
