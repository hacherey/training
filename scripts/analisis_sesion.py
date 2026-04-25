#!/usr/bin/env python3
"""
Descarga el último entrenamiento de Strava y genera análisis HTML con gráficas.
"""
import requests
import json
from datetime import datetime

FTP    = 180
HR_MAX = 185  # estimado; se ajusta si Strava reporta uno mayor

# ── Auth ──────────────────────────────────────────────────────────────────────

def load_keys():
    keys = {}
    with open('data_key.properties') as f:
        for line in f:
            line = line.strip()
            if ':' in line:
                k, v = line.split(':', 1)
                keys[k.strip()] = v.strip()
    return keys

def get_token(keys):
    r = requests.post('https://www.strava.com/api/v3/oauth/token', data={
        'client_id':     keys['client_id'],
        'client_secret': keys['client_secret'],
        'refresh_token': keys['refresh_token'],
        'grant_type':    'refresh_token',
    })
    r.raise_for_status()
    data = r.json()
    keys['token']         = data['access_token']
    keys['refresh_token'] = data['refresh_token']
    with open('data_key.properties', 'w') as f:
        for k, v in keys.items():
            f.write(f'{k}:{v}\n')
    return data['access_token']

def get_last_activity(token):
    r = requests.get(
        'https://www.strava.com/api/v3/athlete/activities',
        headers={'Authorization': f'Bearer {token}'},
        params={'per_page': 1, 'page': 1}
    )
    r.raise_for_status()
    return r.json()[0]

def get_streams(token, activity_id):
    keys = 'time,watts,cadence,heartrate,velocity_smooth,distance,altitude'
    r = requests.get(
        f'https://www.strava.com/api/v3/activities/{activity_id}/streams',
        headers={'Authorization': f'Bearer {token}'},
        params={'keys': keys, 'key_by_type': 'true'}
    )
    r.raise_for_status()
    return r.json()

# ── Helpers ───────────────────────────────────────────────────────────────────

def fmt_dur(s):
    h, r = divmod(int(s), 3600)
    m, s = divmod(r, 60)
    return f'{h}h {m:02d}m' if h else f'{m}m {s:02d}s'

def safe_avg(lst):
    return sum(lst) / len(lst) if lst else 0

# ── Análisis de FC ────────────────────────────────────────────────────────────

def analizar_fc(hr_s, time_s, hr_max_real):
    """Devuelve dict con métricas y alertas de frecuencia cardíaca."""
    if not hr_s:
        return None

    hrmax = max(hr_max_real, max(hr_s))
    avg   = safe_avg(hr_s)
    pico  = max(hr_s)

    # Zonas FC (% HRmax)
    def zona_hr(h):
        p = h / hrmax
        if p < 0.60: return 'Z1'
        if p < 0.70: return 'Z2'
        if p < 0.80: return 'Z3'
        if p < 0.90: return 'Z4'
        return 'Z5'

    zonas_hr = {'Z1':0,'Z2':0,'Z3':0,'Z4':0,'Z5':0}
    for i, h in enumerate(hr_s):
        dt = (time_s[i] - time_s[i-1]) if i > 0 else 1
        zonas_hr[zona_hr(h)] += dt
    zonas_hr_min = {z: round(s/60, 1) for z, s in zonas_hr.items()}

    # Recuperación cardíaca: caída de FC en los primeros 60s de las pausas.
    # Las pausas están aproximadas por el intervalo donde la FC baja >5bpm en 30s.
    recuperaciones = []
    ventana = 60
    for i in range(len(hr_s) - ventana):
        drop = hr_s[i] - hr_s[i + ventana]
        if drop > 15 and hr_s[i] > avg:   # inicio de recuperación
            recuperaciones.append(drop)

    rec_media = round(safe_avg(recuperaciones), 1) if recuperaciones else None

    # Alertas
    alertas = []
    pct_pico = pico / hrmax * 100
    pct_avg  = avg  / hrmax * 100

    if pct_pico > 95:
        alertas.append(('rojo', f'FC máxima ({pico:.0f} bpm) supera el 95% del HRmax estimado. Evalúa si el esfuerzo fue excesivo.'))
    if pct_avg > 85:
        alertas.append(('naranja', f'FC media ({avg:.0f} bpm) estuvo al {pct_avg:.0f}% del HRmax. Sesión de alta intensidad cardiovascular.'))
    if rec_media is not None and rec_media < 15:
        alertas.append(('naranja', f'Recuperación cardíaca baja ({rec_media:.0f} bpm/min). Señal de fatiga acumulada o hidratación insuficiente.'))
    if rec_media is not None and rec_media >= 25:
        alertas.append(('verde', f'Buena recuperación cardíaca: FC baja ~{rec_media:.0f} bpm en los intervalos de descanso.'))
    if not alertas:
        alertas.append(('verde', 'FC dentro de rangos esperados para la sesión.'))

    return {
        'hrmax': hrmax,
        'avg': round(avg, 1),
        'pico': pico,
        'pct_avg': round(pct_avg, 1),
        'pct_pico': round(pct_pico, 1),
        'zonas_min': zonas_hr_min,
        'rec_media': rec_media,
        'alertas': alertas,
    }

# ── HTML ──────────────────────────────────────────────────────────────────────

TOOLTIPS = {
    'NP':  ('Normalized Power', 'Potencia Normalizada. Equivale a la potencia que habrías mantenido de forma constante para el mismo estrés fisiológico. Más representativo que la potencia media cuando hay variaciones (intervalos, frenadas, desconexiones).'),
    'IF':  ('Intensity Factor', 'Factor de Intensidad = NP ÷ FTP. 0.75 es aeróbico suave · 0.85 es sweet spot · 0.95+ es esfuerzo de competición. Te dice qué tan "duro" fue el entreno en relación a tu capacidad máxima.'),
    'TSS': ('Training Stress Score', 'Puntuación de Estrés de Entrenamiento. Una hora al FTP exacto = 100 TSS. <50 = fácil · 50-150 = moderado · >150 = requiere 2+ días de recuperación. Acumula semana a semana para medir la carga total.'),
    'VAM': ('Velocità Ascensionale Media', 'Velocidad Ascensional Media (m/h). Mide cuántos metros subes por hora. En ruta es clave para escaladores: amateur ~800-1000 m/h · Pro Tour >1500 m/h. En rodillo es virtual pero sirve de referencia.'),
}

def tooltip_icon(key):
    title, desc = TOOLTIPS[key]
    safe_desc = desc.replace("'", "&#39;")
    return (
        f'<span class="tip-wrap">'
        f'<span class="tip-icon" tabindex="0">?'
        f'<span class="tip-box"><strong>{title}</strong><br>{safe_desc}</span>'
        f'</span></span>'
    )

def generar_html(activity, streams):
    nombre  = activity.get('name', 'Entrenamiento')
    fecha   = activity['start_date_local'][:10]
    dur     = activity.get('moving_time', 0)
    dist_km = activity.get('distance', 0) / 1000
    avg_w   = activity.get('average_watts', 0) or 0
    max_w   = activity.get('max_watts', 0) or 0
    avg_cad = activity.get('average_cadence', 0) or 0
    avg_hr  = activity.get('average_heartrate', 0) or 0
    max_hr  = activity.get('max_heartrate', 0) or 0
    elev    = activity.get('total_elevation_gain', 0) or 0

    time_s  = streams.get('time',             {}).get('data', [])
    watts_s = streams.get('watts',            {}).get('data', [])
    cad_s   = streams.get('cadence',          {}).get('data', [])
    hr_s    = streams.get('heartrate',        {}).get('data', [])
    vel_s   = streams.get('velocity_smooth',  {}).get('data', [])

    time_min = [round(t / 60, 2) for t in time_s]

    # NP
    np_val = 0
    if watts_s and len(watts_s) >= 30:
        roll = [sum(watts_s[i-29:i+1]) / 30 for i in range(29, len(watts_s))]
        np_val = round((sum(w**4 for w in roll) / len(roll)) ** 0.25, 1)

    if_score = round(np_val / FTP, 2) if np_val else round(avg_w / FTP, 2)
    tss      = round((dur * np_val * if_score) / (FTP * 3600) * 100, 1) if np_val else 0

    # VAM
    vam = round(elev / (dur / 3600), 0) if dur and elev else 0

    # Zonas de potencia
    def zona_w(w):
        if w < FTP * 0.60: return 'Z1'
        if w < FTP * 0.75: return 'Z2'
        if w < FTP * 0.87: return 'Z3'
        if w < FTP * 1.00: return 'Z4'
        if w < FTP * 1.15: return 'Z5'
        return 'Z6'

    zonas = {'Z1':0,'Z2':0,'Z3':0,'Z4':0,'Z5':0,'Z6':0}
    for i, w in enumerate(watts_s):
        dt = (time_s[i] - time_s[i-1]) if i > 0 else 1
        zonas[zona_w(w)] += dt
    zonas_min = {z: round(s/60,1) for z, s in zonas.items()}

    # Cadencia en objetivo
    cad_ok  = sum(1 for c in cad_s if 88 <= c <= 95)
    cad_pct = round(cad_ok / len(cad_s) * 100, 1) if cad_s else 0

    # Análisis FC
    fc_data = analizar_fc(hr_s, time_s, max(HR_MAX, max_hr))

    # Colores
    zc = {'Z1':'#94a3b8','Z2':'#38bdf8','Z3':'#4ade80','Z4':'#fb923c','Z5':'#f43f5e','Z6':'#a855f7'}
    zl = {'Z1':'Recuperación','Z2':'Aeróbico','Z3':'Tempo','Z4':'Umbral','Z5':'VO2max','Z6':'Anaeróbico'}
    hr_zc = {'Z1':'#94a3b8','Z2':'#38bdf8','Z3':'#4ade80','Z4':'#fb923c','Z5':'#f43f5e'}
    hr_zl = {'Z1':'Reposo','Z2':'Aeróbico','Z3':'Tempo','Z4':'Umbral','Z5':'Máximo'}

    # JSON
    w_json  = json.dumps(watts_s)
    c_json  = json.dumps(cad_s)
    hr_json = json.dumps(hr_s)
    t_json  = json.dumps(time_min)
    vel_j   = json.dumps([round(v*3.6,1) for v in vel_s])

    wmax_chart = (max(watts_s) + 50) if watts_s else 300

    # Bloque HTML de alertas FC
    def alerta_fc_html():
        if not fc_data:
            return '<p style="color:var(--muted)">Sin datos de FC en esta sesión.</p>'
        rows = []
        for color, txt in fc_data['alertas']:
            icon = '🟢' if color == 'verde' else ('🟠' if color == 'naranja' else '🔴')
            rows.append(f'<div class="alerta-fc alerta-{color}">{icon} {txt}</div>')
        return '\n'.join(rows)

    def zonas_fc_html():
        if not fc_data:
            return ''
        bars = []
        for z, lbl in hr_zl.items():
            mins = fc_data['zonas_min'].get(z, 0)
            color = hr_zc[z]
            bars.append(
                f'<div class="zona-bar" style="background:{color}22;border:1px solid {color}">'
                f'<div class="zmin" style="color:{color}">{mins}</div>'
                f'<div class="znm">{z} · {lbl}</div></div>'
            )
        return '\n'.join(bars)

    def zonas_pot_html():
        bars = []
        for z in ['Z1','Z2','Z3','Z4','Z5','Z6']:
            color = zc[z]
            bars.append(
                f'<div class="zona-bar" style="background:{color}22;border:1px solid {color}">'
                f'<div class="zmin" style="color:{color}">{zonas_min[z]}</div>'
                f'<div class="znm">{z} · {zl[z]}</div></div>'
            )
        return '\n'.join(bars)

    fc_tabla = ''
    if fc_data:
        rec_txt = f"{fc_data['rec_media']:.0f} bpm/min" if fc_data['rec_media'] else '—'
        rec_eval = '✅ Buena' if (fc_data['rec_media'] or 0) >= 20 else '⚠️ Baja — evalúa descanso'
        fc_tabla = f'''
    <tr><td>FC máxima sesión</td><td><strong>{fc_data["pico"]:.0f} bpm</strong> ({fc_data["pct_pico"]}% HRmax)</td></tr>
    <tr><td>FC media sesión</td><td><strong>{fc_data["avg"]} bpm</strong> ({fc_data["pct_avg"]}% HRmax)</td></tr>
    <tr><td>HRmax referencia</td><td>{fc_data["hrmax"]} bpm</td></tr>
    <tr><td>Recuperación cardíaca</td><td>{rec_txt} — {rec_eval}</td></tr>'''

    hr_chart_block = ''
    if hr_s:
        hr_max_chart = (max(hr_s) + 10)
        hr_chart_block = f'''
<div class="card">
  <h2>❤️ Frecuencia Cardíaca (bpm)</h2>
  <canvas id="chartHR"></canvas>
</div>
<div class="card">
  <h2>❤️ Análisis de Frecuencia Cardíaca</h2>
  <div style="margin-bottom:14px">{alerta_fc_html()}</div>
  <div class="zonas" style="grid-template-columns:repeat(5,1fr);margin-bottom:16px">
    {zonas_fc_html()}
  </div>
  <table>
    <tr><th>Métrica</th><th>Valor</th></tr>
    {fc_tabla}
  </table>
</div>'''
        hr_chart_js = f'''
new Chart(document.getElementById('chartHR'), {{
  type:'line',
  data:{{ labels:t, datasets:[
    ds(hr,'#ef4444'),
    {{ data:t.map(()=>{int(fc_data["hrmax"]*0.90 if fc_data else 165)}), borderColor:'#ef444466',
      borderWidth:1, borderDash:[4,4], pointRadius:0, fill:false, label:'90% HRmax' }},
  ]}},
  options: opts('bpm','#ef4444', {hr_max_chart})
}});'''
    else:
        hr_chart_js = ''

    html = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Análisis · {nombre} · {fecha}</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
:root{{--bg:#0f1117;--card:#1a1d2e;--accent:#f97316;--text:#e2e8f0;--muted:#64748b;--border:#2d3148}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--text);font-family:'Segoe UI',system-ui,sans-serif;padding:24px;max-width:1100px;margin:0 auto}}
h1{{font-size:1.6rem;font-weight:700;margin-bottom:4px}}
.sub{{color:var(--muted);font-size:.9rem;margin-bottom:28px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:12px;margin-bottom:28px}}
.kpi{{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:16px;text-align:center;position:relative}}
.kpi .val{{font-size:1.7rem;font-weight:700;color:var(--accent)}}
.kpi .lbl{{font-size:.73rem;color:var(--muted);margin-top:4px;display:flex;align-items:center;justify-content:center;gap:4px}}
.card{{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:20px;margin-bottom:20px}}
.card h2{{font-size:1rem;font-weight:600;margin-bottom:16px;color:var(--accent)}}
canvas{{max-height:220px}}
.zonas{{display:grid;grid-template-columns:repeat(6,1fr);gap:8px;margin-top:8px}}
.zona-bar{{border-radius:8px;padding:10px 6px;text-align:center}}
.zona-bar .zmin{{font-size:1.1rem;font-weight:700}}
.zona-bar .znm{{font-size:.63rem;margin-top:2px;opacity:.8}}
.alerta{{background:#2d1f00;border:1px solid #f97316;border-radius:10px;padding:14px 18px;margin-bottom:16px;font-size:.9rem;line-height:1.6}}
.alerta-fc{{border-radius:8px;padding:10px 14px;margin-bottom:8px;font-size:.87rem;line-height:1.5}}
.alerta-verde{{background:#052e16;border:1px solid #22c55e}}
.alerta-naranja{{background:#2d1f00;border:1px solid #f97316}}
.alerta-rojo{{background:#2d0d0d;border:1px solid #ef4444}}
table{{width:100%;border-collapse:collapse;font-size:.85rem}}
td,th{{padding:8px 12px;text-align:left;border-bottom:1px solid var(--border)}}
th{{color:var(--muted);font-weight:500}}
/* Tooltip */
.tip-wrap{{display:inline-block;vertical-align:middle;margin-left:3px}}
.tip-icon{{display:inline-flex;align-items:center;justify-content:center;width:15px;height:15px;
  background:#2d3148;border:1px solid #4a5180;border-radius:50%;font-size:.6rem;
  cursor:help;color:#94a3b8;position:relative;font-style:normal}}
.tip-icon .tip-box{{display:none;position:absolute;bottom:calc(100% + 6px);left:50%;
  transform:translateX(-50%);background:#1e2035;border:1px solid #3d4168;border-radius:8px;
  padding:10px 12px;width:230px;font-size:.75rem;color:#e2e8f0;z-index:99;
  white-space:normal;line-height:1.5;text-align:left;pointer-events:none}}
.tip-icon:hover .tip-box,.tip-icon:focus .tip-box{{display:block}}
</style>
</head>
<body>

<h1>🚴 {nombre}</h1>
<div class="sub">{fecha} · Sesión S01A — Plan Progresión 8 semanas · Semana 1</div>

<div class="grid">
  <div class="kpi"><div class="val">{fmt_dur(dur)}</div><div class="lbl">Duración</div></div>
  <div class="kpi"><div class="val">{dist_km:.1f} km</div><div class="lbl">Distancia</div></div>
  <div class="kpi"><div class="val">{avg_w:.0f} W</div><div class="lbl">Potencia media</div></div>
  <div class="kpi"><div class="val">{np_val:.0f} W</div>
    <div class="lbl">NP {tooltip_icon('NP')}</div></div>
  <div class="kpi"><div class="val">{if_score:.2f}</div>
    <div class="lbl">IF {tooltip_icon('IF')}</div></div>
  <div class="kpi"><div class="val">{tss:.0f}</div>
    <div class="lbl">TSS {tooltip_icon('TSS')}</div></div>
  <div class="kpi"><div class="val">{vam:.0f}</div>
    <div class="lbl">VAM m/h {tooltip_icon('VAM')}</div></div>
  <div class="kpi"><div class="val">{avg_cad:.0f} rpm</div><div class="lbl">Cadencia media</div></div>
  <div class="kpi"><div class="val">{avg_hr:.0f} bpm</div><div class="lbl">FC media</div></div>
  <div class="kpi"><div class="val">{max_hr:.0f} bpm</div><div class="lbl">FC máxima</div></div>
</div>

<div class="alerta">
  ⚠️ <strong>Desconexión detectada:</strong> El rodillo se desconectó durante la sesión provocando un gap en los datos de potencia.
  Los bloques completados tras la reconexión son válidos. El NP y TSS están calculados sobre los datos disponibles.
</div>

<div class="card">
  <h2>⚡ Potencia (W)</h2>
  <canvas id="chartWatts"></canvas>
</div>

<div class="card">
  <h2>🔄 Cadencia (rpm) — Zona objetivo: 88-95 rpm</h2>
  <canvas id="chartCad"></canvas>
</div>

{hr_chart_block}

<div class="card">
  <h2>📊 Distribución Zonas de Potencia — FTP: {FTP}W</h2>
  <div style="font-size:.78rem;color:var(--muted);margin-bottom:10px">Minutos en cada zona</div>
  <div class="zonas">{zonas_pot_html()}</div>
</div>

<div class="card">
  <h2>🎯 Cadencia en zona objetivo (88-95 rpm)</h2>
  <table>
    <tr><th>Métrica</th><th>Valor</th></tr>
    <tr><td>Cadencia promedio</td><td><strong>{avg_cad:.0f} rpm</strong></td></tr>
    <tr><td>Tiempo en 88-95 rpm</td><td><strong>{cad_pct}%</strong></td></tr>
    <tr><td>Histórico habitual</td><td>79 rpm</td></tr>
    <tr><td>Mejora</td><td>+{max(0, round(avg_cad - 79, 1))} rpm vs histórico</td></tr>
  </table>
</div>

<div class="card">
  <h2>📝 Resumen de la Sesión</h2>
  <table>
    <tr><th>Aspecto</th><th>Evaluación</th></tr>
    <tr><td>Potencia NP vs objetivo (144W)</td><td>{"✅ Dentro del rango" if 130 <= np_val <= 158 else "⚠️ Revisar — posible impacto de la desconexión"}</td></tr>
    <tr><td>TSS acumulado ({tss:.0f} pts)</td><td>{"✅ Carga moderada — recupera en 24h" if tss < 80 else "⚠️ Carga alta — descansa bien mañana"}</td></tr>
    <tr><td>IF ({if_score:.2f})</td><td>{"✅ Intensidad adecuada para sweet spot" if 0.70 <= if_score <= 0.90 else "ℹ️ Revisa — puede estar afectado por la desconexión"}</td></tr>
    <tr><td>Desconexión rodillo</td><td>⚠️ Sí — afectó datos de un segmento</td></tr>
    <tr><td>Próxima sesión</td><td>Martes · S01A (repetir si no se completó bien) o S02A si todo OK</td></tr>
  </table>
</div>

<script>
const t  = {t_json};
const w  = {w_json};
const c  = {c_json};
const hr = {hr_json};

const opts = (label, color, ymax) => ({{
  responsive:true, animation:false,
  plugins:{{ legend:{{display:false}} }},
  scales:{{
    x:{{ ticks:{{color:'#64748b',maxTicksLimit:10}}, grid:{{color:'#1e2035'}} }},
    y:{{ ticks:{{color:'#64748b'}}, grid:{{color:'#1e2035'}}, max:ymax, min:0 }}
  }}
}});
const ds = (data, color) => ({{
  data, borderColor:color, borderWidth:1.5,
  pointRadius:0, fill:true, backgroundColor:color+'18', tension:0.3
}});
const line = (val, color) => ({{
  data:t.map(()=>val), borderColor:color,
  borderWidth:1, borderDash:[5,5], pointRadius:0, fill:false
}});

new Chart(document.getElementById('chartWatts'), {{
  type:'line',
  data:{{ labels:t, datasets:[ds(w,'#f97316'), line(144,'#f9731666'), line(156,'#f9731666')] }},
  options: opts('W','#f97316', {wmax_chart})
}});

new Chart(document.getElementById('chartCad'), {{
  type:'line',
  data:{{ labels:t, datasets:[ds(c,'#818cf8'), line(88,'#22c55e88'), line(95,'#22c55e88')] }},
  options: opts('rpm','#818cf8', 120)
}});

{hr_chart_js}
</script>
</body>
</html>'''
    return html

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    keys = load_keys()
    print("Refrescando token...")
    token = get_token(keys)

    print("Descargando última actividad...")
    activity = get_last_activity(token)
    print(f"  → {activity['name']} ({activity['start_date_local'][:10]})")

    print("Descargando streams...")
    streams = get_streams(token, activity['id'])

    print("Generando HTML...")
    html = generar_html(activity, streams)

    fname = f"analisis_{activity['start_date_local'][:10]}.html"
    with open(fname, 'w') as f:
        f.write(html)

    print(f"\n✓ {fname}")
    import subprocess
    subprocess.run(['open', fname])

if __name__ == '__main__':
    main()
