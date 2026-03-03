---
name: electronics-firmware
description: Arduino, ESP32, Raspberry Pi, capteurs, radio, mesh, acquisition, PCB
author: PhoenixProject
version: 1.1.0
created: 2026-02-18
last_updated: 2026-02-23
---
# Electronics & Firmware

## Arduino
```cpp
const int LED_PIN = 13;
const int SENSOR_PIN = A0;
void setup() {
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(9600);
}
void loop() {
  int sensorValue = analogRead(SENSOR_PIN);
  if (sensorValue > 512) {
    digitalWrite(LED_PIN, HIGH);
  } else {
    digitalWrite(LED_PIN, LOW);
  }
  Serial.println(sensorValue);
  delay(100);
}
```

## ESP32
- WiFi (station, AP, mesh) + Bluetooth Classic + BLE
- Deep sleep pour economie d'energie (batteries, panneaux solaires)
- OTA updates (mise a jour firmware a distance via WiFi)
- FreeRTOS pour multitache
- MicroPython / CircuitPython pour prototypage rapide
- ESP-NOW pour communication peer-to-peer sans WiFi
- Dual core (tasks paralleles : acquisition + communication)
- ADC, DAC, PWM, touch pins, hall effect sensor

## Raspberry Pi
- GPIO, I2C, SPI, UART pour interfacage capteurs
- Camera module (photo, video, timelapse, streaming)
- Audio HAT (acquisition son, micro array, speaker)
- Serveur local (Node-RED, MQTT broker, web server)
- Edge AI (TensorFlow Lite, inference embarquee)
- Cluster (Kubernetes sur Pi, calcul distribue)

## Capteurs & Acquisition
| Type | Exemples | Protocole |
|------|----------|-----------|
| Temperature | DHT22, DS18B20, BME280, thermocouple | OneWire, I2C |
| Pression | BMP280, BME680, MPX5700 | I2C, analogique |
| Humidite | DHT22, SHT31, capacitif sol | I2C, analogique |
| Mouvement | PIR HC-SR501, radar RCWL-0516 | digital |
| Distance | HC-SR04 (ultrason), VL53L0X (laser) | digital, I2C |
| Lumiere | LDR, BH1750, TSL2591 | analogique, I2C |
| Son | MAX4466, INMP441 (I2S), microphones MEMS | analogique, I2S |
| Video | OV2640, RPi Camera, USB webcam | CSI, USB |
| Gaz | MQ-2 (fumee), MQ-7 (CO), CCS811 (CO2/VOC) | analogique, I2C |
| Accelerometre | MPU6050, ADXL345, LSM6DS3 | I2C, SPI |
| GPS | NEO-6M, NEO-M8N, BN-880 | UART |
| Courant/Tension | INA219, ACS712, PZEM-004T | I2C, UART |

## Station Meteo
- Capteurs : temperature, humidite, pression, vent (anemometre), pluie (pluviometre)
- UV index, luminosite, qualite de l'air
- Transmission : WiFi, LoRa, radio 433MHz
- Dashboard local (ecran e-ink, web) + cloud (upload periodique)
- Historique et graphiques (InfluxDB + Grafana)
- Alertes (gel, tempete, qualite air)

## Radio & Communication sans fil
| Technologie | Portee | Debit | Usage |
|-------------|--------|-------|-------|
| WiFi 2.4/5GHz | 50-100m | Haut | Internet, streaming |
| BLE (Bluetooth Low Energy) | 10-30m | Bas | Wearables, beacons |
| LoRa | 2-15km | Tres bas | IoT longue portee |
| 433/868/915 MHz | 100m-1km | Bas | Telecommandes, capteurs |
| ZigBee | 10-100m | Bas | Mesh domotique |
| Thread/Matter | 10-100m | Moyen | Domotique IP-native |
| NFC/RFID | 1-10cm | Bas | Identification, paiement |
| ESP-NOW | 200m | Moyen | Peer-to-peer rapide |
| nRF24L01 | 100m | Moyen | Communication inter-MCU |

## Mesh Networking
- ESP-MESH (WiFi mesh sur ESP32)
- LoRa Mesh (Meshtastic)
- BLE Mesh
- Auto-healing, auto-routing
- Gateway mesh -> Internet

## EMI & Compatibilite electromagnetique
- Blindage (boitiers metalliques, plans de masse)
- Filtrage (ferrites, condensateurs de decouplage)
- Layout PCB anti-bruit (separation analogique/numerique)
- Tests EMI/EMC (antenne proche, analyseur de spectre)
- Conformite CE / FCC

## Protocoles filaires
| Protocole | Usage |
|-----------|-------|
| I2C | Capteurs, ecrans (2 fils, multi-device) |
| SPI | Memoire, ADC, ecrans rapides (4 fils) |
| UART | Communication serie (2 fils, point-a-point) |
| CAN | Automobile, industriel (robuste, multi-device) |
| OneWire | Capteurs temperature DS18B20 (1 fil) |
| I2S | Audio numerique (microphones, DAC) |
| RS485 / Modbus | Industriel longue distance |

## PCB Design
1. Schema electrique (KiCad)
2. Placement composants
3. Routage pistes
4. Design Rule Check (DRC)
5. Gerber export pour fabrication
6. Assemblage (soudure CMS, refusion, vague)

## Prototypage rapide
- Impression 3D de boitiers (FDM, SLA)
- Breadboard -> PCB prototype -> fabrication
- Simulation de circuits (LTSpice, Proteus)
- Test et mesure (oscilloscope, multimetre, analyseur logique)
- Documentation technique (schematique, BOM, guide assemblage)

## Automatisation industrielle
- PLC (automates programmables) et SCADA
- Capteurs industriels (temperature, pression, debit)
- Relais, contacteurs et actuateurs
- Communication Modbus, OPC-UA

## Alimentation
- Batteries (LiPo, 18650, dimensionnement)
- Panneaux solaires + charge controller
- Power management (buck, boost, LDO)
- Monitoring de charge (coulomb counter, fuel gauge)
- UPS pour systemes critiques
