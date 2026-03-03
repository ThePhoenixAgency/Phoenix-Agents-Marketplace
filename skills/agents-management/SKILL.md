---
name: agents-management
description: Coordination multi-agents, delegation, suivi
author: PhoenixProject
version: 1.0.0
created: 2026-02-18
last_updated: 2026-02-23
---
# Agents Management
## Delegation
1. Identifier l'agent le plus competent pour la tache
2. Fournir un contexte clair (objectif, contraintes, format attendu)
3. Definir les criteres de succes
4. Suivre la progression
5. Valider le resultat
## Communication inter-agents (AMP)
- Messages structures (type, from, to, payload)
- Signatures Ed25519 pour l'authenticite
- Queue de messages pour l'asynchrone
- Broadcast pour les annonces globales
## Patterns
| Pattern | Usage |
|---------|-------|
| Pipeline | A -> B -> C (sequentiel) |
| Fan-out | A -> B, C, D (parallele) |
| Aggregator | B, C, D -> A (fusion resultats) |
| Supervisor | A surveille B, C, D (restart si echec) |
