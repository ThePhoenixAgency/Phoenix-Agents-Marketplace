# Orchestrateur: Security
# Created: 2026-02-18
# Tier: T3
# Mode: H24

## Mission

Securite interieure en continu. Surveillance reseau, cameras, alarmes,
detection d'intrusion (physique et numerique), alertes en temps reel.

## Agents mobilises

- security-auditor : Audit continu, detection menaces
- network-architect : Surveillance perimetre reseau
- sysadmin : Monitoring systemes, logs
- maker-specialist : Capteurs IoT, cameras, alarmes

## Workflow H24

```
BOUCLE CONTINUE :
  1. SURVEILLANCE -> monitoring-agent (logs, trafic, cameras)
  2. DETECTION -> security-auditor (anomalies, intrusions)
  3. ALERTE -> Si menace detectee :
     a. Classification (severite, type)
     b. Notification immediate
     c. Actions automatiques (blocage IP, isolation zone)
  4. ANALYSE -> security-auditor + network-architect
  5. REMEDIATION -> Actions correctives
  6. RAPPORT -> Rapport d'incident
  7. RETOUR -> Boucle continue
```

## Modes d'alerte

| Severite | Action |
|----------|--------|
| INFO | Log uniquement |
| WARNING | Notification push |
| CRITICAL | Notification + actions automatiques |
| EMERGENCY | Notification + actions + escalation humain |

## Sources surveillees

- Trafic reseau (firewall logs, IDS/IPS)
- Cameras de surveillance (motion detection)
- Capteurs IoT (portes, fenetres, mouvement)
- Logs systeme (auth failures, sudo, SSH)
- DNS queries (exfiltration detection)
