---
name: anomaly-weighting
description: CVSS v3.1 scoring methodology and CWE classification guide
author: PhoenixProject
version: 1.0.0
created: 2026-02-18
last_updated: 2026-02-23
---

# Vulnerability Scoring Skill

## When to Use

When assessing and classifying discovered vulnerabilities for Bug Bounty reports.

## CVSS v3.1 Base Score Components

### Attack Vector (AV)

| Value | Code | Meaning |
|-------|------|---------|
| Network | N | Exploitable remotely |
| Adjacent | A | Requires adjacent network |
| Local | L | Requires local access |
| Physical | P | Requires physical access |

### Attack Complexity (AC)

| Value | Code | Meaning |
|-------|------|---------|
| Low | L | No special conditions |
| High | H | Requires specific conditions |

### Privileges Required (PR)

| Value | Code | Meaning |
|-------|------|---------|
| None | N | No authentication needed |
| Low | L | Basic user access |
| High | H | Admin/privileged access |

### User Interaction (UI)

| Value | Code | Meaning |
|-------|------|---------|
| None | N | No user action needed |
| Required | R | Victim must perform action |

### Scope (S)

| Value | Code | Meaning |
|-------|------|---------|
| Unchanged | U | Impact limited to vulnerable component |
| Changed | C | Impact extends beyond |

### Impact (C/I/A)

| Value | Code | Meaning |
|-------|------|---------|
| None | N | No impact |
| Low | L | Partial impact |
| High | H | Total compromise |

## Common Vulnerability Scores

| Vulnerability | Typical CVSS | Vector |
|--------------|-------------|--------|
| RCE (unauthenticated) | 9.8 | AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H |
| SQL Injection (data access) | 8.6 | AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N |
| Auth Bypass | 9.1 | AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N |
| Stored XSS (admin) | 8.4 | AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N |
| IDOR (PII) | 6.5 | AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N |
| SSRF (internal) | 7.5 | AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N |
| CSRF (state change) | 4.3 | AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:N |
| Open Redirect | 3.4 | AV:N/AC:L/PR:N/UI:R/S:C/C:N/I:L/A:N |
| Info Disclosure | 5.3 | AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N |

## CWE Top 25 (Most Dangerous)

| Rank | CWE | Name |
|------|-----|------|
| 1 | CWE-787 | Out-of-bounds Write |
| 2 | CWE-79 | Cross-site Scripting |
| 3 | CWE-89 | SQL Injection |
| 4 | CWE-416 | Use After Free |
| 5 | CWE-78 | OS Command Injection |
| 6 | CWE-20 | Improper Input Validation |
| 7 | CWE-125 | Out-of-bounds Read |
| 8 | CWE-22 | Path Traversal |
| 9 | CWE-352 | Cross-Site Request Forgery |
| 10 | CWE-434 | Unrestricted File Upload |

## Severity to Payout Mapping

| Severity | CVSS Range | Typical BB Payout |
|----------|-----------|-------------------|
| Critical | 9.0 - 10.0 | $5,000 - $100,000+ |
| High | 7.0 - 8.9 | $1,000 - $15,000 |
| Medium | 4.0 - 6.9 | $250 - $3,000 |
| Low | 0.1 - 3.9 | $50 - $500 |
| Info | 0.0 | Usually not rewarded |

## Impact Quantification

Always quantify business impact in reports:

- **Data**: "Access to X records containing PII of Y users"
- **Financial**: "Allows bypassing payment of $Z per transaction"
- **Availability**: "Can take down service affecting N users"
- **Reputation**: "Public disclosure would affect trust of M customers"
