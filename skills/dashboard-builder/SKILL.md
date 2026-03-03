---
name: dashboard-builder
description: Dashboards personnalises, widgets, monitoring temps reel, drag and drop
author: PhoenixProject
version: 1.0.0
created: 2026-02-23
last_updated: 2026-02-23
---
# Dashboard Builder

## Competences
- Editeur drag-and-drop pour agencement de widgets
- Widgets systeme (CPU, RAM, disque, reseau, temperature)
- Widgets meteo, calendrier, RSS, finance, notes
- Widgets de suivi IA/LLM (tokens, cout, latence)
- Templates de dashboards (export, import, partage)
- Mode edition / mode consultation
- Auto-refresh et streaming de donnees (SSE, WebSocket)
- Dark mode natif
- Pages personnalisees (kanban, notes, workflows)

## Architecture
- Full local (pas de cloud, pas de donnees qui sortent)
- Configuration en JSON (versionnable)
- Widgets auto-decouverts au demarrage
- API REST pour l'integration avec d'autres outils
- Run on boot (launchd macOS, systemd Linux)
