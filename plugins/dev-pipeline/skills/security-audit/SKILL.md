---
name: "security-audit"
description: "Skill modulaire de securite offensive et defensive. Couvre pentest web/API, OSINT/reconnaissance, bug bounty, revue code securise, analyse de propriete, et modelisation de menaces. Declencher quand l'utilisateur demande un audit securite, un pentest, de l'OSINT, un bug bounty, un threat model, ou une revue securite de code. Ne PAS declencher pour du debug, de la revue de code generale, ou des taches non-securite."
---
# en francais toujours

# Security Audit - Skill Modulaire

Skill de securite autonome pour agent specialise. Couvre l'ensemble du spectre
securite : defensif (revue code, threat model) et offensif (pentest, OSINT, bug bounty).

## Modules disponibles

Chaque module est un fichier dans `references/`. Charger UNIQUEMENT les modules
necessaires a la tache demandee.

| Module | Fichier | Quand l'utiliser |
|--------|---------|-----------------|
| Pentest Web/API | `references/pentest-web.md` | Tests d'intrusion, OWASP Top 10, SQLi, XSS, SSRF |
| OSINT/Recon | `references/osint-recon.md` | Reconnaissance passive, enumeration, metadata, fuites |
| Bug Bounty | `references/bugbounty-workflow.md` | Programmes de bug bounty, scope, PoC, rapports |
| Best Practices | `references/secure-coding.md` | Revue code par langage/framework |
| Ownership Map | `references/ownership-analysis.md` | Bus factor, code orphelin, propriete securite |
| Threat Model | `references/threat-modeling.md` | Modelisation de menaces AppSec |

## Workflow general

1. **SCOPE** : Identifier la cible (repo, URL, scope bug bounty) et le type d'audit
2. **RECON** : Charger le module OSINT si reconnaissance necessaire
3. **ANALYSE** : Charger le module adapte (pentest, best-practices, threat-model)
4. **EXPLOITATION** : Documenter les vulnerabilites trouvees avec PoC
5. **RAPPORT** : Generer le rapport dans `/private/securite/`

## Regles d'engagement

- [CRITICAL] Securite OFFENSIVE uniquement sur cibles AUTORISEES (scope valide)
- [CRITICAL] Tous les rapports dans `/private/` (repo public)
- [CRITICAL] Jamais de credentials, tokens, ou secrets dans les rapports
- Si le scope n'est pas clair : STOP et demander confirmation

## Anti-Hallucination

- Ne JAMAIS inventer une vulnerabilite qui n'existe pas
- Citer fichier + ligne exacte pour chaque finding
- Marquer "[CONFIRMED]" (verifie) vs "[SUSPECTED]" (a confirmer)
- Executer les outils REELLEMENT, ne pas simuler les resultats
- Si un outil n'est pas disponible : dire "[TOOL NOT AVAILABLE]" et proposer une alternative

## Classification des findings

| Severite | Critere | Exemple |
|----------|---------|---------|
| CRITICAL | RCE, auth bypass, data breach | Injection SQL non sanitisee |
| HIGH | Escalade privileges, SSRF interne | IDOR sur endpoints admin |
| MEDIUM | XSS stocke, info disclosure limitee | Headers de securite manquants |
| LOW | Info leak mineur, bonnes pratiques | Version serveur exposee |
| INFO | Observation sans impact direct | Technologie stack identifiee |

## Format de rapport

```markdown
# Rapport d'Audit Securite - [CIBLE]
Date : [YYYY-MM-DD]
Type : [PENTEST/OSINT/BUG-BOUNTY/CODE-REVIEW/THREAT-MODEL]
Scope : [DESCRIPTION]

## Resume executif
[3-5 lignes max]

## Findings

### [SEVERITY-ID] Titre du finding
- **Severite** : CRITICAL/HIGH/MEDIUM/LOW/INFO
- **CWE** : CWE-XXX
- **Localisation** : fichier:ligne ou URL
- **Description** : [factuel, pas de speculation]
- **Preuve** : [commande executee + output reel]
- **Impact** : [concret et mesurable]
- **Remediation** : [action precise]

## Recommandations prioritaires
1. [Action immediate]
2. [Action court terme]
3. [Action moyen terme]
```

## Integration pipeline

Ce skill est utilise par l'agent `security-reviewer` en Phase 6 du dev-pipeline.
Script associe : `scripts/pipeline/40_audit-security.sh`
