---
name: workflow-triggers
description: Event-driven automation, webhooks, cron, file watchers, pipelines
author: PhoenixProject
version: 1.0.0
created: 2026-02-23
last_updated: 2026-02-23
---
# Workflow Triggers

## Types de triggers
| Type | Declencheur | Exemple |
|------|------------|---------|
| Webhook | HTTP event entrant | Push GitHub, paiement Stripe |
| Cron | Planification temporelle | Backup quotidien a 3h |
| File watcher | Changement de fichier | Nouveau fichier dans un dossier |
| Event bus | Message interne | Agent termine une tache |
| API poll | Verification periodique | Nouveau email, nouveau tweet |
| Manual | Declenchement humain | Bouton dans le dashboard |
| Conditional | Condition remplie | Score > seuil, budget depasse |

## Pipeline d'execution
1. Trigger detecte -> Event emis
2. Event filtre (conditions, debounce, dedup)
3. Actions executees (sequentielles ou paralleles)
4. Resultat enregistre (log, notification)
5. Erreur -> Retry avec backoff exponentiel
6. Dead letter queue pour les echecs definitifs

## Patterns
- Fan-out (un trigger -> plusieurs actions)
- Fan-in (plusieurs triggers -> une action)
- Chain (action 1 -> trigger action 2 -> trigger action 3)
- Circuit breaker (stop apres N echecs consecutifs)
- Rate limiting (max N executions par minute)
- Idempotency (meme trigger = meme resultat, pas de doublons)

## Monitoring
- Dashboard des executions (succes, echec, en cours)
- Alertes sur les echecs
- Metriques de latence (trigger -> execution)
- Historique complet avec replay possible
