<p align="center">
  <img src="assets/phoenix-logo.png" alt="Phoenix Agents Marketplace" width="200">
</p>

<h1 align="center">Phoenix Agents Marketplace</h1>

<p align="center">
  <strong>Autonomous multi-agent orchestration system for AI-powered development workflows.</strong>
</p>

<p align="center">
  <a href="https://github.com/ThePhoenixAgency/Phoenix-Agents-Marketplace"><img src="https://img.shields.io/badge/Compliancy-PhoenixProject-FF8C00?style=flat-square" alt="Compliancy"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue?style=flat-square" alt="License"></a>
</p>

---

## What is this?

Phoenix Agents Marketplace is a **production-ready collection of 40+ specialized AI agents** that work together to handle complex development workflows. Instead of relying on a single AI assistant, Phoenix splits work across dedicated agents -- each with its own expertise, tools, and tier of autonomy.

It works across **Claude Code, Antigravity, Codex CLI, Ollama, and LM Studio**. No vendor lock-in. No third-party dependencies.

### Why use it?

- **Structured workflows**: A 9-phase dev-pipeline from project classification to performance audit
- **Model-agnostic**: Route tasks to local LLMs (Ollama, LM Studio) or cloud APIs based on priority
- **Battle-tested**: 466 tests, 100% pass rate, >96% coverage

---

## Architecture

```
Phoenix-Agents-Marketplace/
  agents/               # 40 specialist agents + 7 orchestrators
  skills/               # Skill modules (dev-pipeline, security, web-research...)
  commands/             # Shell commands (arch, devops, git, osint, security...)
  hooks/                # Lifecycle hooks (PreToolUse, SessionStart...)
  scripts/              # Infrastructure (pipeline, audit, install...)
  standards/            # 7 governance standards (00-06)
  .claude-plugin/       # Claude Code plugin manifest
```

### 3-Layer Agent Architecture

Phoenix agents are organized in 3 tiers based on responsibility and resource access:

```
LAYER 1: ORCHESTRATORS (7)
  Coordinate complex workflows. Delegate tasks to specialists.
  Examples: web-orchestrator, security-orchestrator, bounty-orchestrator

LAYER 2: SPECIALISTS (40)
  Execute domain tasks. Each specialist has granular sub-agents.
  Examples: fullstack-dev, pentester, osint-analyst, qa-engineer

LAYER 3: SUB-AGENTS (n)
  Atomic capabilities within a specialist (defined per agent).
```

### Agent Tiers

| Tier | Role | Resources | Example |
|------|------|-----------|---------|
| **T3** | Strategy & Critical | Best available model | software-architect, security-auditor |
| **T2** | Analysis & Standard | Local + API | devops-engineer, data-analyst |
| **T1** | Execution & Support | Local LLM only | community-manager, sysadmin |

---

## Installation

### One-liner (recommended)

```bash
curl -sSL https://raw.githubusercontent.com/ThePhoenixAgency/Phoenix-Agents-Marketplace/main/install.sh | bash
```

### Manual

```bash
git clone https://github.com/ThePhoenixAgency/Phoenix-Agents-Marketplace.git
cd Phoenix-Agents-Marketplace
bash install.sh
```

### Codex CLI

```bash
bash scripts/install-skill.sh
```

See [INSTALL.md](INSTALL.md) for details.

---

## Dev Pipeline

The `dev-pipeline` skill orchestrates a **9-phase development workflow**. Each phase is handled by a dedicated agent:

| # | Phase | Agent | What it does |
|---|-------|-------|-------------|
| 1 | Classification | project-classifier | Analyzes the request, selects execution mode |
| 2 | Specification | spec-writer | Writes functional specs with acceptance criteria |
| 3 | Research | web-researcher | Validates technology stack, checks versions |
| 4 | Architecture | software-architect | Designs system architecture, writes ADRs |
| 5 | Implementation | fullstack-dev | TDD implementation (Red-Green-Refactor) |
| 6 | Review | security-reviewer | Code review and compliance check |
| 7 | Quality | qa-engineer | Unit tests, integration tests, >95% coverage |
| 8 | Accessibility | accessibility-auditor | WCAG 2.2 AAA compliance check |
| 9 | Performance | performance-auditor | Core Web Vitals (LCP, CLS, INP) optimization |

---

## Key Agents

### Orchestrators

| Orchestrator | Domain | Mode |
|---|---|---|
| web-orchestrator | Web projects, SaaS | On-demand |
| apple-orchestrator | iOS, macOS, SwiftUI | On-demand |
| security-orchestrator | Security operations | Always-on |
| bounty-orchestrator | Bug bounty programs | On-demand |
| infra-orchestrator | Infrastructure, DevOps | Always-on |
| home-orchestrator | Home automation | Always-on |
| community-orchestrator | Content, social | On-demand |



---

## Governance Standards

Phoenix enforces 7 non-negotiable standards across all agents:

| # | Standard | Rule |
|---|----------|------|
| 00 | NO_EMOJI | Zero emoji in code, commits, docs, config |
| 01 | GIT_VERSIONING | Conventional Commits, SemVer, Co-Authored-By |
| 02 | NAMING_PROTOCOL | Consistent naming across all components |
| 03 | ANTI_RUSH_POLICY | No placeholders, no TODOs, no fake code |
| 04 | AGNOSTICISM | Model-agnostic design, no vendor lock-in |

---

## Usage

```bash
npm test                             # Run tests
bash commands/workflow/validate.sh   # Validate project structure
bash commands/workflow/report.sh     # Generate project report
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT - See [LICENSE](LICENSE).

---

<p align="center">
  <sub>Built by <a href="https://github.com/ThePhoenixAgency">ThePhoenixAgency</a></sub>
</p>
