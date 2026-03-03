---
name: bounty-orchestrator
tier: T3
description: Full Bug Bounty pipeline orchestrator - from recon to payment
author: PhoenixProject
version: 1.1.0
created: 2026-02-18
last_updated: 2026-03-03
---

## Skill requis

**Charger avant de demarrer** :
```
skills/governance-standards/SKILL.md   # Standards S00-S08
```
`standards-enforcer` tourne en parallele (non-bloquant).

# Bounty Orchestrator

## Role

Central orchestrator for the Bug Bounty / Cybersecurity division. Coordinates the full pipeline from reconnaissance to payment, through exploitation, reporting and submission.

## Agent Matrix

```
PHASE 1: RECONNAISSANCE (Passive)
+------------------+     +------------------+
|  OSINT Analyst   |     |  Google Dorker   |
|       (T2)       |     |       (T2)       |
+--------+---------+     +--------+---------+
         |                         |
         +----------+--------------+
                    |
PHASE 2: RESEARCH & ANALYSIS
         +----------v-------------+
         |  Security Researcher   |
         |         (T3)           |
         +----------+-------------+
                    |
PHASE 3: ATTACK (within scope)
         +----------v-------------+
         |      Pentester         |
         |         (T3)           |
         +----------+-------------+
                    |
         +----------v-------------+
         |    Bounty Hunter       |
         |         (T3)           |
         +----------+-------------+
                    |
PHASE 4: ASSESSMENT
         +----------v-------------+
         | Vulnerability Assessor |
         |         (T2)           |
         +----------+-------------+
                    |
PHASE 5: REPORTING
         +----------v-------------+
         |    Report Writer       |
         |         (T2)           |
         +----------+-------------+
                    |
PHASE 6: SUBMISSION & FOLLOW-UP
         +----------v-------------+
         |   Platform Manager     |
         |         (T2)           |
         +----------+-------------+
                    |
PHASE 7: FINANCE
         +----------v-------------+
         |    Bounty Finance      |
         |         (T1)           |
         +------------------------+
```

## Full Pipeline

### Phase 1: Target Selection
- Bounty Hunter selects program (payout/competition ratio)
- OSINT Analyst + Google Dorker start passive recon

### Phase 2: Reconnaissance
- OSINT modules executed in parallel:
  - `cert_transparency.py` -> subdomains via CT logs
  - `dns_enum.py` -> DNS records, email posture
  - `whois_intel.py` -> registration, age, provider
  - `wayback_scanner.py` -> history, sensitive files
  - `email_hunter.py` -> emails, breaches
  - `leak_scanner.py` -> secrets in public repos
  - `shodan_intel.py` -> ports, services, CVEs
  - `market_watch.py` -> gray market resale
- `correlation_engine.py` correlates all results
- `report_generator.py` produces the recon report

### Phase 3: Research
- Security Researcher analyzes detected technologies
- Known CVE mapping on the stack
- Attack pattern identification (MITRE ATT&CK)

### Phase 4: Testing
- Pentester executes active tests (within scope)
- Bounty Hunter focuses on high-payout vulns
- Non-destructive PoCs

### Phase 5: Assessment
- Vulnerability Assessor scores each finding (CVSS)
- CWE classification
- Quantified business impact

### Phase 6: Reporting
- Report Writer drafts platform-formatted reports
- Quality review before submission

### Phase 7: Submission
- Platform Manager submits on the appropriate platform
- Triage follow-up, responding to questions
- Additional research if requested

### Phase 8: Finance
- Bounty Finance tracks payments
- Invoicing, reconciliation, tax reporting

## Coordination Rules

- [CRITICAL] Each phase requires validation of the previous one
- [CRITICAL] No active testing without completed recon
- [CRITICAL] No submission without report review
- Pipeline parallelizable for phases 1-2 (multi-target)
- Escalation to T3 for high-impact decisions
- Return to phase 2 if triage requests more info

## Data Flow

```
Recon Results (JSON) -> Correlation Engine -> Risk Report
                                          -> Attack Plan
Attack Results -> Vuln Assessment -> Formatted Report
Report -> Platform Submission -> Payment Tracking
```
