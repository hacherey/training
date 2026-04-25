# Setup y Configuración

## Instalación Inicial

### 1. Dependencias

```bash
pip install -r scripts/requirements.txt
```

Esto instala:
- `requests` — llamadas HTTP a API de Strava
- `fit-tool` — genera archivos FIT para Karoo
- `fitparse` — parsea FIT para validar

### 2. Obtener credenciales de Strava

1. Ve a [strava.com/settings/api](https://strava.com/settings/api)
2. Crea una aplicación si no tienes
3. Nota: 
   - **Client ID** y **Client Secret** (en pantalla)
   - **Authorization Callback Domain:** `http://localhost:8080`

4. Ejecuta:
   ```bash
   python3 scripts/strava_oauth.py
   ```
5. Se abre tu navegador → autoriza → los credenciales se guardan en `data_key.properties`

---

## Flujo Diario

### Después de cada entrenamiento en Hammerhead

```bash
python3 run_analysis.py
```

**Qué hace:**
1. Refresca el token de Strava automáticamente
2. Descarga tu último entrenamiento
3. Calcula NP, IF, TSS, VAM, análisis de FC
4. Genera HTML con gráficas en `reports/YYYY-MM-DD/analisis.html`
5. Abre en navegador

**Archivo guardado:**
```
reports/2026-04-25/analisis.html  ← verlo en el celular después
```

---

## Planes y Workouts

### Generar plan de 8 semanas

```bash
python3 scripts/plan_progresion.py
```

Genera todos los archivos `.zwo` en `workouts/`:
- `S01A_6x4min_80pct.zwo` ← Semana 1
- `S02A_6x5min_80pct.zwo` ← Semana 2
- ... hasta `S08A_3x12min_85pct.zwo`

(B, C, D son fijas y se reutilizan)

### Importar en Hammerhead

1. Ve a `account.hammerhead.io`
2. Library → Workouts → Import
3. Sube `workouts/S0xA_*.zwo`
4. En el Karoo: Plan a Ride → Workout

---

## Configurar GitHub Pages (reportes en móvil)

### 1. Crear repositorio en GitHub

```bash
git remote add origin https://github.com/tuusuario/training.git
git branch -M main
git push -u origin main
```

### 2. Habilitar Pages

En GitHub:
1. Settings → Pages
2. Build and Deployment → Source: `Deploy from a branch`
3. Branch: `main` / folder: `/ (root)`
4. Save

Tu sitio estará en: `https://tuusuario.github.io/training/`

### 3. Acceder desde el móvil

```
https://tuusuario.github.io/training/reports/
```

Ahí verás todas las fechas con análisis disponibles.

---

## Personalización

### Cambiar FTP

El FTP está definido en:
- `scripts/analisis_sesion.py` línea ~79: `FTP = 180`
- `scripts/plan_progresion.py` línea ~11: `FTP = 180`
- `CLAUDE.md` → "Key Constants"

Cámbialo en ambos scripts si haces un test formal.

### Cambiar cadencia objetivo

Objetivo actual: 88-95 rpm

Cambiar en:
- `scripts/plan_progresion.py` → los `.zwo` generados
- `scripts/analisis_sesion.py` → análisis de sesión
- `CLAUDE.md`

### Cambiar HRmax

```python
HR_MAX = 185  # en scripts/analisis_sesion.py
```

Si Strava reporta un valor mayor, se usa ese automáticamente.

---

## Troubleshooting

### "Token expired" / OAuth falla

```bash
python3 scripts/strava_oauth.py
```

Vuelve a autorizar. Los nuevos credenciales se guardan automáticamente.

### Hammerhead rechaza el .zwo

- Verifica que FTP en Karoo = 180W
- Los %.zwo usan % de FTP, no watts absolutos
- Prueba reimportar

### HTML no se abre

```bash
open reports/2026-04-25/analisis.html
```

O en navegador: `File → Open → reports/...`

---

## Scripts disponibles

| Script | Propósito | Cuándo |
|--------|-----------|--------|
| `run_analysis.py` | Ejecutar análisis último entreno | **Después de cada sesión** |
| `scripts/analisis_sesion.py` | Core del análisis | Importado por run_analysis.py |
| `scripts/plan_progresion.py` | Generar 8 semanas de workouts | Una sola vez, o si cambias el plan |
| `scripts/strava_oauth.py` | Refrescar credenciales Strava | Si token expira |
| `scripts/strava_analyzer.py` | Descargar todos los entrenamientos | Análisis histórico (raro) |

---

## Estructura de carpetas — Reglas

```
workouts/          ← .zwo importables (git tracked)
reports/           ← HTML análisis (git tracked, público en Pages)
  YYYY-MM-DD/
    analisis.html

scripts/           ← Python ejecutable (git tracked)
data_key.properties ← SECRETS (⚠️ .gitignore, NO subir)
strava_activities.json ← datos crudos (⚠️ .gitignore, no trackear)
```

---

**Ver también:** `CLAUDE.md` para arquitectura técnica.
