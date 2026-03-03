---
version: 1.0.0
last_updated: 2026-02-04
author: PhoenixProject
status: Stable
description: Agnosticisme Technique et Portabilité des Standards.
---

# AGNOSTICISME & PORTABILITÉ

## PROTOCOLE D'EXÉCUTION OBLIGATOIRE
1.  **START** : Lire `docs/BACKLOG.md` et les Standards de Gouvernance.
2.  **PROCESS** : Appliquer les règles sans déviation.
3.  **END** : Mettre à jour `docs/BACKLOG.md` et `docs/CHANGELOG.md` avant tout commit.

**RÈGLE #6 : LES STANDARDS SONT NEUTRES ET UNIVERSELS.**

### 1. INDÉPENDANCE DES OUTILS
- [ERROR] **Zéro Dépendance** : Un fichier de standard ne doit jamais mentionner un outil spécifique (Claude, Cursor, Codex, etc.) pour définir une règle globale.
- [ERROR] **Zéro Chemin Externe** : Ne jamais faire référence à des dossiers qui n'existent que dans le dépôt de gouvernance (ex: `core_standards`, `AI-STANDARD-RULES`).
- [OK] **Universalité** : Les standards doivent fonctionner de la même manière si le projet change d'IDE ou d'agent IA.

### 2. LOCALISATION ET ACCÈS
- Les standards appartiennent au **Projet**. Ils résident dans `/standards/` à la racine.
- Aucun agent ne possède les standards. Ils sont une ressource partagée en lecture seule.

### 3. SÉPARATION DES PRÉOCCUPATIONS (SoC)
- **Standards** : Définissent le "Quoi" et le "Pourquoi" (Lois).
- **Agents/Profiles** : Définissent le "Qui" (Personnages).
- **Skills/Workflows** : Définissent le "Comment" (Actions).
- Ces trois piliers doivent rester étanches.
