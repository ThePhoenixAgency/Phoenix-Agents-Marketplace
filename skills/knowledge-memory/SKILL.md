---
name: knowledge-memory
description: Memoire persistante des agents, knowledge graph, context management
author: PhoenixProject
version: 1.0.0
created: 2026-02-23
last_updated: 2026-02-23
---
# Knowledge & Memory

## Competences
- Memoire persistante entre sessions
- Knowledge graph (entites, relations, backlinks)
- Context accumulation (pas de cold start)
- Vault Markdown local (inspectable, editable)
- Embeddings et vector search (similarity)
- Delta indexing (indexer uniquement les changements)
- Memory layers (session, project, global)
- Conflict resolution (timestamp-based)

## Architecture
- Storage : fichiers Markdown locaux (plain text, pas de lock-in)
- Index : SQLite + embeddings vector store
- Graph : entites liees par backlinks
- API : CRUD sur memories, search semantique
- Sync : multi-machine via filesystem sync

## Use cases
- Agent se souvient des decisions passees
- Context automatique avant meeting
- Suivi des engagements et action items
- Code graph : navigation codebase intelligente
- Documentation auto-generee depuis le code
