# Agents
<!-- Created: 2026-02-18 | Last Updated: 2026-02-23 -->

Multi-agent system organized in 3 layers.

## 3-Layer Architecture

```
LAYER 1: ORCHESTRATORS (coordination)
  Drive workflows, delegate to specialists.
  7 orchestrators: on-demand + always-on.

LAYER 2: SPECIALIST AGENTS (execution)
  Execute domain tasks. Each has its own sub-agents.
  40 specialist agents across tiers T1-T3.

LAYER 3: SUB-AGENTS (granularity)
  Atomic capabilities within a specialist.
  Defined in each agent file (Sub-agents section).
```

## Orchestrators (Layer 1)

| Orchestrator | Mode | Mission |
|---|---|---|
| web-orchestrator | On-demand | Web projects, SaaS |
| apple-orchestrator | On-demand | iOS/macOS |
| community-orchestrator | On-demand | Content, social |
| security-orchestrator | Always-on | Continuous monitoring |
| home-orchestrator | Always-on | Home automation |
| infra-orchestrator | Always-on | Servers, monitoring |
| bounty-orchestrator | On-demand | Bug bounty pipeline |

## Specialist Agents (Layer 2)

### Tier T3 (critical)

| Agent | Description |
|---|---|
| software-architect | Architecture, technologies, ADR |
| fullstack-dev | TDD code, all languages |
| security-auditor | Audit, pentest, Zero Trust |
| data-ai-lead | ML, data engineering, LLM |
| pentester | Active intrusion testing |
| security-researcher | Vulnerability research, CVE |
| bounty-hunter | Bug bounty, PoC, impact |
| tech-lead | Technical supervision |

### Tier T2 (standard)

| Agent | Description |
|---|---|
| project-manager | Planning, coordination, agile |
| product-owner | Product vision, backlog |
| business-analyst | Business requirements, specs |
| business-manager | Sales, marketing, pricing |
| devops-engineer | CI/CD, containers, cloud |
| network-architect | Network, firewall |
| ui-ux-designer | Design, prototyping |
| data-analyst | BI, dashboards |
| qa-engineer | Testing, quality |
| maker-specialist | Electronics, IoT |
| legal-advisor | Licenses, contracts |
| finance-controller | Budget, pricing |
| compliance-officer | GDPR, regulations |
| osint-analyst | Open-source intelligence |
| google-dorker | Advanced dorking |
| vulnerability-assessor | CVSS, classification |
| report-writer | Structured reports |
| platform-manager | Bounty platforms |
| project-classifier | Workflow routing |
| accessibility-auditor | WCAG, a11y |
| performance-auditor | Core Web Vitals, Lighthouse |
| web-researcher | Tech watch, benchmarks |
| spec-writer | Functional specifications |

### Tier T1 (support)

| Agent | Description |
|---|---|
| community-manager | Content, social media |
| support-agent | Support, tickets |
| executive-assistant | Calendar, emails |
| sysadmin | System administration |
| bounty-finance | Bounty payment tracking |

## File Structure

```
agents/
  agent-name.md              # Simple agent (same definition everywhere)
  agent-name/                # Agent with platform overrides
    agent.md                   Universal base
    codex.md                   Codex override
    antigravity.md             Antigravity override (if needed)
  orchestrators/             # Orchestrators (Layer 1)
    web-orchestrator.md
    apple-orchestrator.md
    ...
```

## Standard Frontmatter

```yaml
---
name: agent-name
tier: T1|T2|T3
description: Short description.
author: PhoenixProject
version: 1.0.0
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
---
```
