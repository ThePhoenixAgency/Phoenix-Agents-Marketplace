---
version: 1.1.0
last_updated: 2026-02-04
author: PhoenixProject
status: Stable
description: Standards Git - Commits, Versioning et Hooks.
---

# COMMITS, VERSIONING & GIT FLOW

## PROTOCOLE D'EXÉCUTION OBLIGATOIRE
1.  **START** : Lire `docs/BACKLOG.md` et les Standards de Gouvernance.
2.  **PROCESS** : Appliquer les règles sans déviation.
3.  **END** : Mettre à jour `docs/BACKLOG.md` et `docs/CHANGELOG.md` avant tout commit.

**Format Obligatoire : Conventional Commits**

### PRE-COMMIT HOOKS (Obligatoires)
- **Linting** : Vérification de la syntaxe.
- **Secrets** : Scan `gitleaks` pour empêcher les fuites d'emails ou de clés.
- **Integrity** : Exécution de `tests/verify_integrity.py`.

### POST-COMMIT RULES
- **Synchronization** : Les modifications de `/core_standards` doivent être répercutées dans `_EXPORTS/` via `run_pipeline.sh`.
- **Documentation** : Le `CHANGELOG.md` doit être à jour avec les changements du commit en cours.

### Versioning Sémantique (SemVer 2.0.0)
L'IA ne décide pas de la version, elle est calculée par le pipeline de standardisation.
- **Minor** : Nouvelles fonctionnalités (`feat`).
- **Patch** : Corrections (`fix`), documentation ou maintenance.
- **Changelog** : Automatisé dans le cadre du pipeline.
