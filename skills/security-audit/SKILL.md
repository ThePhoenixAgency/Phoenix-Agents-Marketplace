---
name: security-audit
description: "Skill Zero Trust couvrant audits offensifs et defensifs : pentest web/API, OSINT, bug bounty, detection de secrets, revue de code securise, CVSS scoring, modelisation de menaces. Declencher pour : audit securite, pentest, OSINT, bug bounty, threat model, CVE/CWE/OWASP, scan secrets, revue code securise."
author: EthanBernier
team: PhoenixProject
version: 2.0.0
created: 2026-02-25
last_updated: 2026-03-03
---
# en francais toujours

# Security Audit — Skill Zero Trust

Skill autonome pour le spectre complet : defensif (revue code, threat model) et offensif (pentest, OSINT, bug bounty).

## Modules disponibles

Charger UNIQUEMENT les modules necessaires a la tache demandee.

| Module | Fichier | Quand l'utiliser |
|--------|---------|-----------------|
| Pentest Web/API | `references/pentest-web.md` | Tests d'intrusion, OWASP Top 10, SQLi, XSS, SSRF |
| OSINT/Recon | `references/osint-recon.md` | Reconnaissance passive, enumeration, metadata, fuites |
| Bug Bounty | `references/bugbounty-workflow.md` | Programmes bug bounty, scope, PoC, rapports HackerOne/Bugcrowd |
| Code securise | `references/secure-coding.md` | Regexes secrets, patterns securises par langage, audit deps |
| Ownership Map | `references/ownership-analysis.md` | Bus factor, code orphelin, propriete securite |
| Threat Model | `references/threat-modeling.md` | Modelisation de menaces AppSec, STRIDE, arbres d'attaque |

## Workflow Zero Trust

1. **SCOPE** : Identifier la cible et le type (pentest/OSINT/bug-bounty/code-review/threat-model)
2. **RECON** : Charger `references/osint-recon.md` si reconnaissance necessaire
3. **ANALYSE** : Charger le module adapte a la tache
4. **EXPLOITATION** : Documenter les vulnerabilites trouvees avec PoC et preuve reelle
5. **RAPPORT** : Generer dans `private/securite/` (gitignored)

## Regles d'engagement

- [CRITICAL] Securite OFFENSIVE uniquement sur cibles AUTORISEES (scope valide)
- [CRITICAL] Tous les rapports dans `private/` — jamais en clair dans le repo
- [CRITICAL] Jamais de credentials, tokens, ou secrets dans les rapports
- Si le scope n'est pas clair : STOP et demander confirmation explicite

## Anti-Hallucination

- Ne JAMAIS inventer une vulnerabilite qui n'existe pas
- Citer fichier + ligne exacte pour chaque finding
- Marquer `[CONFIRMED]` (verifie) vs `[SUSPECTED]` (a confirmer manuellement)
- Executer les outils REELLEMENT — ne pas simuler les resultats
- Si un outil est absent : `[TOOL NOT AVAILABLE: <outil>]` puis continuer avec `curl`/`grep`

## Bases de donnees de vulnerabilites

| Priorite | Source | URL | Usage |
|----------|--------|-----|-------|
| 1 | NVD/CVE | nvd.nist.gov | CVE specifiques, scores CVSS |
| 2 | OWASP | owasp.org | Top 10 risques web |
| 3 | CWE | cwe.mitre.org | Classification des faiblesses |
| 4 | MITRE ATT&CK | attack.mitre.org | Techniques d'attaque |
| 5 | NIST | csrc.nist.gov | Standards securite |
| 6 | CERT/CC | kb.cert.org | Advisories |

Requetes types :
```
site:nvd.nist.gov "[product]" "[version]" vulnerability
site:owasp.org "[vulnerability-type]" prevention
site:cwe.mitre.org "CWE-[ID]"
```

## Scores CVSS v3.1

| Score | Severite | Action |
|-------|----------|--------|
| 9.0–10.0 | CRITIQUE | Correction immediate |
| 7.0–8.9 | HAUTE | Correction urgente (<72h) |
| 4.0–6.9 | MOYENNE | Planifier correction |
| 0.1–3.9 | BASSE | Evaluer le risque |

Vecteurs critiques communs :
```
RCE sans auth   : CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H = 9.8
SQL Injection   : CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N = 9.1
Auth Bypass     : CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N = 8.2
```

## Classification des findings

| Severite | Critere | Exemple |
|----------|---------|---------|
| CRITICAL | RCE, auth bypass, data breach | Injection SQL non sanitisee |
| HIGH | Escalade privileges, SSRF interne | IDOR sur endpoints admin |
| MEDIUM | XSS stocke, info disclosure | Headers de securite manquants |
| LOW | Info leak mineur, best practices | Version serveur exposee |
| INFO | Observation sans impact direct | Stack technique identifiee |

## Checklist Zero Trust

- [ ] Secrets en dur dans le code ?
- [ ] Entrees utilisateur validees et sanitisees ?
- [ ] Principe du moindre privilege respecte ?
- [ ] Dependances vulnerables identifiees ?
- [ ] Documents sensibles dans `.gitignore` ?
- [ ] Chiffrement en transit (TLS 1.2+) ?
- [ ] Chiffrement au repos ?
- [ ] Logging des acces sensibles ?
- [ ] Headers de securite configures ?
- [ ] CORS restrictif ?

## Audit de dependances

```bash
npm audit --json           # Node.js
pip-audit --format json    # Python
safety check --json        # Python (alternatif)
composer audit             # PHP
bundle audit               # Ruby
govulncheck ./...          # Go
```

## Format de rapport

```markdown
# Rapport d'Audit Securite — [CIBLE]
Date : YYYY-MM-DD
Type : PENTEST/OSINT/BUG-BOUNTY/CODE-REVIEW/THREAT-MODEL
Scope : [description de la cible]

## Resume executif
[3–5 lignes, non-technique, pour stakeholders]

## Matrice de severite
| Severite | Nombre |
|----------|--------|
| CRITIQUE | X |
| HAUTE    | X |
| MOYENNE  | X |
| BASSE    | X |

## Findings

### [CRITICAL-001] Titre du finding
- **Severite** : CRITICAL
- **CWE** : CWE-89
- **Localisation** : `fichier:ligne` ou URL
- **Description** : [factuel, sans speculation]
- **Preuve** : [commande executee + output reel]
- **Impact** : [concret et mesurable]
- **Remediation** : [action precise et verifiable]

## Secrets exposes
| Type | Fichier | Valeur masquee | Action immediate |
|------|---------|----------------|-----------------|

## Plan de remediation
1. [Priorite immediate — sous 24h]
2. [Court terme — sous 7j]
3. [Moyen terme — sous 30j]
```

## Livrables

- `private/securite/AUDIT_JOURNAL.md` — Journal unique (cases cochees, "Reste a faire : 0"). Reecrire en place sans duplication de bloc.
- `private/securite/AUDIT_REPORT.md` — Details techniques des findings
- `private/securite/REMEDIATION_PLAN.md` — Plan de correction priorise

S'assurer que `private/` est dans `.gitignore`.

## Integration pipeline

Ce skill est utilise par `security-reviewer` et `security-auditor` en Phase 6 du dev-pipeline.
Script associe : `scripts/pipeline/40_audit-security.sh`
Sous-agents : `vulnerability-researcher` (recherche CVE), `secret-scanner` (detection secrets)
