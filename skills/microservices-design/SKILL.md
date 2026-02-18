---
name: microservices-design
description: Event-driven, saga pattern, service mesh
---
# Microservices Design
## Event-Driven Architecture
```
Service A -> Event Bus -> Service B
                       -> Service C
Events sont immutables et ordonnees.
Chaque service possede ses propres donnees.
Communication asynchrone par defaut.
```
## Saga Pattern
```
Saga = sequence de transactions locales avec compensation.
1. Order Service: createOrder() -> OrderCreated
2. Payment Service: processPayment() -> PaymentCompleted
3. Inventory Service: reserveStock() -> StockReserved
4. Shipping Service: createShipment() -> ShipmentCreated
COMPENSATION (si echec a l'etape 3):
3. Inventory Service: ECHEC -> StockReservationFailed
2. Payment Service: refundPayment() -> PaymentRefunded
1. Order Service: cancelOrder() -> OrderCancelled
```
## Service Communication
| Pattern | Usage |
|---------|-------|
| REST/gRPC | Requetes synchrones |
| Message Queue | Commandes asynchrones |
| Event Stream | Events (Kafka, NATS) |
| Service Mesh | Observabilite, retry, circuit breaker |
## Anti-patterns
- Base de donnees partagee entre services
- Couplage synchrone en cascade
- Services trop granulaires (nano-services)
- Pas de circuit breaker
