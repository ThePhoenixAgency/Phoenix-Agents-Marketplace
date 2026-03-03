---
name: frontend-excellence
description: Architecture composants, state management, performance budgets
author: PhoenixProject
version: 1.0.0
created: 2026-02-18
last_updated: 2026-02-23
---

# Frontend Excellence

## Architecture composants

### Regles de decomposition

```
1. Un composant = une responsabilite
2. Props descendent, events remontent
3. Composants presentationnels vs containers
4. Composition plutot qu'heritage
5. Maximum 150 lignes par composant
```

### Organisation fichiers

```
src/
  components/
    Button/
      Button.tsx
      Button.test.tsx
      Button.module.css
      index.ts
  features/
    auth/
      components/
      hooks/
      services/
      types/
```

## State Management

| Outil | Usage |
|-------|-------|
| Local state (useState) | UI locale, formulaires simples |
| Context | Theme, locale, auth |
| Zustand/Jotai | State global leger |
| React Query/SWR | Cache serveur, data fetching |
| Redux Toolkit | State complexe avec middleware |

## Performance Budgets

| Metrique | Budget |
|----------|--------|
| First Contentful Paint | < 1.8s |
| Largest Contentful Paint | < 2.5s |
| Cumulative Layout Shift | < 0.1 |
| First Input Delay | < 100ms |
| Total Blocking Time | < 200ms |
| Bundle size (gzipped) | < 200kb |

## Techniques d'optimisation

- Code splitting avec lazy() et Suspense
- Image optimization (WebP, AVIF, lazy loading)
- Memoization (React.memo, useMemo, useCallback)
- Virtualisation des listes longues
- Prefetching des routes probables
- Service Workers pour le cache
