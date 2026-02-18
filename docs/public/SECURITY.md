# Security Policy
<!-- Created: 2026-02-18 | Last Updated: 2026-02-18 -->

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly:

1. **Do not** create a public GitHub issue
2. Email: security@phoenixproject.dev (or use GitHub's private vulnerability reporting)
3. Include: description, reproduction steps, impact assessment
4. Expected response time: 48 hours

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | Yes       |

## Security Measures

- All inputs are validated
- No secrets in code (environment variables only)
- Dependencies scanned with `npm audit`
- Sensitive documents stored in `/private/` (gitignored)
- Pre-commit hooks block secrets via gitleaks
- SAST scanning available via `bash commands/security/sast-scan.sh`
