# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

Personal cycling training system that connects to Strava, analyzes workout data, generates structured training sessions, and produces HTML reports. Built for one user (Hugo) with a Hammerhead Karoo cyclocomputer and a smart trainer.

## Key Constants (user-specific)

- **FTP**: 180W (smart trainer)
- **Historical average cadence**: 79 rpm
- **Target cadence**: 88-95 rpm
- **HRmax reference**: 185 bpm
- **Strava credentials**: `data_key.properties` (client_id, client_secret, token, refresh_token)

## Scripts and Their Role

| Script | Purpose | Run when |
|--------|---------|----------|
| `strava_oauth.py` | OAuth flow to get/refresh Strava tokens | Token expires or first setup |
| `strava_analyzer.py` | Downloads all activities → `strava_activities.json`, prints summary | Bulk re-analysis |
| `analisis_sesion.py` | **Main workflow** — fetches last activity, generates `analisis_YYYY-MM-DD.html` | After every workout |
| `plan_progresion.py` | Generates all 8-week `.zwo` workout files into `workouts/` | Once, or when plan changes |
| `sesion_hoy.py` | Generates a one-off `.zwo` and `.fit` for today's session | Ad-hoc session creation |

## Token Management

`analisis_sesion.py` and `strava_analyzer.py` auto-refresh the token using the refresh_token and rewrite `data_key.properties`. If the refresh fails, re-run `strava_oauth.py` which starts a local server on port 8080 to capture the OAuth callback.

Strava requires scope `activity:read_all` — the OAuth URL in `strava_oauth.py` already includes this.

## Workout File Formats

- **Hammerhead Karoo** accepts `.zwo` and `.fit`. Use `.zwo` — it works reliably.
- `.zwo` uses percentage of FTP (0.0–1.0), not absolute watts. FTP must be set in the Karoo profile.
- `.fit` generation uses `fit-tool` library with power offset +1000 per FIT protocol spec.
- `.erg` format does NOT work with Hammerhead.

Import path: `account.hammerhead.io → Library → Workouts → Import`

## Training Plan Structure

8-week progression in `workouts/`:
- `S0xA_*.zwo` — interval session (changes each week, core of the plan)
- `S01B_base.zwo` — Z2 aerobic base, 45 min (fixed, reuse every week)
- `S01C_base.zwo` — high-cadence neuromuscular, 50 min (fixed)
- `S01D_larga_75min.zwo` — long ride with 3 tempo spikes (fixed)

Weekly schedule: Tue=A, Thu=B, Sat=C, Sun=D. Priority if short on time: A → D → B → C.

**Progression rule**: user must complete all reps before advancing to next week's file.

## HTML Report (`analisis_sesion.py`)

Generates a dark-theme HTML report with Chart.js graphs (CDN). Key metrics:
- NP (Normalized Power): 30s rolling average^4
- IF = NP / FTP
- TSS = (duration × NP × IF) / (FTP × 3600) × 100
- VAM = elevation_gain / (duration_hours)
- HR analysis: zones, recovery quality, alerts (verde/naranja/rojo)
- Cadencia % in target zone (88-95 rpm)

Tooltips explain NP, IF, TSS, VAM on hover via pure CSS (no JS dependency).

## Dependencies

```bash
pip install requests fit-tool fitparse
```
