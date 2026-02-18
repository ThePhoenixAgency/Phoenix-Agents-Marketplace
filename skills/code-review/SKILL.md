---
name: code-review
description: Checklist review, patterns detection, feedback constructif
---
# Code Review
## Checklist
### Correction
- [ ] La logique est correcte
- [ ] Les edge cases sont geres (null, vide, limites)
- [ ] Les erreurs sont gerees proprement
- [ ] Pas de race conditions
### Qualite
- [ ] Noms descriptifs
- [ ] Pas de duplication
- [ ] Responsabilite unique
- [ ] Tests presents et suffisants
- [ ] Documentation (JSDoc) sur les fonctions publiques
### Securite
- [ ] Inputs valides et assainis
- [ ] Pas de secrets en dur
- [ ] Pas de donnees sensibles dans les logs
- [ ] SQL parametre (pas de concatenation)
### Performance
- [ ] Pas de N+1
- [ ] Pas de boucles couteuses inutiles
- [ ] Pas de re-render superflu (React)
- [ ] Pagination sur les collections
## Feedback constructif
```
[OK] Format :
"Ce bloc pourrait beneficier d'un early return pour reduire l'imbrication.
Exemple : if (!condition) return; au lieu du if/else."

[INTERDIT] Format :
"C'est mal fait."
"Pourquoi tu as fait ca comme ca ?"
```
