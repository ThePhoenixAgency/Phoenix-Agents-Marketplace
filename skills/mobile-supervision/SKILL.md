---
name: mobile-supervision
description: Supervision et controle d'agents depuis mobile (iOS/Android)
author: PhoenixProject
version: 1.0.0
created: 2026-02-23
last_updated: 2026-02-23
---
# Mobile Supervision

## Competences
- Dashboard mobile temps reel (SwiftUI, React Native)
- Push notifications pour alertes agents
- Remote start/stop/restart d'agents
- Logs en streaming sur mobile
- Metriques et graphiques embarques
- Authentification biometrique (Face ID, Touch ID)
- Offline mode avec sync au retour

## Architecture
- WebSocket pour temps reel
- REST API pour commandes
- Token-based auth (JWT + refresh)
- Rate limiting sur les commandes critiques
