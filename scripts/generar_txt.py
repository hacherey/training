#!/usr/bin/env python3
"""Helper para generar análisis.txt más limpio."""
import json
from pathlib import Path
from datetime import datetime

def simplificar_analisis(txt_file):
    """Lee el txt generado y lo simplifica, manteniendo solo lo esencial."""
    with open(txt_file) as f:
        contenido = f.read()

    lineas = contenido.split('\n')
    salida = []

    # Mantener header
    salida.extend(lineas[:3])  # Título y FTP
    salida.append("")

    # Ir directamente a TENDENCIAS
    en_tendencias = False
    for l in lineas:
        if 'TENDENCIAS' in l:
            en_tendencias = True

        if en_tendencias:
            if l.startswith('✓') or l.startswith('⚠') or l.startswith('~'):
                salida.append(l)
            elif l.startswith('Generado'):
                salida.append("")
                salida.append(l)
                break

    resultado = "\n".join(salida)

    with open(txt_file, 'w') as f:
        f.write(resultado)

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        simplificar_analisis(sys.argv[1])
