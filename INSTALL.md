# Installation
<!-- Created: 2026-02-18 | Last Updated: 2026-02-23 -->

## Quick Start / Demarrage Rapide

```bash
curl -sSL https://raw.githubusercontent.com/ThePhoenixAgency/Phoenix-Agents-Marketplace/main/install.sh | bash
```

This will:
- Clone the repository
- Install the dev-pipeline plugin into Claude Code
- Install the security-audit plugin into Claude Code
- Display agent/skill/command counts

## Manual Installation

```bash
git clone https://github.com/ThePhoenixAgency/Phoenix-Agents-Marketplace.git
cd Phoenix-Agents-Marketplace
bash install.sh
```

## Codex CLI

```bash
bash scripts/install-skill.sh
```

## Uninstall

```bash
bash scripts/uninstall-skill.sh
```

## Verify Installation

```bash
npm test                             # Run tests
bash commands/workflow/validate.sh   # Validate project
bash commands/workflow/report.sh     # Generate report
```

## Optional Dependencies

### Local LLM (recommended)
- [Ollama](https://ollama.com) - Local LLM server
- [LM Studio](https://lmstudio.ai) - GUI for local models

## Directory Structure

After installation, your project should contain:
- `agents/` - Agent definitions
- `skills/` - Skill modules
- `commands/` - Shell commands
- `hooks/` - Lifecycle hooks
- `scripts/` - Core infrastructure
- `standards/` - Governance standards
