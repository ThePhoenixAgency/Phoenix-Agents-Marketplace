---
version: 1.0.1
last_updated: 2026-02-04
author: PhoenixProject
status: Stable
---

# ANTI-RUSH POLICY (VITAL)

## PROTOCOLE D'EXÉCUTION OBLIGATOIRE
1.  **START** : Lire `docs/BACKLOG.md` et les Standards de Gouvernance.
2.  **PROCESS** : Appliquer les règles sans déviation.
3.  **END** : Mettre à jour `docs/BACKLOG.md` et `docs/CHANGELOG.md` avant tout commit.

**"Pas de code sans boussole."**

### 1. LE VERROU DE SPÉCIFICATION

- [FORBIDDEN] **INTERDICTION FORMELLE** de commencer à coder tant que la phase de Spécification n'est pas **explicitement validée**.
- Ne pas polluer le contexte avec du code, des snippets ou des solutions techniques prématurées.
- Tant que le besoin ("Scope") n'est pas clair à 100%, l'IA doit rester en mode "Business Analyst / Architecte".
- **Signal de départ** : Attendre un "GO", "Valid", ou la commande slash `/start-coding`.

### 2. RIGUEUR D'EXÉCUTION (Une fois le code lancé)

- **PAS DE FAKE CODE** :
    - [FORBIDDEN] `// TODO: implement later`
    - [FORBIDDEN] `pass`
    - [FORBIDDEN] `return "mock data"`
    - Le code livré doit être complet, fonctionnel et testable localement.

- **STABILITÉ** :
    - [OK] Une interface (API/UI) validée est **GRAVÉE DANS LE MARBRE**.
    - [OK] On ne change plus une spec validée sur un coup de tête de l'IA.

- **ANTICIPATION** :
    - Si une question surgit après avoir écrit 500 lignes de code et oblige à tout refaire : **C'EST UN ÉCHEC MAJEUR**.
    - Les questions bloquantes doivent être posées AVANT d'écrire la première ligne.

### 3. TDD STRICT (Test First)

Pour TOUTE logique métier :
1.  **RED** : Écrire le test qui échoue (Spécification exécutable).
2.  **GREEN** : Écrire le code minimal pour passer le test.
3.  **REFACTOR** : Nettoyer.

**Pas de code métier sans test préalable.**
