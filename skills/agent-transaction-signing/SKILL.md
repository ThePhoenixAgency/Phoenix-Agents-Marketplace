---
name: agent-transaction-signing
description: Signature cryptographique des transactions inter-agents, verification, non-repudiation
author: PhoenixProject
version: 1.0.0
created: 2026-02-23
last_updated: 2026-02-23
---
# Agent Transaction Signing

## Competences
- Signature RSA/ECDSA des messages inter-agents
- Verification de signature avant execution
- Non-repudiation (preuve d'origine)
- Chain of custody des decisions agents
- Audit trail signe et horodate
- Key rotation et revocation
- Certificate pinning pour agents

## Implementation
- Chaque agent a une paire de cles
- Tout message signe avec cle privee
- Recepteur verifie avec cle publique
- Timestamps anti-replay
- Nonce pour unicite
- Log immutable des transactions signees
