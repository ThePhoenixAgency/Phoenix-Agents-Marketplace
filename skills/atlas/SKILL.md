---
name: atlas
description: Multi-agent coordination and task state management. Use when Codex needs to coordinate multiple agents (e.g., architect, implementer, reviewer) to solve a complex task.
metadata:
  short-description: Codex multi-agent task coordinator
author: PhoenixProject
version: 1.0.0
created: 2026-02-25
last_updated: 2026-02-25
---

# Atlas Skill (Codex Multi-Agent)

## PROTOCOLE D'EXÉCUTION OBLIGATOIRE
1.  **START** : Lire `docs/BACKLOG.md` et les Standards de Gouvernance.
2.  **PROCESS** : Appliquer les règles sans déviation.
3.  **END** : Mettre à jour `docs/BACKLOG.md` et `docs/CHANGELOG.md` avant tout commit.

Atlas is the internal multi-agent coordinator for Codex. It manages the hand-off between different specialized agents and ensures that the global project state is maintained throughout the development pipeline.

## Coordination Protocol

1.  **Task Distribution**: Atlas analyzes the incoming request and breaks it down into sub-tasks assigned to specific agents (e.g., `architect` for planning, `implementer` for coding).
2.  **State Management**: Atlas maintains the "Task Context" in `docs/BACKLOG.md` and ensures that mỗi agent reviews the context before starting.
3.  **Validation Loop**: After an agent completes a task, Atlas invokes the `qa-tester` or `security-reviewer` to validate the work before proceeding to the next phase.
4.  **Final Synthesis**: Atlas compiles the contributions of all agents into the final project output.

## Guidelines for Codex

- When Atlas is active, Codex should act as the "Project Manager."
- Use `docs/BACKLOG.md` as the source of truth for task progress.
- Ensure that the "Protocol d'Exécution Obligatoire" (START -> PROCESS -> END) is followed by all agents under Atlas supervision.

## Interaction with Other Skills

- **skill-creator**: Atlas can request the creation of new specialized skills if a task requires a new capability.
- **dev-pipeline**: Atlas manages the execution flow of the `dev-pipeline`.
- **web-research**: Atlas initiates research tasks to gather technical requirements.
