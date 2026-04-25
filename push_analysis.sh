#!/bin/bash
set -e

echo "🚴 Training Analysis Pipeline"
echo "─────────────────────────────"

# Generar análisis
echo "📊 Analizando última sesión de Strava..."
python3 run_analysis.py

# Detectar cambios en reportes
echo ""
echo "🔍 Detectando nuevos reportes..."

if git diff --quiet reports/ 2>/dev/null; then
    echo "✓ No hay cambios nuevos"
    exit 0
fi

# Commit y push
echo "📤 Subiendo a GitHub..."
git add reports/
DATE=$(date +%Y-%m-%d)
git commit -m "Análisis $DATE"
git push

echo ""
echo "✅ Publicado en GitHub Pages"
echo "📱 Ver en: https://hugorey.github.io/training/reports/"
