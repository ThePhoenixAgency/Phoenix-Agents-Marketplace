---
name: report-templates
description: Bug Bounty report templates for major platforms
author: PhoenixProject
version: 1.0.0
created: 2026-02-18
last_updated: 2026-02-23
---

# Report Templates Skill

## When to Use

When writing vulnerability reports for submission to Bug Bounty platforms.

## HackerOne Template

```markdown
## Summary

[One paragraph: what is the vulnerability, where does it exist, what is the impact]

## Severity

**CVSS Score**: X.X ([Critical/High/Medium/Low])
**CVSS Vector**: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H
**CWE**: CWE-XXX - [Name]

## Steps to Reproduce

1. Navigate to `https://target.com/endpoint`
2. Login with credentials (create test account)
3. Intercept request to `POST /api/v1/resource`
4. Modify parameter `id` from `123` to `456`
5. Forward the request
6. Observe unauthorized access to another user's data

## Proof of Concept

### Request

```http
POST /api/v1/resource HTTP/1.1
Host: target.com
Authorization: Bearer <token>
Content-Type: application/json

{"id": "456"}
```

### Response

```http
HTTP/1.1 200 OK
Content-Type: application/json

{"user": "victim@example.com", "data": "sensitive_info"}
```

### Screenshot

[Annotated screenshot showing the vulnerability]

## Impact

An attacker with a valid account can access any user's data by
changing the resource ID parameter. This affects approximately
X users and exposes [PII type].

**Business Impact**: Full compromise of user data confidentiality.

## Remediation

Implement server-side authorization checks:
- Verify the requesting user owns the resource
- Compare session user ID with resource owner ID
- Return 403 Forbidden for unauthorized access

## References

- CWE-639: Authorization Bypass Through User-Controlled Key
- OWASP: Insecure Direct Object References
```

## Bugcrowd Template

```markdown
## Title

[Vulnerability Type] in [Component] Allows [Impact]

## VRT Category

Server Security Misconfiguration > [Specific Category]

## URL / Location

`https://target.com/vulnerable-endpoint`

## Description

[Detailed technical description]

## Steps to Reproduce

[Numbered steps]

## PoC

[Code, curl command, or screenshot]

## Impact

[Business-focused impact description]

## Suggested Fix

[Remediation]
```

## Direct Program Template (Email/PDF)

```markdown
# Security Vulnerability Report

**Date**: YYYY-MM-DD
**Reporter**: [Name/Handle]
**Target**: [Program/Application]
**Classification**: CONFIDENTIAL

---

## Executive Summary

[Non-technical summary for management]

## Technical Details

**Vulnerability**: [Type]
**Severity**: [CVSS] - [Critical/High/Medium/Low]
**Affected Component**: [URL/Feature]
**CWE**: CWE-XXX

## Reproduction Steps

[Detailed numbered steps]

## Evidence

[Screenshots, logs, curl commands]

## Impact Assessment

- **Confidentiality**: [Impact]
- **Integrity**: [Impact]
- **Availability**: [Impact]
- **Affected Users**: [Estimated count]

## Recommended Remediation

[Technical fix with code examples]

## Timeline

| Date | Action |
|------|--------|
| YYYY-MM-DD | Vulnerability discovered |
| YYYY-MM-DD | Report submitted |
| YYYY-MM-DD | Vendor acknowledgment |
| YYYY-MM-DD + 90 days | Public disclosure deadline |
```

## Writing Tips

1. **Title**: Be specific. "XSS" is bad. "Stored XSS in user profile bio leads to account takeover" is good.
2. **Reproduction**: If the triager cannot reproduce it, it will be closed. Be exhaustive.
3. **Impact**: Think business, not just technical. "$10K revenue loss" > "integrity violation".
4. **PoC**: curl commands > screenshots. Reproducible > visual.
5. **Remediation**: Show you understand the fix. Include code when possible.
6. **Tone**: Professional, factual, no drama. "This vulnerability allows..." not "Your security is terrible."
