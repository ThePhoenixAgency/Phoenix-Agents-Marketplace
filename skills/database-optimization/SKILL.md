---
name: database-optimization
description: Query planning, indexing, N+1, connection pooling
author: PhoenixProject
version: 1.0.0
created: 2026-02-18
last_updated: 2026-02-23
---

# Database Optimization

## Indexing

### Quand creer un index

```
[OK] Colonnes dans WHERE, JOIN, ORDER BY frequents
[OK] Colonnes avec haute cardinalite
[OK] Index composite pour queries multi-colonnes

[INTERDIT] Index sur des colonnes rarement filtrees
[INTERDIT] Index sur des tables avec < 1000 lignes (sauf FK)
[INTERDIT] Trop d'index sur une table a forte ecriture
```

### Types d'index

| Type | Usage |
|------|-------|
| B-tree | Egalite, range, tri (defaut) |
| Hash | Egalite uniquement |
| GIN | JSONB, full-text, arrays |
| GiST | Geospatial, range types |
| BRIN | Donnees naturellement ordonnees |

## Prevention N+1

```
[INTERDIT] Boucle qui fait une query par iteration

for user in users:
    orders = db.query("SELECT * FROM orders WHERE user_id = ?", user.id)

[OK] Eager loading / JOIN

SELECT u.*, o.*
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE u.status = 'active';
```

## Connection Pooling

```
REGLES :
- Pool size = (cpu_cores * 2) + disk_spindles
- Max connections: 100 typiquement
- Idle timeout: 10-30 secondes
- Connection lifetime: 30 minutes max
```

## Query Optimization

### EXPLAIN ANALYZE

```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM orders
WHERE created_at > '2026-01-01'
AND status = 'completed'
ORDER BY total DESC
LIMIT 20;
```

### Checklist performance

- [ ] Pas de SELECT * en production
- [ ] Indexes sur les colonnes filtrees
- [ ] LIMIT sur les requetes de liste
- [ ] Pas de N+1
- [ ] Connection pooling configure
- [ ] Slow query logging active
- [ ] Vacuum regulier (PostgreSQL)
