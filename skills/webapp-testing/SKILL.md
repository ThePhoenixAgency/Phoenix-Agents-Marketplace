---
name: webapp-testing
description: Tests web apps avec Playwright pour verification UI et debug
---
# Webapp Testing (Playwright)
## Setup
```typescript
import { test, expect } from '@playwright/test';
test.describe('Login Page', () => {
  test('should login with valid credentials', async ({ page }) => {
    await page.goto('/login');
    await page.fill('[data-testid="email"]', 'user@test.com');
    await page.fill('[data-testid="password"]', 'password123');
    await page.click('[data-testid="submit"]');
    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('h1')).toContainText('Dashboard');
  });
  test('should show error for invalid credentials', async ({ page }) => {
    await page.goto('/login');
    await page.fill('[data-testid="email"]', 'wrong@test.com');
    await page.fill('[data-testid="password"]', 'wrong');
    await page.click('[data-testid="submit"]');
    await expect(page.locator('[data-testid="error"]')).toBeVisible();
  });
});
```
## Visual Regression
```typescript
test('should match visual snapshot', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveScreenshot('homepage.png', {
    maxDiffPixels: 100,
  });
});
```
## Best Practices
- Utiliser data-testid pour les selecteurs (stable)
- Attendre les elements avant d'interagir (await expect)
- Isoler les tests (pas de dependance a l'ordre)
- Screenshot sur echec pour debug
