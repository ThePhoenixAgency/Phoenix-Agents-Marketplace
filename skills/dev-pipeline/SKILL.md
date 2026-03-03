---
name: dev-pipeline
description: Utiliser pour developper une feature complete, suivre le pipeline 9 phases, orchestrer les agents specialises. Declenche sur "developpe", "cree", "implemente", "nouvelle feature", "pipeline", "mode FULL/QUICK/RESEARCH/APPLE/SECURITY".
version: 2.1.0
author: EthanBernier
team: PhoenixProject
created: 2026-02-25
last_updated: 2026-03-03
---
# en francais toujours

# DEV PIPELINE

Pipeline de developpement en 9 phases avec agents specialises.
Optimise pour l'economie de tokens et la reduction des hallucinations.

## Skill requis

**Charger avant de demarrer** :
```
skills/governance-standards/SKILL.md   # Standards immuables S00-S08
```
Le `standards-enforcer` tourne EN PARALLELE a chaque phase cle (non-bloquant).

## MODES DE COLLABORATION

### Mode Collaboratif (Multi-Agents)
Chaque phase est deleguee a l'agent dedie. Le transfert de contexte se fait
par la lecture des fichiers produits dans les dossiers de documentation.

### Mode Autonome (Solo-Agent)
L'agent unique execute l'integralite du pipeline en changeant de posture.
- **Action** : Annoncer "[POSTURE] Je passe en role ARCHITECTE pour cette phase."
- **Rigueur** : Appliquer les checklists du profil concerne (dans `agents/`).

## MODES D'EXECUTION

| Mode | Phases | Usage |
|------|--------|-------|
| FULL | 1-9 | Projets critiques |
| QUICK | 4-5-6 | Corrections mineures |
| RESEARCH | 1-3 | Analyse sans code |
| APPLE | 1-9 + HIG | Ecosysteme Apple |
| SECURITY | Phase 6 | Audit securite standalone |

## PHASES ET AGENTS

| Phase | Agent | Modele | Mission |
|-------|-------|--------|---------|
| 1 | project-classifier | haiku | Analyser et orienter |
| 2 | spec-writer | sonnet | Specifications |
| 3 | web-researcher | haiku | Validation stack |
| 4 | architect | sonnet | Conception |
| 5 | implementer | sonnet | TDD, code |
| 6 | security-reviewer | sonnet | Audit securite Zero Trust |
| 7 | qa-tester | sonnet | Tests |
| 8 | accessibility-auditor | haiku | WCAG 2.2 |
| 9 | performance-auditor | haiku | Optimisation (INP, LCP, CLS) |
| * | tech-lead | sonnet | Supervision |
| * | hub-manager | haiku | Backlog, changelog |
| PARALLELE | standards-enforcer | haiku | Governance S00-S08 (non-bloquant) |

## INTEGRATION STANDARDS (OBLIGATOIRE)

Le `standards-enforcer` est invoque EN PARALLELE a 3 moments cles :

```
# Phase 2 — Spec gate : S04 Anti-Rush valide
Task("standards-enforcer", "Valider S04 Anti-Rush : spec complete avant code")

# Phase 5 — Post-implementation : S00 S02 S03 S04
Task("standards-enforcer", "Valider S00/S02/S03/S04 sur les fichiers modifies")

# Phase 6 — Pre-commit : S01 S02 Zero Trust
Task("standards-enforcer", "Valider S01 Zero Trust et S02 Commit format")
```

Rapport des violations dans `private/governance/VIOLATIONS.md` (gitignored).

## WORKFLOW DETAILLE PAR PHASE

### PHASE 1 - CLASSIFICATION (Posture : CLASSIFICATEUR)
Analyser demande, choisir mode (FULL/QUICK/RESEARCH/APPLE/SECURITY), identifier risques.
Lire l'existant avant de classifier. Si ambigu : poser UNE question.

### PHASE 2 - SPECIFICATION (Posture : REDACTEUR-SPECS)
Transformer une idee en document technique exploitable.
- Recueillir besoins et rediger recits utilisateur
- Criteres d'acceptation testables
- Exigences non-fonctionnelles (securite, perf, RGPD)
- Perimetre In-Scope / Out-of-Scope
- **[PARALLELE]** `standards-enforcer` : S04 Anti-Rush (spec validee avant code)
- Livrables : `/docs/specs/SPECIFICATIONS.md`, `/docs/private/security.md`

### PHASE 3 - RECHERCHE (Posture : CHERCHEUR-WEB)
Valider la faisabilite technique et s'appuyer sur les skills :
- `skills/web-research/` pour le protocole de recherche
- Sources Tier 1 (doc officielle) > Tier 2 (StackOverflow) > Tier 3 (articles)
- Croiser 2 sources minimum, citer les URLs
- Livrables : `/docs/research/RESEARCH_REPORT.md`

### PHASE 4 - ARCHITECTURE (Posture : ARCHITECTE)
Concevoir les fondations du logiciel.
- Structure technique, choix technos
- Interfaces et contrats entre composants
- Principes SOLID, KISS, Separation des responsabilites
- Livrables : `/docs/architecture/ARCHITECTURE.md`, `/docs/private/security.md`

### PHASE 5 - IMPLEMENTATION (Posture : IMPLEMENTEUR)
Produire du code robuste en TDD strict.
- RED : Ecrire le test qui echoue
- GREEN : Code minimal pour passer le test
- REFACTOR : Nettoyer sans casser
- Couverture > 90%, zero TODO/pass/mock
- **[PARALLELE]** `standards-enforcer` : S00/S02/S03/S04 sur fichiers modifies
- Secrets documentes uniquement dans `/docs/private/security.md`

### PHASE 6 - SECURITE (Posture : REVISEUR-SECURITE)
Garantir l'integrite du code selon Zero Trust.
- Executer `scripts/pipeline/40_audit-security.sh`
- Skills : `security-audit`, `security-best-practices`, `security-threat-model`
- OWASP Top 10, scan secrets, CVE/CWE
- **[PARALLELE]** `standards-enforcer` : S01 Zero Trust + S02 Commit format
- Livrables : `/docs/private/security.md`

### PHASE 7 - QUALITE (Posture : TESTEUR-QA)
Valider le bon fonctionnement.
- Tests unitaires, integration, bout en bout
- Cas limites et regression avant prod
- Livrables : `/docs/tests/TEST_PLAN.md`, `BUG_REPORTS.md`

### PHASE 8 - ACCESSIBILITE (Posture : AUDITEUR-ACCESSIBILITE)
Inclusion de tous les utilisateurs.
- WCAG 2.2 AA/AAA, VoiceOver, NVDA
- Navigation clavier, contrastes, labels, ARIA, semantique
- Dynamic Type (iOS/macOS) en mode APPLE
- Livrables : `/docs/accessibility/ACCESSIBILITY_REPORT.md`

### PHASE 9 - PERFORMANCE (Posture : AUDITEUR-PERFORMANCE)
Optimisation de la rapidite.
- Core Web Vitals : LCP < 2.5s, INP < 200ms, CLS < 0.1
- Instruments/Time Profiler en mode APPLE
- Livrables : `/docs/performance/PERFORMANCE_REPORT.md`

### SUPERVISION (Posture : CHEF-TECHNIQUE)
Coordonner phases, valider etapes, resoudre blocages.
Garantir BACKLOG.md et CHANGELOG.md a jour.

## OPTIMISATION TOKENS
- Phases 1, 3, 8, 9 et hub-manager utilisent **haiku** (taches systematiques)
- Phases 2, 4, 5, 6, 7 et tech-lead utilisent **sonnet** (raisonnement complexe)
- standards-enforcer utilise **haiku** (checks automatises en arriere-plan)
- Chaque agent doit etre concis et factuel

## ANTI-HALLUCINATION (TOUTES PHASES)
- Lire le code/docs existant AVANT de produire quoi que ce soit
- Ne JAMAIS inventer des APIs, versions, endpoints, ou vulnerabilites
- Citer les fichiers/lignes sources pour chaque affirmation
- Marquer "[HYPOTHESE]" toute supposition non validee
- Utiliser "[NOT FOUND]" quand une info n'est pas trouvable

## SUPPORT DOCUMENTS
- Si l'utilisateur fournit un document (spec, audit, brief, schema) : le lire INTEGRALEMENT
- Baser le travail sur le document fourni avant tout raisonnement autonome

## MODE APPLE
Quand le mode APPLE est active, les standards suivants s'appliquent en plus :
- Lire : `standards/domain_specific/APPLE_STANDARDS.md`
- **Design HIG** : Composants systeme, animations fluides, Dark Mode, SF Symbols
- **Technique** : Swift/SwiftUI prioritaire, optimisation memoire/batterie, sandboxing
- **Accessibilite** : VoiceOver complet, Dynamic Type, palettes couleurs systeme
- **Deploiement** : App Store ready, profils provisionnement, certificats signature

## PROTOCOLE
1. **START** : Lire `skills/governance-standards/SKILL.md`, `docs/BACKLOG.md`, `docs/checklog.md`
2. **PRE-IMPLEMENTATION** : Valider phase 3 (web-research) avec preuves OWASP/CVE avant d'ecrire du code
3. **PROCESS** : Appliquer regles sans deviation, annoncer "[POSTURE] NOM-AGENT"
4. **IMPLEMENTATION** : TDD stricte (RED/GREEN/REFACTOR), tests ecrits/ajustes avant validation
5. **END** : Mettre a jour `docs/BACKLOG.md`, `docs/checklog.md` et `CHANGELOG.md`

## SCRIPTS PIPELINE
Les scripts dans `scripts/pipeline/` sont executables dans l'ordre :
- `00_preflight.sh` : Verification pre-vol
- `10_spec_gate.sh` : Validation specifications
- `20_develop.sh` : Developpement
- `30_tests.sh` : Tests
- `40_audit-security.sh` : Audit securite automatise
- `50_human-validation.sh` : Validation humaine
- `60_deploy.sh` : Deploiement
- `70_post-deploy-verify.sh` : Verification post-deploiement

## METHODOLOGIE TRANSVERSALE
- **Annonce de posture** : Obligatoire en mode solo pour garantir la transparence
- **TDD strict** : Independant du mode de collaboration
- **Securisation systematique** : Toutes les postures doivent proteger les donnees privees
- **Economie de tokens** : Reponses concises, pas de repetitions inutiles
- **Cycle operationnel** : lecture backlog/checklog, preuve securite web, test+`docs/checklog.md` apres implementation
