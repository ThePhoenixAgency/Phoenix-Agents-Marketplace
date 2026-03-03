---
name: agent-economics
description: Suivi des couts, ROI, facturation des taches agents, budget IA
author: PhoenixProject
version: 1.0.0
created: 2026-02-23
last_updated: 2026-02-23
---
# Agent Economics

## Competences
- Tracking cout par tache (tokens, compute, API calls)
- ROI par agent (valeur produite vs cout)
- Budget IA mensuel (alertes, caps, throttling)
- Facturation interne des taches (temps estime x valeur)
- Comparaison cout local vs cloud
- Optimisation (router vers le provider le moins cher)
- Reporting financier IA (depenses par projet, par agent)

## Metriques
- Cout par token (input/output par provider)
- Cout par tache completee
- Ratio qualite/cout
- Temps economise vs cout IA
- Break-even point (a partir de quand l'agent est rentable)

## Strategies d'optimisation
- Local-first pour les taches simples (cout zero)
- Cache des reponses repetitives
- Batch processing pour reduire les Round trips
- Model selection par complexite (T1 local, T2 API, T3 premium)
