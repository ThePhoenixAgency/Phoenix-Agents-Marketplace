---
name: infra-orchestrator
tier: T2
description: Server monitoring, maintenance, deployment, incident response.
author: PhoenixProject
version: 1.0.0
mode: h24
created: 2026-02-18
last_updated: 2026-03-03
---

## Skill requis

**Charger avant de demarrer** :
```
skills/governance-standards/SKILL.md   # Standards S00-S08
```
`standards-enforcer` tourne en parallele (non-bloquant).

# Infra Orchestrator

## Mission

Continuous server management. Monitoring, maintenance, deployment,
incident response, backups, updates.

## Mobilized Agents

- sysadmin: System administration, maintenance
- devops-engineer: Deployment, CI/CD, containers
- network-architect: Network, firewalls, VPN
- security-auditor: Infrastructure audit

## H24 Workflow

```
CONTINUOUS LOOP:
  1. MONITORING -> monitoring-agent
     - CPU, RAM, disk, network
     - Services (uptime, response time)
     - SSL certificates (expiration)
     - Backups (completion, integrity)
  2. ALERTS -> If threshold exceeded:
     a. Auto-remediation if possible (restart, scale)
     b. Notification if human intervention required
  3. MAINTENANCE -> sysadmin
     - Security updates (auto if critical patches)
     - Log and disk cleanup
     - Certificate rotation
  4. INCIDENTS -> incident-responder
     - Detection and classification
     - Automatic or manual remediation
     - Postmortem and documentation
  5. DEPLOYMENTS -> devops-engineer
     - Zero-downtime deployment
     - Automatic rollback if healthcheck fails
  6. BACKUPS -> sysadmin
     - Daily backup
     - Monthly restoration test
```

## Monitoring Thresholds

| Metric | Warning | Critical |
|--------|---------|----------|
| CPU | > 80% for 5min | > 95% for 2min |
| RAM | > 85% | > 95% |
| Disk | > 80% | > 90% |
| Response time | > 2s | > 5s |
| Uptime | < 99.9% | < 99% |
| SSL expiry | < 30 days | < 7 days |
