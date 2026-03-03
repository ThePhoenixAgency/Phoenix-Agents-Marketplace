---
name: testing-strategies
description: Contract, snapshot, property-based testing
author: PhoenixProject
version: 1.0.0
created: 2026-02-18
last_updated: 2026-02-23
---
# Testing Strategies
## Contract Testing
Verifier que l'API respecte son contrat (schema).
```typescript
test('GET /users should match contract', async () => {
  const response = await request(app).get('/api/v1/users');
  expect(response.status).toBe(200);
  expect(response.body).toMatchSchema(userListSchema);
});
```
## Snapshot Testing
```typescript
test('UserCard renders correctly', () => {
  const tree = renderer.create(<UserCard user={mockUser} />).toJSON();
  expect(tree).toMatchSnapshot();
});
```
## Property-Based Testing
```typescript
import fc from 'fast-check';
test('sort is idempotent', () => {
  fc.assert(fc.property(
    fc.array(fc.integer()),
    (arr) => {
      const sorted = arr.slice().sort((a, b) => a - b);
      const sortedTwice = sorted.slice().sort((a, b) => a - b);
      return JSON.stringify(sorted) === JSON.stringify(sortedTwice);
    }
  ));
});
```
## Pyramide des tests
```
          /  E2E  \          Peu, chemins critiques
         /  Integ  \         Moyen, API boundaries
        /  Unitaire \        Beaucoup, logique metier
```
