---
name: logic-purification
description: Protocol for washing and sanitizing logic flows before execution.
author: PhoenixProject
version: 1.0.0
created: 2026-02-25
last_updated: 2026-02-25
---

## Logic Washing Cycle
Every code fragment or dynamic instruction must pass through the mandatory washing cycle:
1. **Neutralization**: Execute `node scripts/logic-cleaner.js <file>` to remove comments, non-ASCII characters, and normalize whitespace.
2. **Scrutiny**: Validate via `node scripts/module-validator.js` on the washed fragment.
3. **Sandbox**: Mandatory execution via `node scripts/purity-jail.js "<command>"` to limit environmental impact.

## Selection Alignment (Decision Guidance)
- Prioritize local models (Ollama/LM Studio) audited in `daily-health.js`.
- Avoid models with high-entropy names or non-aligned sources.
- Use `shadow-scrutiny.js` to independently validate critical decisions.

## Segment Maintenance
- Perform a `stress-alignment.js` cycle after every major model change to stabilize memory segments.
- Verify `NODE_ID` to ensure execution on authorized hardware (Mac Ultra / Mini-PC).
