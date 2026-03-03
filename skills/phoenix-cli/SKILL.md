---
name: phoenix-cli
description: "Interface CLI pour Phoenix-Orchestrator local. Commandes mappees fr/en vers le runtime Phoenix. Agnostique : fonctionne sur tout systeme ou phoenix est installe."
author: EthanBernier
team: PhoenixProject
version: 1.0.0
created: 2026-03-03
last_updated: 2026-03-03
whenToUse: |
  Utiliser quand le runtime Phoenix-Orchestrator est installe localement.
  Invoquer pour diagnostiquer, reparer, ou executer des taches via CLI.
tools: ["Bash"]
runtime:
  agnostic: true
  docker_compatible: true
  requires: phoenix CLI installed
---
# en francais toujours

# Phoenix CLI — Interface Runtime Locale

## Mission

Wrapper CLI pour le runtime Phoenix local. Mappe les commandes naturelles
(fr/en) vers les commandes CLI exactes du runtime Phoenix.

## Commandes (Reference Complete)

| Commande slash | CLI exacte | Alias FR | Alias EN |
|----------------|-----------|----------|----------|
| `/doctor` | `phoenix doctor --deep` | verifier | check |
| `/policy check` | `phoenix policy check --strict` | politique | policy |
| `/repair safe` | `phoenix repair --safe` | reparer | repair |
| `/run <task>` | `phoenix run --task "<task>"` | executer | run |

## Configuration Runtime

```json
{
  "language": "fr",
  "passive_mode": true,
  "audit_security_gate": true
}
```

- `language` : "fr" ou "en" (defaut: fr)
- `passive_mode` : true = veille passive sans tokens (defaut: true)
- `audit_security_gate` : true = audit securite obligatoire avant run/deploy

## Regles d'Execution

1. Zero exfiltration par defaut
2. Audit securite (`/policy check`) obligatoire AVANT tout `/run` ou deploy
3. Runtime event-driven en veille passive (zero token LLM sans evenement)
4. Toujours lire `skills/governance-standards/SKILL.md` avant execution

## Diagnostics

```bash
# Verification complete du runtime
phoenix doctor --deep

# Verification des politiques de securite
phoenix policy check --strict

# Reparation safe (non-destructive)
phoenix repair --safe

# Execution d'une tache
phoenix run --task "audit securite app web"
```

## Integration Phoenix Orchestrateur

Le Phoenix CLI est une extension du Phoenix Orchestrateur master.
L'orchestrateur peut invoquer ces commandes via Bash :

```
# Depuis phoenix-orchestrator
Bash("phoenix doctor --deep")
Bash("phoenix run --task \"<description tache>\"")
```
