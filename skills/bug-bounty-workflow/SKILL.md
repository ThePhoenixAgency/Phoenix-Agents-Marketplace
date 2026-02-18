---
name: bug-bounty-workflow
description: Complete Bug Bounty hunting workflow from recon to submission
---

# Bug Bounty Workflow Skill

## When to Use

When conducting a Bug Bounty engagement on an authorized program.

## Prerequisites

- Authorized scope from Bug Bounty program
- OSINT toolkit installed (scripts/osint/)
- Pentesting tools: nmap, nuclei, ffuf, burp/caido
- Platform account (HackerOne, Bugcrowd, etc.)

## Phase 1: Program Selection

1. Review available programs on target platform
2. Evaluate scope breadth vs competition level
3. Check median payout and response time
4. Read program policy (out-of-scope, safe harbor)
5. Note recently added assets (less tested)

## Phase 2: Passive Reconnaissance

Use the `osint-recon` skill for full passive recon:

```bash
# Run all OSINT modules
python3 scripts/osint/cert_transparency.py <target> > /tmp/bb_ct.json
python3 scripts/osint/dns_enum.py <target> > /tmp/bb_dns.json
python3 scripts/osint/leak_scanner.py <target> > /tmp/bb_leaks.json
python3 scripts/osint/wayback_scanner.py <target> > /tmp/bb_wayback.json
python3 scripts/osint/shodan_intel.py <target> > /tmp/bb_shodan.json
```

## Phase 3: Active Scanning

```bash
# Subdomain enumeration
subfinder -d <target> -all | httpx -silent -title -tech-detect -status-code > alive.txt

# Directory fuzzing on interesting targets
ffuf -u https://<target>/FUZZ -w wordlist.txt -mc 200,301,302,403

# Nuclei vulnerability scanning
nuclei -l alive.txt -t cves/ -t exposures/ -t misconfiguration/ -severity critical,high

# Port scanning (if in scope)
nmap -sV -sC -p- --min-rate 1000 <target>
```

## Phase 4: Manual Testing

Focus on high-value vulnerability classes:

1. **Authentication**: bypass, weak reset, session issues
2. **Authorization**: IDOR, privilege escalation, BAC
3. **Injection**: SQLi, XSS, SSTI, command injection
4. **SSRF**: internal service access
5. **Business Logic**: payment bypass, rate limiting
6. **API**: broken auth, mass assignment, excessive data

## Phase 5: Vulnerability Assessment

For each finding:

1. Calculate CVSS v3.1 score
2. Map to CWE
3. Assess business impact
4. Build exploitation chain if possible
5. Create non-destructive PoC

## Phase 6: Report Writing

Use the Report Writer agent template:

```
TITLE: [Type] in [Component] allows [Impact]
SEVERITY: [CVSS Score]
STEPS TO REPRODUCE: [numbered, reproducible]
PROOF OF CONCEPT: [curl/code/screenshot]
IMPACT: [business impact]
REMEDIATION: [suggested fix]
```

## Phase 7: Submission

1. Verify report completeness
2. Submit on correct program/asset
3. Monitor triage status
4. Respond to questions within 24h
5. Track through to resolution and payout

## Rules

- [CRITICAL] Stay within authorized scope
- [CRITICAL] Non-destructive testing only
- [CRITICAL] No PII in reports
- Document everything for reproducibility
