# Tests
<!-- Created: 2026-02-18 | Last Updated: 2026-02-18 -->

Test suites pour les scripts core et les hooks.

## Runner

```bash
npm test                     # All tests + coverage
npx jest --watch             # Watch mode
npx jest tests/hooks.test.js # Single suite
```

## Suites

| Suite | Module | Tests |
|-------|--------|-------|
| `amp-protocol.test.js` | AMP Protocol | Messages, IDs, serialisation, pub/sub |
| `amp-signing.test.js` | AMP Signing | RSA sign, verify, tamper, wrong key |
| `agent-registry.test.js` | Agent Registry | Discovery, metadata, activation |
| `memory-system.test.js` | Memory System | Save/load, list, delete, sessions |
| `proxy-router.test.js` | Proxy Router | Routing, tiers, local preference |
| `content-security.test.js` | Content Security | Sensitive detection, scan |
| `graph-analysis.test.js` | Graph Analysis | Cycles, coupling, imports |
| `doc-generator.test.js` | Doc Generator | Structure, coverage |
| `pipeline-runner.test.js` | Pipeline Runner | Pass/fail, stopOnFailure |
| `hooks.test.js` | Hooks | 4 hooks principaux |
| `session-start.test.js` | Session Start | 8 package managers |

## Coverage

Lines: 98%+ (seuil: 90%)
