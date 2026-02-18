---
name: electronics-firmware
description: PCB, microcontroleurs, protocoles, firmware
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
## Protocoles
| Protocole | Usage |
|-----------|-------|
| I2C | Capteurs, ecrans (2 fils) |
| SPI | Memoire, ADC (rapide, 4 fils) |
| UART | Communication serie (2 fils) |
| CAN | Automobile, industriel |
## PCB Design
1. Schema electrique (KiCad)
2. Placement composants
3. Routage pistes
4. Design Rule Check (DRC)
5. Gerber export pour fabrication
