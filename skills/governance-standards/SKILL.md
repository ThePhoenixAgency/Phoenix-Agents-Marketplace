---
name: governance-standards
description: "Standards de gouvernance immuables PhoenixProject. Charge avant toute tache de developpement ou d audit. Agnostique Claude/Codex/Docker."
author: EthanBernier
team: PhoenixProject
version: 1.0.0
created: 2026-03-03
last_updated: 2026-03-03
whenToUse: |
  Charger systematiquement avant de commencer toute tache de dev, audit, spec ou commit.
  Invoquer standards-enforcer en parallele pour la validation en continu.
---
# en francais toujours

# Governance Standards — Standards Immuables PhoenixProject

## Standards Actifs

Tous les standards resident dans `standards/` a la racine du repo.
Ils sont en lecture seule. Aucun agent ne les modifie.

| Standard | Fichier | Regle principale |
|----------|---------|------------------|
| S00 — Zero Emoji | `standards/00_NO_EMOJI.md` | Aucun emoji dans le code, commits, docs |
| S01 — Zero Trust | `standards/01_SECURITY_ZERO_TRUST.md` | Repo PUBLIC : /private/ gitignored, secrets interdits |
| S02 — Git Flow | `standards/02_GIT_VERSIONING.md` | Conventional Commits, SemVer, gitleaks pre-commit |
| S03 — Nommage | `standards/03_NAMING_PROTOCOL.md` | camelCase/PascalCase, 2-3 mots max, anglais technique |
| S04 — Anti-Rush | `standards/04_ANTI_RUSH_POLICY.md` | Spec validee avant code, TDD strict, zero fake code |
| S05 — Asset Guard | `standards/05_ASSET_PROTECTION.md` | Backlog-driven uniquement, hors-scope = intouchable |
| S06 — Agnosticisme | `standards/06_AGNOSTICISM.md` | Standards neutres, zero lock-in outil |
| S07 — Agent IA | `standards/domain_specific/AI_AGENT_STANDARDS.md` | FR pour user, EN pour code, Zero Trust, honnetete |
| S08 — Apple | `standards/domain_specific/APPLE_STANDARDS.md` | Swift/SwiftUI, HIG, VoiceOver, App Store |

## Protocole de Chargement

```
OBLIGATOIRE pour tout agent :
1. Lire ce fichier (index)
2. Charger les standards pertinents a la tache :
   - Dev general   : S00, S02, S03, S04, S05
   - Securite      : S01, S07
   - Code AI/Agents: S07
   - Apple         : S08
   - Commits       : S00, S02
3. Appliquer sans deviation
```

## Deleguees en Parallele

Appeler `standards-enforcer` via Task (haiku, rapide) pour validation en parallele :

```
Task("standards-enforcer", "Valider compliance standards S00-S07 sur [fichier/dossier]")
```

Ne PAS bloquer le workflow principal — standards-enforcer tourne en arriere-plan
et produit `private/governance/VIOLATIONS.md`.

## Violations — Format de Signal

```
[VIOLATION] S03 standards/03_NAMING_PROTOCOL.md
Fichier : src/user_authentication_management.ts
Raison  : Nom trop long (>3 mots), utiliser AuthService.ts

[OK] S00, S01, S02, S04, S05
```

## Hierarchie des Standards

```
Standards (standards/)    = "Quoi" et "Pourquoi"  — IMMUABLES
Agents   (agents/)        = "Qui"                 — Comportements
Skills   (skills/)        = "Comment"             — Actions et procedures
```

## Mise a Jour

Les standards sont versiones (SemVer). Toute modification suit le workflow S02.
Seul le Mainteneur (EthanBernier) peut bumper la version d'un standard.
