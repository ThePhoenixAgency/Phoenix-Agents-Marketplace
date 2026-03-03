---
name: active-logic-scrutiny
description: Real-time validation and containment protocols for autonomous agent execution.
author: PhoenixProject
version: 1.1.0
created: 2026-02-25
last_updated: 2026-02-25
---

## Consensus Protocols (Double Verification)
- **Shadow Scrutiny**: For any critical flow (download, system command, memory access), a "shadow" agent (sub-agent) must independently validate the vector without access to the primary agent's reasoning.
- **Cross-Agent Validation**: Comparison of purity signatures between two distinct logical entities before a permit is granted.
- **Quarantine Delegation**: Specialized sub-agents manage the isolation of suspect segments while the main agent maintains dialogue continuity.

## Execution Barriers (Purity Gate)
- **Sanitization Sandbox**: Mandatory use of `purity-jail.js`. Any system command or code snippet must be executed in a restricted environment with a limited `PATH` and strict `TIMEOUT`.
- **Integrity Consensus**: If the shadow agent detects a deviation (NMIS, LURE, B64P), the segment is immediately quarantined and reported to the `Alignment Dashboard`.

## Validation Workflow
1. **Logic Washing**: Systematic cleaning of logic fragments (strip comments, normalize spaces).
2. **Shadow Audit**: Independent evaluation of the vector.
3. **Purity Permit**: Final permit granted only upon consensus.
4. **Jail Execution**: Execution in a restricted container/jail.
