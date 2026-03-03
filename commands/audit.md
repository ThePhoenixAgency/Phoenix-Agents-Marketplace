---
name: audit
description: Audit de securite complet
argument-hint: "[target]"
allowed-tools: ["Read", "Write", "Glob", "Grep", "Bash", "WebSearch", "WebFetch", "Task"]
---

# /security-audit:audit

Effectuer un audit de securite complet.

## Execution

1. Identifier la cible (argument ou repertoire courant)
2. Creer `docs/private/security/` et `/private/securite/`, puis mettre à jour `/private/securite/AUDIT_JOURNAL.md` (bloc unique, cases cochées, commentaires).
3. Lancer en parallele avec Task :
   - Agent `security-reviewer` pour audit principal
   - Agent `secret-scanner` pour secrets
   - Agent `vulnerability-researcher` pour CVE
4. Consolider dans `docs/private/security-audit.md` (FR) et enregistrer les artefacts dans `/private/securite/` :
   - Resume executif
   - Matrice severite
   - Findings avec POC payloads
   - Secrets exposes (valeurs reelles)
   - Plan remediation
   - Checklist Zero Trust
