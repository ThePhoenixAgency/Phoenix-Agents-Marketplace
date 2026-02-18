# Rules: TypeScript
# Created: 2026-02-18

## Strict mode
- strict: true dans tsconfig.json
- noImplicitAny: true
- strictNullChecks: true
- noUnusedLocals: true
- noUnusedParameters: true

## Conventions
- Interfaces pour les contracts publics
- Types pour les unions et intersections
- Enums seulement si necessaire (const objects preferes)
- Utiliser as const pour les literals
- Pas de any sauf cas justifie et documente
- Generics avec des noms descriptifs (pas T si ambigu)

## Patterns
- Discriminated unions pour les states
- Zod pour la validation runtime
- Result<T, E> pour les erreurs typees
