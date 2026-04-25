# Configurar GitHub Pages — Reportes en el móvil

Los análisis se publican en una URL pública donde puedes verlos desde el celular.

---

## Paso 1: Crear repositorio en GitHub

1. Ve a [github.com/new](https://github.com/new)
2. **Repository name:** `training`
3. **Description:** `Cycling training analytics + Strava integration`
4. **Visibility:** Elige **Public** (para que GitHub Pages funcione)
5. **NO inicializar** con README (ya tenemos uno)
6. Clic en **Create repository**

---

## Paso 2: Conectar tu repositorio local

En la terminal:

```bash
git remote add origin https://github.com/TUUSUARIO/training.git
git branch -M main
git push -u origin main
```

Reemplaza `TUUSUARIO` con tu usuario de GitHub.

**Salida esperada:**
```
...
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

---

## Paso 3: Habilitar GitHub Pages

1. En GitHub, ve a tu repo: `github.com/TUUSUARIO/training`
2. Settings → Pages (lado izquierdo)
3. **Source:** Deploy from a branch
4. **Branch:** `main` / Folder: `/ (root)`
5. Clic en **Save**

GitHub generará una URL tipo:
```
https://TUUSUARIO.github.io/training/
```

**Espera 1-2 minutos** a que el sitio se genere.

---

## Paso 4: Acceder desde el navegador (PC o móvil)

```
https://TUUSUARIO.github.io/training/reports/
```

Verás una lista de carpetas por fecha:
```
2026-04-25/
2026-04-26/
...
```

Entra a cualquiera y abre `analisis.html`.

---

## Automatización: Push automático después de cada análisis

Actualmente haces:
```bash
python3 run_analysis.py      # genera HTML
git add reports/             # stagea el HTML nuevo
git commit -m "..."
git push                     # sube a GitHub
```

### Opción A — Manual (simple, sin automatización)

Cada sesión:
```bash
python3 run_analysis.py
git add reports/
git commit -m "Análisis $(date +%Y-%m-%d)"
git push
```

### Opción B — Script automático (recomendado)

Crea `push_analysis.sh` en la raíz:

```bash
#!/bin/bash
set -e

echo "Analizando última sesión..."
python3 run_analysis.py

echo "Detectando cambios..."
if git diff --quiet reports/; then
    echo "✓ No hay cambios nuevos en reportes"
else
    echo "Subiendo reporte a GitHub..."
    git add reports/
    git commit -m "Análisis $(date +%Y-%m-%d)"
    git push
    echo "✓ Publicado en https://hugorey.github.io/training/reports/"
fi
```

Hazlo ejecutable:
```bash
chmod +x push_analysis.sh
```

Y úsalo:
```bash
./push_analysis.sh
```

---

## Ver en el móvil

**iPhone/Android:**
1. Abre navegador
2. Ve a `https://TUUSUARIO.github.io/training/reports/`
3. Selecciona la fecha de hoy
4. Abre `analisis.html`
5. **Opcional:** Agrega a pantalla de inicio (Share → Add to Home Screen)

---

## Troubleshooting

### GitHub Pages no se genera

1. Verifica que **Source** esté en Settings → Pages
2. Espera 2-3 minutos
3. Verifica que el repo sea **Public**

### Ver progreso de deployment

En el repo de GitHub:
- Pestaña **Actions**
- Verás un workflow `pages build and deployment`
- Si muestra ✅ verde, ya está live

### Cambiar URL de Pages

Si quieres una URL personalizada (tudominio.com), ver Settings → Pages → Custom domain.

---

**Listo.** Después de cada entrenamiento:
1. `python3 run_analysis.py` genera el HTML
2. `./push_analysis.sh` lo sube a GitHub
3. Abre en móvil en 10 segundos

