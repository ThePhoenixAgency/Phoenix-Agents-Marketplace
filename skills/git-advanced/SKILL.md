---
name: git-advanced
description: Worktrees, bisect, interactive rebase, hooks
author: PhoenixProject
version: 1.0.0
created: 2026-02-18
last_updated: 2026-02-23
---
# Git Advanced
## Worktrees
```bash
# Travailler sur 2 branches en parallele sans stash
git worktree add ../feature-branch feature/my-feature
git worktree list
git worktree remove ../feature-branch
```
## Bisect
```bash
git bisect start
git bisect bad          # commit actuel est casse
git bisect good v1.0.0  # v1.0.0 fonctionnait
# Git checkout automatiquement au milieu
# Tester, puis marquer bon/mauvais
git bisect good  # ou git bisect bad
# Repeter jusqu'a trouver le commit fautif
git bisect reset
```
## Interactive Rebase
```bash
git rebase -i HEAD~5
# pick = garder
# reword = changer le message
# squash = fusionner avec le commit precedent
# drop = supprimer
# fixup = squash sans message
```
## Hooks
```bash
# .git/hooks/pre-commit
#!/bin/sh
npm run lint
npm test
# Bloquer si erreur
```
## Conventions
- Commits atomiques (une chose par commit)
- Messages conventionnels (feat, fix, docs, etc.)
- Branches courtes (< 1 semaine)
- Rebase sur main avant merge
