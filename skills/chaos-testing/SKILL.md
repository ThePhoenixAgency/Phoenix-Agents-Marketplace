---
name: chaos-testing
description: Injection pannes, resilience, blast radius
---
# Chaos Testing
## Principes
1. Definir un etat stable (steady state)
2. Hypothetiser que l'etat sera maintenu sous perturbation
3. Introduire la perturbation (pannes, latence, perte reseau)
4. Observer et mesurer la deviation
5. Reduire le blast radius (commencer petit)
## Types de chaos
| Type | Simulation |
|------|-----------|
| Kill process | Arreter un service aleatoirement |
| Network latency | Ajouter 500ms+ de latence |
| Network partition | Couper la communication entre services |
| Disk full | Remplir le disque |
| CPU stress | Simuler charge CPU a 100% |
| DNS failure | Couper la resolution DNS |
## Checklist resilience
- [ ] Circuit breakers configures
- [ ] Retry avec backoff exponentiel
- [ ] Timeouts sur tous les appels externes
- [ ] Graceful degradation (mode degrade)
- [ ] Health checks fonctionnels
- [ ] Runbooks pour chaque scenario de panne
