---
name: postgres-optimization
description: EXPLAIN ANALYZE, indexes, partitioning, JSONB
---
# PostgreSQL Optimization
## EXPLAIN ANALYZE
```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT u.name, COUNT(o.id) as order_count
FROM users u
JOIN orders o ON o.user_id = u.id
WHERE u.created_at > '2026-01-01'
GROUP BY u.name
ORDER BY order_count DESC
LIMIT 10;
```
Lire le plan : Seq Scan = pas d'index, Index Scan = bon.
Verifier actual time vs estimated rows.
## Indexing
```sql
-- Index simple
CREATE INDEX idx_users_email ON users (email);
-- Index composite (ordre des colonnes = important)
CREATE INDEX idx_orders_user_status ON orders (user_id, status);
-- Index partiel
CREATE INDEX idx_orders_active ON orders (created_at) WHERE status = 'active';
-- Index JSONB
CREATE INDEX idx_metadata ON products USING GIN (metadata);
```
## Partitioning
```sql
CREATE TABLE events (
  id BIGSERIAL,
  created_at TIMESTAMPTZ NOT NULL,
  data JSONB
) PARTITION BY RANGE (created_at);
CREATE TABLE events_2026_01 PARTITION OF events
  FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
```
## JSONB
```sql
-- Query JSONB
SELECT * FROM products WHERE metadata @> '{"color": "red"}';
SELECT metadata->>'brand' FROM products WHERE metadata ? 'brand';
```
