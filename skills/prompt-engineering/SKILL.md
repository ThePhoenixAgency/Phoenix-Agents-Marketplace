---
name: prompt-engineering
description: Chain-of-thought, few-shot, structured outputs, optimisation
---

# Prompt Engineering

## Techniques

### Chain-of-thought (CoT)

Forcer le raisonnement etape par etape.

```
Resous ce probleme etape par etape :
1. D'abord, identifie les donnees
2. Ensuite, analyse les contraintes
3. Puis, propose une solution
4. Enfin, verifie la solution
```

### Few-shot

Fournir des exemples avant la tache.

```
Voici des exemples de classification :
- "Le produit ne fonctionne pas" -> categorie: bug
- "J'aimerais une nouvelle feature" -> categorie: feature-request
- "Comment configurer X ?" -> categorie: support

Classifie : "Le bouton de login ne repond plus"
-> categorie:
```

### Structured Output

Forcer un format de sortie precis.

```
Reponds UNIQUEMENT avec un objet JSON valide :
{
  "severity": "low|medium|high|critical",
  "category": "string",
  "summary": "string (max 100 chars)",
  "action_required": true|false
}
```

## Anti-patterns

- Prompts vagues et ambigus
- Instructions contradictoires
- Trop de contraintes en une seule instruction
- Pas d'exemples pour les taches complexes
- Oublier de specifier le format de sortie

## Optimisation des couts

| Technique | Reduction |
|-----------|-----------|
| Cache de prompts similaires | 40-60% |
| Compression du contexte | 20-30% |
| Choix du modele adapte au tier | 50-80% |
| Batch processing | 30-50% |
