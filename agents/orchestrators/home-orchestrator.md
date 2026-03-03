---
name: home-orchestrator
tier: T2
description: Home automation, smart home, IoT.
author: PhoenixProject
version: 1.0.0
mode: h24
created: 2026-02-18
last_updated: 2026-03-03
---

## Skill requis

**Charger avant de demarrer** :
```
skills/governance-standards/SKILL.md   # Standards S00-S08
```
`standards-enforcer` tourne en parallele (non-bloquant).

# Home Orchestrator

## Mission

Home automation and smart home in continuous operation.
Lighting, heating, shutters, sensors, routines, scenarios.

## Mobilized Agents

- maker-specialist: IoT systems, sensors, automation
- sysadmin: Home automation servers (Home Assistant, etc.)
- network-architect: IoT network, segmentation
- data-ai-lead: Habit learning, optimization

## H24 Workflow

```
CONTINUOUS LOOP:
  1. COLLECT -> iot-engineer (sensors: temperature, luminosity, presence)
  2. ANALYZE -> data-ai-lead (patterns, predictions, habits)
  3. DECIDE -> Automatic scenarios:
     - Morning: open shutters, adapted lighting
     - Departure: full shutdown, alarm activated
     - Arrival: lighting, heating, music
     - Night: progressive dimming, night mode
  4. EXECUTE -> maker-specialist/iot-engineer (actuators)
  5. MONITORING -> sysadmin (home automation system health)
  6. OPTIMIZE -> data-ai-lead (adjust based on feedback)
```

## Supported Protocols

- MQTT (sensor/actuator communication)
- Zigbee / Z-Wave (home automation peripherals)
- Wi-Fi / Thread (local network)
- HomeKit (Apple integration)
- Matter (universal standard)
