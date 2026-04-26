#!/usr/bin/env python3
"""
Wrapper para ejecutar analisis_sesion.py desde cualquier directorio.
Automáticamente:
1. Descarga el último entrenamiento de Strava
2. Genera HTML con gráficas
3. Guarda en reports/YYYY-MM-DD/analisis.html
"""
import sys
import os

# Agregar scripts/ al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))

# Cambiar al directorio raíz del proyecto
os.chdir(os.path.dirname(__file__))

# Importar y ejecutar
from analisis_sesion import main

if __name__ == '__main__':
    descargar = '--no-download' not in sys.argv
    main(descargar=descargar)
