---
name: agent-identity-mesh
description: Identite cryptographique des agents, DID, mesh reseau, coordination
author: PhoenixProject
version: 1.0.0
created: 2026-02-23
last_updated: 2026-02-23
---
# Agent Identity & Mesh

## Competences
- Decentralized Identifiers (DID) pour chaque agent
- Verifiable Credentials pour preuves d'execution
- Peer mesh network (multi-machine, multi-OS)
- Agent discovery et registration
- Delegation chains (qui a autorise quoi)
- Audit trail cryptographique immutable
- Agent-to-agent messaging signe
- Priority levels et message types
- Cross-machine team coordination

## Architecture
- Chaque agent = DID unique + paire de cles
- Mesh peer-to-peer (pas de serveur central)
- Messages signes avec verification
- Persistent memory partagee (conflits resolus par timestamp)
- Dashboard unifie multi-machine

## Coordination
- War rooms (split-pane multi-agents)
- Kanban board pour taches agents
- Meeting mode (agents discutent un sujet)
- Background agents (taches recurentes automatiques)
