# Orchestrateur: Home
# Created: 2026-02-18
# Tier: T2
# Mode: H24

## Mission

Domotique et automatisation maison en continu.
Gestion eclairage, chauffage, volets, capteurs, routines, scenarios.

## Agents mobilises

- maker-specialist : Systemes IoT, capteurs, automatisation
- sysadmin : Serveurs domotique (Home Assistant, etc.)
- network-architect : Reseau IoT, segmentation
- data-ai-lead : Apprentissage habitudes, optimisation

## Workflow H24

```
BOUCLE CONTINUE :
  1. COLLECTE -> iot-engineer (capteurs : temperature, luminosite, presence)
  2. ANALYSE -> data-ai-lead (patterns, predictions, habitudes)
  3. DECISION -> Scenarios automatiques :
     - Matin : ouverture volets, eclairage adapte
     - Depart : extinction generale, alarme activee
     - Arrivee : eclairage, chauffage, musique
     - Nuit : extinction progressive, mode nuit
  4. EXECUTION -> maker-specialist/iot-engineer (actionneurs)
  5. MONITORING -> sysadmin (sante systeme domotique)
  6. OPTIMISATION -> data-ai-lead (ajuster selon retours)
```

## Protocoles supportes

- MQTT (communication capteurs/actionneurs)
- Zigbee / Z-Wave (peripheriques domotique)
- Wi-Fi / Thread (reseau local)
- HomeKit (integration Apple)
- Matter (standard universel)
