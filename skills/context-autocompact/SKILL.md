---
name: context-autocompact
version: 1.2.0
author: EthanBernier
team: PhoenixProject
description: Compaction automatique du contexte de session sans perte semantique.
created: 2026-03-02
tags: [memory, context, optimization, tokens]
---

# Skill : Context Auto-Compact

> Auteur : EthanBernier | Equipe : PhoenixProject | v1.2.0

## Objectif

Eviter le depassement de la fenetre de contexte (200k tokens) en compactant
regulierement la session sans perdre le sens des taches en cours.

## Principes

- Compacter SOUVENT et TOT (seuil bas = 15 edits)
- Toujours sauvegarder l'etat avant compaction (hook PreCompact)
- Preserver : taches actives, decisions cles, fichiers modifies, erreurs rencontrees
- Supprimer : verbosites, repetitions, details deja integres

## Declencheurs

| Signal | Seuil | Action |
|--------|-------|--------|
| Modifications fichiers | >= 15 | Warning `/compact` |
| Token usage > 60% | automatique | Proposer compaction |
| Erreur bloquante | immediate | Compact + relancer |
| Fin de tache | systematique | Compact preventif |

## Procedure de Compaction

```
1. AVANT COMPACT
   - Lister les taches en cours (TODO actif)
   - Noter les fichiers modifies non commites
   - Sauvegarder les decisions cles (architecture, choix techniques)
   - Identifier les erreurs non resolues

2. PENDANT COMPACT (/compact)
   - Claude reduit le contexte a l'essentiel semantique
   - Le hook pre-compact.js sauvegarde l'etat dans .agent/state/pre-compact.json

3. APRES COMPACT
   - Verifier que les taches actives sont toujours visibles
   - Reprendre sans perte avec : "Reprends depuis la derniere tache"
```

## Format de Resumé Semantique

Lors d'une compaction manuelle, fournir ce bloc :

```
## Contexte compact [PHOENIX v1.2.0]
Projet : <nom>
Branche : <branche>
Taches actives : <liste>
Fichiers modifies : <liste>
Derniere action : <action>
Prochaine action : <action>
Blocages : <liste ou "aucun">
```

## Configuration

```bash
# Seuil de compaction (defaut: 15 edits)
export PHOENIX_COMPACT_THRESHOLD=15

# Activer le mode verbose pre-compact
export PHOENIX_COMPACT_VERBOSE=1
```

## Integration Hooks

Ce skill s'appuie sur :
- `hooks/suggest-compact.js` : declencheur apres N modifications
- `hooks/pre-compact.js` : sauvegarde d'etat avant compaction
- `hooks/hooks.json` : configuration PreCompact + PostToolUse

## Valeur Ajoutee

- Sessions 3x plus longues sans depassement de contexte
- Reprise fluide apres compaction (etat persiste dans `.agent/state/`)
- Compatible Claude Code, Codex, et agents tiers (format agnostique)
- Zero perte semantique : seules les verbosites sont eliminees
