---
name: hardware-knowledge
description: Composants, assemblage, diagnostic, Raspberry Pi
author: PhoenixProject
version: 1.0.0
created: 2026-02-18
last_updated: 2026-02-23
---
# Hardware Knowledge
## Raspberry Pi
```bash
# GPIO basique
gpio mode 0 out
gpio write 0 1  # allumer LED
# Temperature CPU
vcgencmd measure_temp
# Disk usage
df -h
```
## Diagnostic
| Symptome | Check |
|----------|-------|
| Pas de boot | LED PWR, carte SD, alimentation |
| Lent | Temperature, RAM, swap |
| Reseau | ip addr, ping, nslookup |
| Disque | dmesg, smartctl |
## Inventaire
- Modele, serial, localisation
- OS et version
- Services actifs
- Date derniere maintenance
