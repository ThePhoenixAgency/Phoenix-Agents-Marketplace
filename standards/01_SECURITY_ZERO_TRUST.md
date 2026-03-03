---
version: 1.0.1
last_updated: 2026-02-04
author: PhoenixProject
status: Stable
---

# SÉCURITÉ - ZERO TRUST (Repository PUBLIC)

## PROTOCOLE D'EXÉCUTION OBLIGATOIRE
1.  **START** : Lire `docs/BACKLOG.md` et les Standards de Gouvernance.
2.  **PROCESS** : Appliquer les règles sans déviation.
3.  **END** : Mettre à jour `docs/BACKLOG.md` et `docs/CHANGELOG.md` avant tout commit.

**RÈGLE #1 : Ce repository est considéré PUBLIC par défaut (Codeberg/GitLab)**

La sécurité n'est pas une option, c'est la fondation. "Zero Trust" signifie que nous supposons toujours que le réseau est hostile et que le code peut fuiter.

### JAMAIS COMMITTER DANS GIT (`/docs/` ou root)

Les types de documents suivants sont **STRICTEMENT INTERDITS** dans tout dossier public ou commit :

- [ERROR] **Threat Models** (Analyses de menaces, vecteurs d'attaque).
- [ERROR] **Rapports d'Audit** (Vulnérabilités trouvées, Pentests).
- [ERROR] **Rapports de Remédiation** (Comment nous avons corrigé les failles).
- [ERROR] **Architecture de Sécurité** (Détails des firewalls, gestion des clés).
- [ERROR] **Secrets & Credentials** (Même cryptés, pas de .env, pas de clés).
- [ERROR] **Données Personnelles (PII)** (GDPR compliance).
- [ERROR] **Contacts d'Urgence / Pro** (Numéros personnels des devs).

### ZONE SÉCURISÉE : `/private/`

Tout document sensible doit résider EXCLUSIVEMENT dans le dossier `/private/`.

- Le dossier `/private/` doit être impérativement listé dans `.gitignore`.
- Il est réservé à l'usage local du développeur.

### PROTECTIONS ACTIVES (CI/CD)

1.  **Gitleaks** : Hook Pre-commit OBLIGATOIRE pour scanner les secrets (API keys, tokens).
2.  **CI Check `check-sensitive-docs`** : Le pipeline doit échouer (`allow_failure: false`) si des fichiers interdits (regex: `THREAT-MODEL`, `VULNERABILITY`) sont détectés hors de `/private/`.
