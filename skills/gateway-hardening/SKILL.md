---
name: gateway-hardening
description: Hardening des gateways reseau, ports, WebSocket, mDNS, isolation
author: PhoenixProject
version: 1.0.0
created: 2026-02-23
last_updated: 2026-02-23
---
# Gateway Hardening

## Competences
- Bind sur 127.0.0.1 (jamais 0.0.0.0)
- Auth forte obligatoire sur tous les ports
- Desactivation mDNS/Bonjour en production
- Ports non-standard + firewall
- Docker network isolation
- WebSocket auth (token par frame)
- Rate limiting par IP et par session
- TLS termination obligatoire

## Checks
- Scanner les ports ouverts (nmap, ss)
- Verifier absence d'auth bypass
- Tester les WebSocket sans credentials
- Verifier que Shodan ne voit rien
- Audit des permissions Docker (no privileged, no root)

## Automatisation
- Script d'audit pre-deploy
- CI gate bloquant si port expose sans auth
- Monitoring continu des ports ouverts
