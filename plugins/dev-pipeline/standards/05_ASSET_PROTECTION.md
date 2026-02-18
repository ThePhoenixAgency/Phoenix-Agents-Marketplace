---
version: 1.0.1
last_updated: 2026-02-04
author: PhoenixProject
status: Stable
---

# ASSET PROTECTION & DATA SAFETY

## PROTOCOLE D'EXÉCUTION OBLIGATOIRE
1.  **START** : Lire `docs/BACKLOG.md` et les Standards de Gouvernance.
2.  **PROCESS** : Appliquer les règles sans déviation.
3.  **END** : Mettre à jour `docs/BACKLOG.md` et `docs/CHANGELOG.md` avant tout commit.

### LA LOI DU BACKLOG
La seule protection fiable contre la destruction accidentelle est le respect strict du périmètre défini.

1.  **Backlog Driven Modification** : L'IA n'a le droit de modifier ou supprimer un fichier QUE si c'est explicitement nécessaire pour une tâche active du `BACKLOG.md`.
2.  **Hors Scope = Intouchable** : Si un fichier n'est pas lié à la tâche en cours, il est en lecture seule absolue.
3.  **Vérification Active** : Avant toute suppression massive (`rm`, clean-up), l'IA doit vérifier le `BACKLOG.md` pour s'assurer que ces assets ne sont pas des pré-requis pour une tâche future.

### ANTI-DESTRUCTION
- [FORBIDDEN] Supprimer des fichiers "au cas où" ou pour "nettoyer" sans mandat explicite dans le ticket en cours.
- [OK] La propreté du code est importante, mais l'intégrité du projet prime.
