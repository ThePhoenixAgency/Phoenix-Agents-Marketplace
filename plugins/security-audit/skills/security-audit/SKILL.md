---
name: Security Audit
description: This skill should be used when the user asks to "audit security", "scan for vulnerabilities", "check CVE", "find secrets", "security review", "OWASP check", "penetration test", "scan credentials", "check dependencies", "security by design", or mentions CVE, CWE, CVSS, OWASP, MITRE, NIST, CERT, Zero Trust, SAST.
version: 1.0.0
---

# Security Audit - Guide Complet

Audit de securite complet avec recherche CVE/CWE/OWASP/MITRE/NIST/CERT, detection de secrets, et remediation.

## Protocole d'Execution

1. **START** : Lire `docs/BACKLOG.md` et les Standards de Gouvernance si existants
2. **PROCESS** : Appliquer les regles Zero Trust sans deviation
3. **END** : Mettre a jour `docs/BACKLOG.md` et `docs/CHANGELOG.md`, generer rapport dans `docs/private/security-audit.md`

## Bases de Donnees de Vulnerabilites

| Priorite | Base | URL | Usage |
|----------|------|-----|-------|
| 1 | NVD/CVE | nvd.nist.gov | CVE specifiques, scores CVSS |
| 2 | OWASP | owasp.org | Risques web Top 10 |
| 3 | CWE | cwe.mitre.org | Classification faiblesses |
| 4 | MITRE ATT&CK | attack.mitre.org | Techniques d'attaque |
| 5 | NIST | csrc.nist.gov | Standards securite |
| 6 | CERT/CC | kb.cert.org | Advisories |

### Requetes de Recherche

```
# NVD
WebSearch: site:nvd.nist.gov "[product]" "[version]" vulnerability

# OWASP
WebSearch: site:owasp.org "[vulnerability-type]" prevention

# CWE
WebSearch: site:cwe.mitre.org "CWE-[ID]"
```

## Top 50 Vulnerabilites a Verifier

### Injection (CWE-89, 78, 94)
- SQL Injection, OS Command Injection, Code Injection
- **Test**: `' OR '1'='1`, `; ls -la`, `{{7*7}}`

### Authentication (CWE-287, 384, 352)
- Broken Auth, Session Fixation, CSRF
- **Test**: Token prediction, session replay

### Access Control (CWE-862, 639, 22)
- Missing Authorization, IDOR, Path Traversal
- **Test**: ID enumeration, `../../../etc/passwd`

### XSS (CWE-79)
- Reflected, Stored, DOM-based
- **Test**: `<script>alert(1)</script>`, `javascript:alert(1)`

### Cryptography (CWE-327, 311, 312)
- Weak crypto, Missing encryption
- **Check**: MD5, SHA1, DES, ECB mode

### SSRF/XXE (CWE-918, 611)
- Server-Side Request Forgery, XML External Entity
- **Test**: `http://169.254.169.254`, `<!ENTITY xxe SYSTEM "file:///etc/passwd">`

## Detection de Secrets - Patterns Regex

### Cloud Providers
```regex
# AWS
(?<![A-Za-z0-9/+=])[A-Za-z0-9/+=]{40}(?![A-Za-z0-9/+=])

# GCP

# Azure
DefaultEndpointsProtocol=https;AccountName=[^;]+;AccountKey=[^;]+
```

### Tokens
```regex
# GitHub

# Slack
xoxb-[0-9]{10,13}-[0-9]{10,13}[a-zA-Z0-9-]*

# Stripe
```

### Credentials
```regex
# Private Keys
-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----

# Database URLs
(postgres|mysql|mongodb)(\+srv)?://[^:]+:[^@]+@

# Generic
(?i)(password|secret|api_key)\s*[:=]\s*['"][^'"]{8,}['"]
```

### Faux Positifs a Ignorer
- `sk_test_`, `pk_test_`
- Patterns: `YOUR_`, `REPLACE_`, `example`, `xxx`

## Audit de Dependances

### Commandes par Ecosysteme
```bash
# Node.js
npm audit --json

# Python
pip-audit --format json
safety check --json

# PHP
composer audit

# Ruby
bundle audit

# Go
govulncheck ./...
```

## Scores CVSS v3.1

| Score | Severite | Action |
|-------|----------|--------|
| 9.0-10.0 | CRITIQUE | Correction immediate |
| 7.0-8.9 | HAUTE | Correction urgente |
| 4.0-6.9 | MOYENNE | Planifier correction |
| 0.1-3.9 | BASSE | Evaluer le risque |

### Vecteurs Critiques Communs
```
# RCE sans auth
CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H = 9.8

# SQL Injection
CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N = 9.1

# Auth Bypass
CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N = 8.2
```

## Patterns de Code Securise

### Input Validation
```python
# Whitelist validation
import re
ALLOWED = re.compile(r'^[a-zA-Z0-9_-]{1,50}$')
def validate(input):
    if not ALLOWED.match(input):
        raise ValueError("Invalid input")
```

### SQL Injection Prevention
```python
# Prepared statements
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

### XSS Prevention
```javascript
// Encode output
const safe = str.replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#x27;'
}[c]));
```

### Password Hashing
```python
import bcrypt
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))
```

## Checklist Zero Trust

- [ ] Secrets en dur dans le code ?
- [ ] Entrees utilisateur validees/sanitisees ?
- [ ] Principe du moindre privilege respecte ?
- [ ] Dependances vulnerables identifiees ?
- [ ] Documents sensibles exclus de Git ?
- [ ] Chiffrement en transit (TLS 1.2+) ?
- [ ] Chiffrement au repos ?
- [ ] Logging des acces sensibles ?
- [ ] Headers de securite configures ?
- [ ] CORS restrictif ?

## Format du Rapport

Generer dans `docs/private/security-audit.md` (gitignore) :

```markdown
# Rapport d'Audit de Securite

**Date**: YYYY-MM-DD
**Cible**: [path/url]

## Resume Executif
[Pour stakeholders non-techniques]

## Matrice de Severite
| Severite | Nombre |
|----------|--------|
| CRITIQUE | X |
| HAUTE | X |

## Findings

### [CRITIQUE] [Titre]
- **CWE**: CWE-XXX
- **CVSS**: X.X
- **Fichier**: `path:line`
- **Description**: ...
- **POC Payload**: `...`
- **Remediation**: ...

## Secrets Exposes
| Type | Fichier | Valeur |
|------|---------|--------|

## Plan de Remediation
1. [Priorite 1] ...
2. [Priorite 2] ...

## Checklist
[x] ou [ ] pour chaque item
```

## Livrables

1. `docs/private/security-audit.md` - Rapport principal (FR)
2. `docs/private/security/AUDIT_REPORT.md` - Details techniques
3. `docs/private/security/REMEDIATION_PLAN.md` - Plan de correction

4. `private/securite/AUDIT_JOURNAL.md` - Journal unique (cases cochées, commentaires et « Reste à faire : 0 »). Réécrire ce bloc sans dupliquer les lignes à chaque passage.

S'assurer que `docs/private/` est dans `.gitignore`.
