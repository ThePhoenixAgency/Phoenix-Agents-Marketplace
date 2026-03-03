---
name: integrity-development
description: Zero Trust basics, validation, sanitization
author: PhoenixProject
version: 1.0.0
created: 2026-02-18
last_updated: 2026-02-23
---
# Secure Coding
## Principes Zero Trust
- Ne jamais faire confiance aux inputs
- Valider cote serveur, toujours
- Principe du moindre privilege
- Defense en profondeur
## Regles de base
- Tous les inputs valides et assainis
- Pas de secrets en dur
- Pas de logs avec PII
- Prepared statements pour les queries
- HTTPS partout
- CORS configure correctement
- Rate limiting sur les endpoints sensibles
