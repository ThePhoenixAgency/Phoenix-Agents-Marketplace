# Security Audit Plugin

Plugin Claude Code pour l'audit de securite complet avec recherche contextuelle sur les bases de donnees de vulnerabilites.

## Fonctionnalites

- **Recherche multi-sources** : CVE, CWE, CVSS, OWASP Top 10, MITRE ATT&CK, NIST NVD, CERT/CC
- **Analyse Top 50** : Vulnerabilites contextuelles selon la stack technique
- **Detection de secrets** : Regex pour 50+ types (AWS, GCP, Azure, GitHub, Stripe, etc.)
- **POC Payloads** : Charges de test pour chaque vulnerabilite
- **Remediation** : Corrections automatiques et patterns de code securise
- **Rapports** : Format Markdown en francais dans `docs/private/`

## Installation

```bash
claude --plugin-dir /path/to/security-audit
```

## Commandes

| Commande | Description |
|----------|-------------|
| `/security-audit:audit [target]` | Audit complet (code + deps + secrets) |
| `/security-audit:scan-secrets` | Scan rapide des secrets exposes |
| `/security-audit:check-deps` | Verification des dependances vulnerables |
| `/security-audit:report` | Generer/mettre a jour le rapport |

## Agents

| Agent | Role |
|-------|------|
| `security-reviewer` | Orchestrateur principal - Zero Trust, SAST, OWASP |
| `vulnerability-researcher` | Recherche web sur CVE/CWE/OWASP |
| `secret-scanner` | Detection de secrets avec valeurs exposees |
| `security-auditor` | Audit deps, vecteurs d'attaque, POC |

## Configuration

Creer `.claude/security-audit.local.md` pour personnaliser :

```markdown
# Security Audit Settings

## Severity Threshold
- minimum: high

## Ignored Patterns
- node_modules/
- vendor/
- .git/

## Custom Secret Patterns
- MY_CUSTOM_KEY=[A-Za-z0-9]{32}
```

## Livrables

```
docs/
└── private/
    └── security-audit.md      # Rapport principal (gitignored)

private/
└── securite/
    ├── AUDIT_JOURNAL.md       # Journal unique (cases cochées, reste à faire)
    ├── AUDIT_REPORT.md        # Détails techniques des findings
    └── REMEDIATION_PLAN.md    # Plan de correction Zero Trust
```

Le journal `/private/securite/AUDIT_JOURNAL.md` est réécrit en place à chaque exécution (pas de duplication de bloc) : on coche les actions réalisées, on note les commentaires et on laisse “Reste à faire : 0” à la fin de la chaîne.

## Hooks

- **Pre-commit** : Bloque les commits avec secrets exposes
- **Auto-audit** : Declenchement sur mots-cles securite

## Licence

MIT
