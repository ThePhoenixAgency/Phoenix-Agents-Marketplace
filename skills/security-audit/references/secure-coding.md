# Code Securise — Patterns, Secrets & Dependances

## Detection de Secrets — Patterns Regex

### Providers Cloud
```regex
# AWS Access Key
# AWS Secret Key
(?<![A-Za-z0-9/+=])[A-Za-z0-9/+=]{40}(?![A-Za-z0-9/+=])
# GCP API Key
# Azure Connection String
DefaultEndpointsProtocol=https;AccountName=[^;]+;AccountKey=[^;]+
```

### Tokens et Credentials
```regex
# GitHub Personal Access Token
# GitHub Fine-grained PAT
# Slack Bot Token
xoxb-[0-9]{10,13}-[0-9]{10,13}[a-zA-Z0-9-]*
# Stripe Live Key
# Twilio Account SID
AC[a-zA-Z0-9]{32}
# SendGrid API Key
SG\.[a-zA-Z0-9_-]{22}\.[a-zA-Z0-9_-]{43}
# Mailchimp API Key
[a-f0-9]{32}-us[0-9]{1,2}
# JWT Token
eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}
```

### Cles Cryptographiques
```regex
# Cles privees RSA/EC/SSH
-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----
# Certificates
-----BEGIN CERTIFICATE-----
```

### URLs de Bases de Donnees
```regex
(postgres|mysql|mongodb)(\+srv)?://[^:]+:[^@]+@
redis://[^:]+:[^@]+@
```

### Generique
```regex
(?i)(password|passwd|secret|api_key|apikey|access_token|auth_token)\s*[:=]\s*['\"][^'\"]{8,}['\"]
```

### Faux Positifs a Ignorer
- `sk_test_`, `pk_test_`
- Patterns : `YOUR_`, `REPLACE_`, `<YOUR_`, `example`, `xxx`, `***`
- Variables de template : `${...}`, `{{...}}`, `%s`

## Patterns de Code Securise

### Validation d'Entrees (Python)
```python
import re
# Whitelist — refuser tout ce qui n'est pas autorise
ALLOWED = re.compile(r'^[a-zA-Z0-9_-]{1,50}$')
def validate_identifier(value: str) -> str:
    if not ALLOWED.match(value):
        raise ValueError(f"Entree invalide : {value!r}")
    return value
```

### Prevention Injection SQL
```python
# Prepared statements — TOUJOURS
cursor.execute("SELECT * FROM users WHERE id = %s AND active = %s", (user_id, True))
# JAMAIS : f"SELECT * FROM users WHERE id = {user_id}"
```

### Prevention XSS (JavaScript)
```javascript
// Encoder la sortie HTML
const encode = str => str.replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"''": '&quot;', "'": '&#x27;'
}[c]));
// Utiliser textContent au lieu de innerHTML
element.textContent = userInput; // Sûr
// element.innerHTML = userInput; // DANGEREUX
```

### Hachage de Mot de Passe
```python
import bcrypt
# Hachage
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12))
# Verification
bcrypt.checkpw(password.encode('utf-8'), hashed)
# JAMAIS : MD5, SHA1, SHA256 sans sel
```

### Headers de Securite HTTP
```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
Content-Security-Policy: default-src 'self'; script-src 'self'
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=()
```

### Principe du Moindre Privilege
```python
# Connexion DB en lecture seule si pas d'ecriture necessaire
conn = psycopg2.connect(dsn, user='readonly_user')
# Droits fichiers
os.chmod(config_file, 0o600)  # Uniquement proprietaire
```

## Audit de Dependances par Ecosysteme

```bash
# Node.js — audit + fix automatique si possible
npm audit --json
npm audit fix --dry-run

# Python
pip-audit --format json --output audit.json
safety check --json

# PHP
composer audit

# Ruby
bundle audit update && bundle audit

# Go
govulncheck ./...

# Java/Maven
mvn dependency:tree
mvn org.owasp:dependency-check-maven:check

# Rust
cargo audit
```

## OWASP Top 10 — Checklist Rapide

| # | Categorie | Test principal |
|---|-----------|----------------|
| A01 | Broken Access Control | IDOR, path traversal, privilege escalation |
| A02 | Cryptographic Failures | Secrets en dur, TLS faible, MD5/SHA1 |
| A03 | Injection | SQLi, XSS, OS command injection, SSTI |
| A04 | Insecure Design | Threat model absent, logique metier cassee |
| A05 | Security Misconfiguration | Default creds, debug actif, CORS *, erreurs verbeux |
| A06 | Vulnerable Components | Deps obsoletes, CVE connues |
| A07 | Auth Failures | Brute force, session fixation, JWT faible |
| A08 | Software Integrity | CI/CD non signe, deps non verifiees |
| A09 | Logging Failures | Pas de logs acces, logs avec secrets |
| A10 | SSRF | Requetes vers metadonnees cloud, services internes |
