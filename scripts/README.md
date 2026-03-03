# Scripts
<!-- Created: 2026-02-18 | Last Updated: 2026-02-23 -->

Core infrastructure modules for the multi-agent system.

## Modules

| Module | Description |
|--------|-------------|
| `amp-protocol.js` | Agent Message Protocol - signed inter-agent communication |
| `agent-registry.js` | Agent discovery and management |
| `memory-system.js` | Persistent data storage between sessions |
| `proxy-router.js` | LLM routing by tier (local first) |
| `content-security.js` | Sensitive document check before commit |
| `graph-analysis.js` | Dependency analysis, cycle detection |
| `doc-generator.js` | Documentation generation from code |
| `pipeline-runner.js` | Sequential execution of validation steps |

## Usage

```javascript
const { AMPBus, AMPMessage } = require('./amp-protocol');
const { AgentRegistry } = require('./agent-registry');
const { MemorySystem } = require('./memory-system');
const { ProxyRouter, DEFAULT_PROVIDERS } = require('./proxy-router');
```

## Tests

```bash
npm test
```

Coverage > 96%.
