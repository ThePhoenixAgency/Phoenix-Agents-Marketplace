# Claude Marketplace
<!-- Created: 2026-02-18 | Last Updated: 2026-02-18 -->

Multi-agent orchestration system for Claude Code. A marketplace of specialized AI agents, skills, hooks, and commands that work together as a team.

## Overview

Claude Marketplace provides a structured framework where multiple specialized AI agents collaborate through a secure message protocol. Each agent handles a specific domain (development, security, design, DevOps, etc.) and communicates via the Agent Message Protocol (AMP).

## Architecture

```
claude-marketplace/
  agents/             # 22 specialized agents + 6 orchestrators
  skills/             # 57 skill modules
  commands/           # 40 shell commands (8 categories)
  hooks/              # 14 lifecycle hooks
  scripts/            # 8 core infrastructure modules
  tests/              # 11 test suites, 85 tests
  contexts/           # 3 work mode contexts
  rules/              # 5 language-specific rule sets
  schemas/            # 3 JSON validation schemas
  .github/workflows/  # 7 CI/CD pipelines
```

## Installation

```bash
git clone https://github.com/YOUR-USER/claude-marketplace.git
cd claude-marketplace
npm install
```

## Usage

### Run tests
```bash
npm test
```

### Validate project
```bash
bash commands/workflow/validate.sh
```

### Generate report
```bash
bash commands/workflow/report.sh
```

## Core Components

### Agent Message Protocol (AMP)
Signed, structured communication between agents. Supports direct messaging, pub/sub, and broadcast with RSA signature verification.

### Proxy Router
Routes LLM requests to the optimal provider based on tier requirements. Prefers local providers (Ollama, LM Studio) to minimize cost.

### Memory System
Persistent storage for session data, agent state, and learned patterns. Survives between sessions.

### Content Security
Prevents sensitive documents (threat models, audit reports, credentials) from being committed to public repositories.

## Agent Tiers

| Tier | Role | Resources |
|------|------|-----------|
| T1 | Execution | Local LLM |
| T2 | Analysis | Local + API |
| T3 | Strategy | Best available |

## Quality

- 85 tests, 11 suites
- 98% line coverage
- JSDoc on all public APIs
- Zero placeholders, zero TODOs

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

See [LICENSE](LICENSE).
