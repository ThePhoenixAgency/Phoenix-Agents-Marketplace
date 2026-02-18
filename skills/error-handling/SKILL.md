---
name: error-handling
description: Patterns de gestion d'erreurs, retry, circuit breaker
---
# Error Handling
## Patterns
### Result Type
```typescript
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };
function divide(a: number, b: number): Result<number, string> {
  if (b === 0) return { ok: false, error: 'Division by zero' };
  return { ok: true, value: a / b };
}
```
### Retry avec backoff exponentiel
```typescript
async function retry<T>(fn: () => Promise<T>, maxRetries = 3, baseDelay = 1000): Promise<T> {
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (attempt === maxRetries) throw error;
      const delay = baseDelay * Math.pow(2, attempt) + Math.random() * 100;
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
  throw new Error('Unreachable');
}
```
### Circuit Breaker
```
CLOSED -> (erreur) -> OPEN -> (timeout) -> HALF-OPEN -> (succes) -> CLOSED
                                                     -> (echec)  -> OPEN
States:
  CLOSED: Normal, requetes passent
  OPEN: Bloque, fail fast
  HALF-OPEN: Test, une requete passe
```
## Anti-patterns
- catch vide (swallow errors)
- throw new Error() sans message
- Pas de distinction entre erreurs recoverables et fatales
- Retry sans backoff (DDoS self-inflicted)
