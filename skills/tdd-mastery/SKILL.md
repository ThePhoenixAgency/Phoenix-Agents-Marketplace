---
name: tdd-mastery
description: Cycle TDD Red-Green-Refactor, test-first design, couverture cible
author: PhoenixProject
version: 1.0.0
created: 2026-02-18
last_updated: 2026-02-23
---

# TDD Mastery

## Quand utiliser cette skill

A chaque fois que tu implementes de la logique metier ou fonctionnelle.
Aucune exception. Le code metier sans test prealable est interdit.

## Cycle TDD

### Phase 1 : RED (ecrire le test)

Le test DOIT echouer. Si le test passe avant l'implementation, il est mauvais.

```
CHECKLIST RED :
- [ ] Le test decrit UN comportement precis
- [ ] Le test a un nom descriptif (should_do_X_when_Y)
- [ ] Le test echoue pour la bonne raison (pas une erreur de syntaxe)
- [ ] Le test est independant (pas de dependance a l'ordre)
```

### Phase 2 : GREEN (implementation minimale)

Ecrire le MINIMUM de code pour faire passer le test. Pas plus.

```
ANTI-PATTERNS GREEN :
- [INTERDIT] Implementer plus que ce que le test demande
- [INTERDIT] Ajouter des abstractions "au cas ou"
- [INTERDIT] Optimiser avant que le test passe
```

### Phase 3 : REFACTOR (ameliorer)

Refactoriser sans casser le test. Le test est le filet de securite.

```
CHECKLIST REFACTOR :
- [ ] Le test passe toujours
- [ ] Pas de duplication
- [ ] Noms explicites
- [ ] Responsabilite unique
- [ ] Complexite reduite
```

## Couverture cible

| Type | Seuil minimum |
|------|--------------|
| Unitaire | > 90% |
| Integration | > 70% |
| E2E | Chemins critiques couverts |

## Patterns de test

### Arrange-Act-Assert (AAA)

```javascript
test('should calculate total with tax', () => {
  // Arrange
  const cart = new Cart();
  cart.addItem({ price: 100, quantity: 2 });

  // Act
  const total = cart.calculateTotal({ taxRate: 0.2 });

  // Assert
  expect(total).toBe(240);
});
```

### Given-When-Then (BDD)

```python
def test_user_login_with_valid_credentials():
    # Given
    user = create_user(email="test@test.com", password="secure123")

    # When
    result = auth_service.login("test@test.com", "secure123")

    # Then
    assert result.is_authenticated is True
    assert result.token is not None
```

## Anti-patterns a eviter

- Tests couples a l'implementation (mock excessif)
- Tests fragiles (dependance aux details d'implementation)
- Tests sans assertions
- Tests qui testent le framework, pas le code
- Noms de tests generiques (test1, test2)
