# Scripts
<!-- Created: 2026-02-18 | Last Updated: 2026-02-18 -->

Core infrastructure modules for the multi-agent system.

## Modules

| Module | Description |
|--------|-------------|
| `amp-protocol.js` | Agent Message Protocol - communication inter-agents signee |
| `agent-registry.js` | Decouverte et gestion des agents disponibles |
| `memory-system.js` | Persistance de donnees entre sessions |
| `proxy-router.js` | Routage LLM par tier (local first) |
| `content-security.js` | Verification documents sensibles avant commit |
| `graph-analysis.js` | Analyse des dependances, detection de cycles |
| `doc-generator.js` | Generation de documentation a partir du code |
| `pipeline-runner.js` | Execution sequentielle des steps de validation |

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
