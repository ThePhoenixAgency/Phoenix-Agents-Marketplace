# [PRIVATE] AGENTS INDEX - LOIS DE GOUVERNANCE PHOENIXPROJECT

**Version** : 1.5.0 (SemVer)
**Dernière mise à jour** : 2026-02-27

## But de ce fichier
Ce fichier ne contient aucune règle détaillée pour éviter la duplication.
Les règles opérationnelles complètes sont définies dans les fichiers ci-dessous.

## Fichiers canoniques de gouvernance (doivent être lus)
- `./AGENTS.override.md` (règles détaillées, priorité absolue)
- `./INSTRUCTIONS.agent.yaml` (paramétrage exécutable par l’agent)
- `./docs/BACKLOG.md` (plan du tour)
- `./docs/checklog.md` (journal de tour)
- `./docs/private/security.md` (artefacts sécurité et remédiation)

## Notes d’exécution
- Respecter la hiérarchie de priorité: `AGENTS.override.md` > `INSTRUCTIONS.agent.yaml`.
- Toute règle métier détaillée doit être écrite uniquement dans `AGENTS.override.md`.

## Pipeline de base
Consulter toujours les fichiers de pipeline dans l’ordre:
1) `./AGENTS.override.md`
2) `./INSTRUCTIONS.agent.yaml`
3) `./docs/BACKLOG.md`
4) `./docs/checklog.md`

---
[INFO] PhoenixProject : Conception Souveraine, Immutabilité, Auditabilité.
