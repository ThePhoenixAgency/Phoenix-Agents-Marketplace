# Installation
<!-- Created: 2026-02-18 | Last Updated: 2026-02-18 -->

## Prerequisites

- Node.js >= 18
- npm >= 9
- Git

## Quick Start

```bash
git clone https://github.com/YOUR-USER/claude-marketplace.git
cd claude-marketplace
npm install
npm test
```

## Verify Installation

```bash
# Run all tests
npm test

# Check coverage
npx jest --coverage

# Validate project
bash commands/workflow/validate.sh

# Generate report
bash commands/workflow/report.sh
```

## Optional Dependencies

### Local LLM (recommended)
- [Ollama](https://ollama.com) - Local LLM server
- [LM Studio](https://lmstudio.ai) - GUI for local models

### Code Quality
```bash
npm install -g eslint prettier
```

### Security Scanning
```bash
npm install -g gitleaks
```

## Directory Structure

After installation, your project should contain:
- `node_modules/` - Dependencies (gitignored)
- `scripts/` - Core infrastructure
- `tests/` - Test suites
- `agents/` - Agent definitions
- `skills/` - Skill modules
- `commands/` - Shell commands
- `hooks/` - Lifecycle hooks
