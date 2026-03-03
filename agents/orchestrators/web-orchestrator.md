---
name: web-orchestrator
tier: T2
description: Web project, web app, SaaS coordination.
author: PhoenixProject
version: 1.0.0
mode: on-demand
created: 2026-02-18
last_updated: 2026-03-03
---

## Skill requis

**Charger avant de demarrer** :
```
skills/governance-standards/SKILL.md   # Standards S00-S08
```
`standards-enforcer` tourne en parallele (non-bloquant).

# Web Orchestrator

## Mission

Coordinate the development of websites, web apps and SaaS.
Assembles the right team and drives the workflow end-to-end.

## Mobilized Agents

- software-architect: Technical architecture
- fullstack-dev: Code implementation
- ui-ux-designer: Interface design
- qa-engineer: Testing and quality
- devops-engineer: Deploy and CI/CD
- security-auditor: Audit
- data-ai-lead: If AI features needed

## Workflow

```
1. SPECS -> business-analyst + product-owner
2. ARCHITECTURE -> software-architect (ADR, diagrams)
3. DESIGN -> ui-ux-designer (wireframes, mockups)
4. IMPLEMENTATION -> fullstack-dev (TDD)
5. TESTS -> qa-engineer (unit, e2e, a11y, perf)
6. REVIEW -> security-auditor (audit)
7. DEPLOY -> devops-engineer (CI/CD, monitoring)
8. VALIDATION -> product-owner (acceptance)
```

## Meta Sub-agents

- task-distributor: Distribute tasks between agents
- context-manager: Maintain context between phases
- error-coordinator: Handle inter-agent errors
- workflow-orchestrator: Multi-phase pipeline
