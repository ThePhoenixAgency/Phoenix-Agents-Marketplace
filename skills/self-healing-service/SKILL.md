---
name: self-healing-service
description: Surveillance automatique des services Docker et auto-remediation. Detecte les services down, les ressources critiques, et applique des corrections sans intervention humaine pour les cas standard. Previent le proprietaire pour les cas complexes. Utilisable sur tout serveur Linux avec Docker.
---

# SKILL : self-healing-service
# Created: 2026-03-02
# Last Updated: 2026-03-02
# Concu pour : ReadyToClaw-Site (web + tunnel), Docker-OpenClaw-MiniPc

## PERIMETRE

Ce skill surveille et repare automatiquement :
- Services Docker down -> restart automatique
- Espace disque critique (> 85%) -> nettoyage cache/logs
- Port inaccessible -> diagnostic + restart service
- Tunnel Cloudflare coupe -> restart + verification

Il NOTIFIE sans agir pour :
- Erreurs de certificat SSL
- Changements de configuration inattendus
- Echecs repetes (> 3 fois) -> escalation humaine obligatoire

## CHECKS DISPONIBLES

### check-services
```bash
# Verifier l'etat de tous les containers
docker ps --format "{{.Names}}\t{{.Status}}" | grep -v "Up"
```
Si container down -> restart automatique :
```bash
docker restart [nom_container]
sleep 5
docker inspect [nom_container] --format "{{.State.Status}}"
```

### check-disk
```bash
df -h / | awk 'NR==2 {print $5}' | sed 's/%//'
```
Si > 85% -> nettoyer :
```bash
docker system prune -f --volumes 2>/dev/null
docker image prune -f 2>/dev/null
```

### check-port
```bash
# Verifier qu'un port repond
nc -z localhost [PORT] 2>/dev/null && echo "open" || echo "closed"
```
Si closed -> identifier quel service doit ecouter + restart

### check-tunnel
```bash
# Verifier le tunnel Cloudflare (ReadyToClaw specifique)
curl -s --max-time 5 https://home.readytoclaw.io > /dev/null
echo $?
```
Si echec -> `docker restart readytoclaw-tunnel`

## PHASES D'EXECUTION

### Phase 1 - Health scan complet
Executer tous les checks ci-dessus et produire un rapport :
```
HEALTH REPORT [YYYY-MM-DD HH:MM]
Services  : [OK/WARN liste des containers]
Disque    : [X% utilise]
Ports     : [liste port:status]
Tunnel    : [OK/FAIL]
```

### Phase 2 - Triage
- OK   : aucune action
- WARN : remediation automatique (restart/nettoyage)
- FAIL repete (> 3x) : [STOP] notifier le proprietaire, ne pas agir

### Phase 3 - Remediation automatique (WARN uniquement)
Appliquer la correction standard, verifier le resultat.
Logger dans `~/.agents/ARCHIVE.md` section "Incidents resolus".

### Phase 4 - Rapport post-action
```
REMEDIATION [YYYY-MM-DD HH:MM]
Probleme : [description]
Action   : [commande executee]
Resultat : [OK/FAIL]
Duree    : [temps de resolution]
```

## INTEGRATION PIPELINE

Ce skill incremente `70_post-deploy-verify.sh` :
- Apres chaque deploy, lancer le health scan
- Si health scan echoue, bloquer le pipeline (exit 1)
- Path du script de reference : ~/.agents/hooks/audit-security.sh (meme pattern)

## CRON RECOMMANDE

Ajouter dans crontab pour surveillance continue :
```
*/15 * * * * goose run "Executer le skill self-healing-service check-services" 2>/dev/null
0 */6 * * * goose run "Executer le skill self-healing-service check-disk" 2>/dev/null
```
