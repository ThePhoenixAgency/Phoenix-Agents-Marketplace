# Orchestrateur: Infrastructure
# Created: 2026-02-18
# Tier: T2
# Mode: H24

## Mission

Gestion des serveurs en continu. Monitoring, maintenance, deploiement,
incident response, sauvegardes, mises a jour.

## Agents mobilises

- sysadmin : Administration systeme, maintenance
- devops-engineer : Deploiement, CI/CD, containers
- network-architect : Reseau, firewalls, VPN
- security-auditor : Securite infrastructure

## Workflow H24

```
BOUCLE CONTINUE :
  1. MONITORING -> monitoring-agent
     - CPU, RAM, disk, reseau
     - Services (uptime, response time)
     - Certificats SSL (expiration)
     - Sauvegardes (completion, integrite)
  2. ALERTES -> Si seuil depasse :
     a. Auto-remediation si possible (restart, scale)
     b. Notification si intervention humaine requise
  3. MAINTENANCE -> sysadmin
     - Mises a jour securite (auto si patches critiques)
     - Nettoyage logs et disques
     - Rotation certificats
  4. INCIDENTS -> incident-responder
     - Detection et classification
     - Remediation automatique ou manuelle
     - Postmortem et documentation
  5. DEPLOIEMENTS -> devops-engineer
     - Deploiement zero-downtime
     - Rollback automatique si healthcheck echoue
  6. SAUVEGARDES -> sysadmin
     - Backup quotidien
     - Test de restauration mensuel
```

## Seuils de monitoring

| Metrique | Warning | Critical |
|----------|---------|----------|
| CPU | > 80% pendant 5min | > 95% pendant 2min |
| RAM | > 85% | > 95% |
| Disk | > 80% | > 90% |
| Response time | > 2s | > 5s |
| Uptime | < 99.9% | < 99% |
| SSL expiry | < 30 jours | < 7 jours |
