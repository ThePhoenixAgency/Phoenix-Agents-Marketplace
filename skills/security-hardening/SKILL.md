---
name: security-hardening
description: Input validation, auth patterns, secrets management, CSP, Zero Trust
---

# Security Hardening

## Principes Zero Trust

Jamais faire confiance. Toujours verifier. Limiter les privileges.

## Input Validation

### Regles

```
TOUT input utilisateur DOIT etre :
1. Valide (type, format, longueur)
2. Assaini (escape, sanitize)
3. Borne (min/max, whitelist)
```

### Exemple

```javascript
const { z } = require('zod');

const userSchema = z.object({
  email: z.string().email().max(255),
  name: z.string().min(1).max(100).regex(/^[a-zA-Z\s-]+$/),
  age: z.number().int().min(0).max(150),
  role: z.enum(['user', 'admin', 'moderator']),
});

function validateInput(data) {
  return userSchema.safeParse(data);
}
```

## Secrets Management

```
[INTERDIT] Secrets en dur dans le code
[INTERDIT] Secrets dans les logs
[INTERDIT] Secrets dans les commits
[INTERDIT] Secrets dans les fichiers de config versiones

[OK] Variables d'environnement
[OK] KeyVault / Secret Manager
[OK] .env dans .gitignore
[OK] Rotation reguliere des secrets
```

## Content Security Policy

```
Content-Security-Policy:
  default-src 'self';
  script-src 'self' 'nonce-{random}';
  style-src 'self' 'unsafe-inline';
  img-src 'self' data: https:;
  font-src 'self';
  connect-src 'self' https://api.example.com;
  frame-ancestors 'none';
  base-uri 'self';
  form-action 'self';
```

## Headers de securite

```
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 0
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=()
```

## SQL Injection Prevention

```
[INTERDIT] "SELECT * FROM users WHERE id = " + userId
[OK] "SELECT * FROM users WHERE id = $1", [userId]
[OK] ORM avec parametres prepares
```

## OWASP Top 10 Checklist

- [ ] A01 Broken Access Control
- [ ] A02 Cryptographic Failures
- [ ] A03 Injection
- [ ] A04 Insecure Design
- [ ] A05 Security Misconfiguration
- [ ] A06 Vulnerable Components
- [ ] A07 Auth Failures
- [ ] A08 Software/Data Integrity Failures
- [ ] A09 Logging/Monitoring Failures
- [ ] A10 SSRF
