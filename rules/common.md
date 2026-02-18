# Rules: common
# Created: 2026-02-18
# Regles communes a tous les projets

## Conventions

1. Noms de variables descriptifs (pas de temp, data, result sans contexte)
2. Fonctions < 30 lignes idealement
3. Fichiers < 300 lignes idealement
4. Un fichier = une responsabilite
5. Imports ordonnes (std, external, internal)
6. Pas de magic numbers (constantes nommees)
7. Pas de code commente laisse en place
8. Pas de console.log en production
9. Gestion d'erreurs explicite (pas de catch vide)
10. DRY mais sans abstraction prematuree

## Format de commit
```
<type>(<scope>): <subject>

<body>

Co-Authored-By: AI Assistant
```

## Documentation
- JSDoc/SwiftDoc sur toute fonction publique
- README.md par module
- Horodatage sur chaque fichier cree/modifie
