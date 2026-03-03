---
name: security-orchestrator
tier: T3
description: Continuous monitoring, detection, real-time alerts.
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

# Security Orchestrator

## Mission

Continuous internal monitoring. Network surveillance, cameras, alarms,
intrusion detection (physical and digital), real-time alerts.

## Mobilized Agents

- security-auditor: Continuous audit, threat detection
- network-architect: Network perimeter surveillance
- sysadmin: System monitoring, logs
- maker-specialist: IoT sensors, cameras, alarms

## H24 Workflow

```
CONTINUOUS LOOP:
  1. SURVEILLANCE -> monitoring-agent (logs, traffic, cameras)
  2. DETECTION -> security-auditor (anomalies, intrusions)
  3. ALERT -> If threat detected:
     a. Classification (severity, type)
     b. Immediate notification
     c. Automatic actions (IP blocking, zone isolation)
  4. ANALYSIS -> security-auditor + network-architect
  5. REMEDIATION -> Corrective actions
  6. REPORT -> Incident report
  7. RETURN -> Continuous loop
```

## Alert Modes

| Severity | Action |
|----------|--------|
| INFO | Log only |
| WARNING | Push notification |
| CRITICAL | Notification + automatic actions |
| EMERGENCY | Notification + actions + human escalation |

## Monitored Sources

- Network traffic (firewall logs, IDS/IPS)
- Surveillance cameras (motion detection)
- IoT sensors (doors, windows, motion)
- System logs (auth failures, sudo, SSH)
- DNS queries (exfiltration detection)
