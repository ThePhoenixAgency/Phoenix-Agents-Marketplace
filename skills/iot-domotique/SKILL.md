---
name: iot-domotique
description: MQTT, edge computing, digital twins, capteurs, protocoles
---
# IoT & Domotique
## MQTT
```python
import paho.mqtt.client as mqtt
client = mqtt.Client()
client.connect("localhost", 1883, 60)
# Publier
client.publish("home/salon/temperature", "22.5")
# Souscrire
def on_message(client, userdata, msg):
    print(f"{msg.topic}: {msg.payload.decode()}")
client.subscribe("home/#")
client.on_message = on_message
client.loop_forever()
```
## Protocoles
| Protocole | Usage |
|-----------|-------|
| MQTT | Communication capteurs (leger, pub/sub) |
| Zigbee | Peripheriques domotiques (faible conso) |
| Z-Wave | Domotique (mesh, fiable) |
| Thread | IoT moderne (IP-based, mesh) |
| Matter | Standard universel (interoperabilite) |
| HomeKit | Ecosysteme Apple |
## Architecture type
```
Capteurs -> MQTT Broker -> Home Assistant -> Automations
                        -> Dashboard (Grafana)
                        -> Alertes (Notifications push)
```
## Digital Twin
Representation virtuelle d'un objet physique.
Synchronisation en temps reel via MQTT/WebSocket.
Simulation de scenarios avant deploiement physique.
## Securite IoT
- Segmentation reseau (VLAN dedie IoT)
- Chiffrement TLS pour MQTT
- Firmware signe
- Mises a jour OTA securisees
- Pas de mots de passe par defaut
