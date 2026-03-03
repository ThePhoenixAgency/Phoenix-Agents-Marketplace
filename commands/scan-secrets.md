---
name: scan-secrets
description: Scan rapide des secrets exposes dans le code (cles API, tokens, mots de passe, certificats)
argument-hint: "[path]"
allowed-tools: ["Read", "Glob", "Grep", "Write"]
---

# /security-audit:scan-secrets

Scan rapide des secrets exposes dans le code source.

## Execution

1. Identifier la cible (argument ou repertoire courant)
2. Scanner avec les patterns regex suivants :

### Patterns critiques
```
-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----      # Cles privees
(postgres|mysql|mongodb)(\+srv)?://[^:]+:[^@]+@      # Database URLs
```

### Patterns haute severite
```
xoxb-[0-9]{10,13}-[0-9]{10,13}[a-zA-Z0-9-]*          # Slack Bot Token
```

### Patterns generiques
```
(?i)(password|secret|api_key|api_secret|access_token)\s*[:=]\s*['"][^'"]{8,}['"]
DefaultEndpointsProtocol=https;AccountName=[^;]+;AccountKey=[^;]+
```

3. Ignorer les faux positifs :
   - Patterns: `YOUR_`, `REPLACE_`, `example`, `xxx`, `TODO`
   - Fichiers: `*.lock`, `node_modules/`, `vendor/`, `.git/`

4. Generer un rapport dans `docs/private/security/SECRETS_SCAN.md` :
```markdown
# Scan de Secrets
**Date**: YYYY-MM-DD
**Cible**: [path]

## Resultats
| Severite | Type | Fichier:Ligne | Valeur (masquee) | Action |
|----------|------|---------------|-------------------|--------|
```

5. S'assurer que `docs/private/` est dans `.gitignore`
