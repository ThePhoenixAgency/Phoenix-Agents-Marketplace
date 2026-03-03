---
name: report
description: Generer ou mettre a jour le rapport de securite consolide
argument-hint: "[path]"
allowed-tools: ["Read", "Glob", "Grep", "Write"]
---

# /security-audit:report

Generer ou consolider le rapport de securite a partir des audits existants.

## Execution

1. Verifier l'existence de rapports partiels dans `docs/private/security/` :
   - `SECRETS_SCAN.md` (scan de secrets)
   - `DEPS_AUDIT.md` (audit dependances)
   - `AUDIT_REPORT.md` (audit complet)
   - `REMEDIATION_PLAN.md` (plan de correction)

2. Si aucun rapport n'existe, informer l'utilisateur et suggerer :
   - `/security-audit:audit` pour un audit complet
   - `/security-audit:scan-secrets` pour un scan rapide
   - `/security-audit:check-deps` pour les dependances

3. Consolider tous les rapports dans `docs/private/security-audit.md` en ajoutant les liens vers `/private/securite/` :
```markdown
# Rapport d'Audit de Securite

**Date**: YYYY-MM-DD
**Cible**: [project-name]
**Version**: X.X.X

## Resume Executif
[Synthese non-technique pour stakeholders]

## Matrice de Severite
| Severite | Nombre | Statut |
|----------|--------|--------|
| CRITIQUE | X | Corrige / En cours / A faire |
| HAUTE    | X | ... |
| MOYENNE  | X | ... |
| BASSE    | X | ... |

## Findings
[Consolide depuis AUDIT_REPORT.md]

## Secrets Exposes
[Consolide depuis SECRETS_SCAN.md]

## Dependances Vulnerables
[Consolide depuis DEPS_AUDIT.md]

## Plan de Remediation
[Consolide depuis REMEDIATION_PLAN.md]
1. [Priorite 1] ...
2. [Priorite 2] ...

## Checklist Zero Trust
- [ ] Secrets en dur dans le code ?
- [ ] Entrees utilisateur validees/sanitisees ?
- [ ] Principe du moindre privilege respecte ?
- [ ] Dependances vulnerables corrigees ?
- [ ] Documents sensibles exclus de Git ?
- [ ] Chiffrement en transit (TLS 1.2+) ?
- [ ] Headers de securite configures ?
- [ ] CORS restrictif ?
```

4. S'assurer que `docs/private/` est dans `.gitignore`
5. Réécrire `/private/securite/AUDIT_JOURNAL.md` (bloc unique, aucune duplication) pour refléter les actions de consolidation et noter si « Reste à faire » est à zéro.
