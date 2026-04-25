#!/usr/bin/env python3
"""
Genera index.html en reports/ listando todos los análisis disponibles
en orden descendente (más reciente primero).
"""
import os
from datetime import datetime
from pathlib import Path

def generar_indice():
    reports_dir = Path(__file__).parent.parent / 'reports'
    reports_dir.mkdir(exist_ok=True)

    # Obtener carpetas con formato YYYY-MM-DD
    carpetas = []
    for item in reports_dir.iterdir():
        if item.is_dir():
            try:
                # Validar formato fecha
                datetime.strptime(item.name, '%Y-%m-%d')
                carpetas.append(item.name)
            except ValueError:
                pass

    # Ordenar descendente (más reciente primero)
    carpetas.sort(reverse=True)

    # HTML
    rows = []
    for fecha in carpetas:
        # Convertir a formato legible
        dt = datetime.strptime(fecha, '%Y-%m-%d')
        fecha_legible = dt.strftime('%A, %d de %B de %Y').capitalize()
        dias_ago = (datetime.now() - dt).days

        if dias_ago == 0:
            cuando = '🔴 Hoy'
        elif dias_ago == 1:
            cuando = '🟡 Ayer'
        else:
            cuando = f'⚪ Hace {dias_ago} días'

        rows.append(f'''
    <tr>
      <td class="fecha">{fecha}</td>
      <td class="dia">{fecha_legible}</td>
      <td class="cuando">{cuando}</td>
      <td class="accion">
        <a href="./{fecha}/analisis.html" class="btn">📊 Ver análisis</a>
      </td>
    </tr>''')

    html = f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Training Reports — Historial de Análisis</title>
  <style>
    :root {{
      --bg: #0f1117;
      --card: #1a1d2e;
      --accent: #f97316;
      --text: #e2e8f0;
      --muted: #64748b;
      --border: #2d3148;
      --hover: #2d3148;
    }}

    * {{
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }}

    body {{
      background: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      padding: 24px;
      max-width: 900px;
      margin: 0 auto;
      line-height: 1.6;
    }}

    h1 {{
      font-size: 1.8rem;
      font-weight: 700;
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .subtitle {{
      color: var(--muted);
      font-size: 0.95rem;
      margin-bottom: 28px;
    }}

    .info-box {{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 16px 20px;
      margin-bottom: 28px;
      font-size: 0.9rem;
      line-height: 1.6;
    }}

    .info-box strong {{
      color: var(--accent);
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 12px;
      overflow: hidden;
    }}

    thead {{
      background: var(--border);
    }}

    th {{
      padding: 16px;
      text-align: left;
      font-weight: 600;
      font-size: 0.85rem;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}

    td {{
      padding: 14px 16px;
      border-top: 1px solid var(--border);
      vertical-align: middle;
    }}

    tr:hover {{
      background: var(--hover);
    }}

    .fecha {{
      font-weight: 600;
      color: var(--accent);
      font-family: 'Courier New', monospace;
    }}

    .dia {{
      color: var(--text);
    }}

    .cuando {{
      color: var(--muted);
      font-size: 0.85rem;
    }}

    .btn {{
      display: inline-block;
      padding: 8px 16px;
      background: var(--accent);
      color: #000;
      border-radius: 6px;
      text-decoration: none;
      font-size: 0.85rem;
      font-weight: 600;
      transition: all 0.2s;
    }}

    .btn:hover {{
      transform: scale(1.05);
      box-shadow: 0 4px 12px rgba(249, 115, 22, 0.3);
    }}

    .empty {{
      text-align: center;
      padding: 40px 20px;
      color: var(--muted);
    }}

    .empty-icon {{
      font-size: 3rem;
      margin-bottom: 16px;
      opacity: 0.5;
    }}

    footer {{
      margin-top: 40px;
      padding-top: 20px;
      border-top: 1px solid var(--border);
      font-size: 0.85rem;
      color: var(--muted);
      text-align: center;
    }}

    @media (max-width: 768px) {{
      body {{
        padding: 16px;
      }}

      h1 {{
        font-size: 1.4rem;
      }}

      table {{
        font-size: 0.85rem;
      }}

      th, td {{
        padding: 10px 12px;
      }}

      .dia {{
        display: none;
      }}
    }}
  </style>
</head>
<body>

<h1>🚴 Training Reports</h1>
<div class="subtitle">Historial de análisis de entrenamientos</div>

<div class="info-box">
  <strong>📊 {len(carpetas)} análisis</strong> registrados.
  Haz clic en cualquier fecha para ver el análisis detallado con gráficas.
</div>

<table>
  <thead>
    <tr>
      <th>Fecha</th>
      <th class="fecha-col">Día</th>
      <th>Cuándo</th>
      <th>Acción</th>
    </tr>
  </thead>
  <tbody>
    {"".join(rows) if carpetas else '''
    <tr>
      <td colspan="4">
        <div class="empty">
          <div class="empty-icon">📭</div>
          <p>Aún no hay análisis. Completa tu primer entrenamiento y ejecuta:</p>
          <p style="margin-top: 8px; font-family: monospace;">python3 run_analysis.py</p>
        </div>
      </td>
    </tr>
    '''}
  </tbody>
</table>

<footer>
  <p>🏠 <a href="../" style="color: var(--accent); text-decoration: none;">Volver al proyecto</a></p>
  <p style="margin-top: 8px;">Actualizado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
</footer>

</body>
</html>'''

    # Guardar
    index_file = reports_dir / 'index.html'
    with open(index_file, 'w') as f:
        f.write(html)

    print(f"✓ Índice generado: {index_file}")
    return True

if __name__ == '__main__':
    generar_indice()
