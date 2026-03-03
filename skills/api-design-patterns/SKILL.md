---
name: api-design-patterns
description: REST, versioning, pagination, gestion erreurs, HATEOAS
author: PhoenixProject
version: 1.0.0
created: 2026-02-18
last_updated: 2026-02-23
---

# API Design Patterns

## Conventions REST

### Nommage des endpoints

```
[OK] GET    /api/v1/users          -> Liste des utilisateurs
[OK] GET    /api/v1/users/:id      -> Un utilisateur
[OK] POST   /api/v1/users          -> Creer un utilisateur
[OK] PUT    /api/v1/users/:id      -> Remplacer un utilisateur
[OK] PATCH  /api/v1/users/:id      -> Modifier partiellement
[OK] DELETE /api/v1/users/:id      -> Supprimer

[INTERDIT] GET /api/v1/getUsers
[INTERDIT] POST /api/v1/createUser
[INTERDIT] GET /api/v1/user/delete/:id
```

### Versioning

Toujours versionner. Prefixe URL recommande.

```
/api/v1/...   -> Version stable
/api/v2/...   -> Nouvelle version (backward-compatible ou migration guide)
```

### Pagination

```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "perPage": 20,
    "total": 150,
    "totalPages": 8,
    "hasNext": true,
    "hasPrev": false
  }
}
```

### Gestion des erreurs

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The request body is invalid",
    "details": [
      {
        "field": "email",
        "message": "Must be a valid email address"
      }
    ]
  }
}
```

### Codes HTTP

| Code | Usage |
|------|-------|
| 200 | Succes |
| 201 | Cree |
| 204 | Succes sans contenu |
| 400 | Requete invalide |
| 401 | Non authentifie |
| 403 | Non autorise |
| 404 | Non trouve |
| 409 | Conflit |
| 422 | Entite non processable |
| 429 | Rate limited |
| 500 | Erreur serveur |

### Filtrage et tri

```
GET /api/v1/users?status=active&role=admin&sort=-createdAt&fields=id,name,email
```

## Anti-patterns

- Verbes dans les URLs (getUsers, createUser)
- Pas de versioning
- Retourner 200 avec un message d'erreur dans le body
- Pas de pagination sur les collections
- Exposer les IDs internes de la base de donnees
