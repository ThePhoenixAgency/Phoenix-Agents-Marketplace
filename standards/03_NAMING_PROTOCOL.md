---
version: 1.0.1
last_updated: 2026-02-04
author: PhoenixProject
status: Stable
---

# PROTOCOLE DE NOMMAGE & CONVENTIONS

## PROTOCOLE D'EXÉCUTION OBLIGATOIRE
1.  **START** : Lire `docs/BACKLOG.md` et les Standards de Gouvernance.
2.  **PROCESS** : Appliquer les règles sans déviation.
3.  **END** : Mettre à jour `docs/BACKLOG.md` et `docs/CHANGELOG.md` avant tout commit.

### 1. AUTORITÉ DE NOMMAGE (Projet)

- [FORBIDDEN] **L'IA NE DOIT JAMAIS INVENTER LE NOM DU PROJET.**
- "Phoenix Project" est le nom de l'entité/organisation, PAS le nom du logiciel.
- Si un nom est nécessaire, l'IA doit **demander** ou proposer une session de brainstorming ("On cherche un nom ensemble ?").
- Le nom final est **toujours** validé par l'humain.
- Pas de noms génériques par défaut (ex: "SmartApp", "AI-Bot").

### 2. CONVENTIONS DE FICHIERS (Anti-Spaghetti)

Les noms de fichiers doivent être courts, lisibles et professionnels.

- [FORBIDDEN] **Noms à rallonge** : `user_authentication_management_service_controller.ts` (Illisible).
- [FORBIDDEN] **Espaces ou caractères spéciaux** (Accents, émojis).
- [OK] **Court et Percutant** : 2 à 3 mots maximum.
- [OK] **Exemples** :
    - `AuthService.ts`
    - `UserLogin.tsx`
    - `api/routes.js`

### 3. CONVENTIONS DE CODE

- **Variables/Fonctions** : `camelCase`.
- **Classes/Composants** : `PascalCase`.
- **Constantes** : `UPPER_SNAKE_CASE`.
- **Langue** : Anglais technique US (sauf demande spécifique du projet).
