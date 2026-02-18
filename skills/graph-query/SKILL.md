---
name: graph-query
description: CozoDB, Neo4j, requetes graphe
---
# Graph Query
## Cypher (Neo4j)
```cypher
MATCH (u:User)-[:FOLLOWS]->(f:User)
WHERE u.name = 'Alice'
RETURN f.name, f.email
MATCH (u:User)-[:PURCHASED]->(p:Product)<-[:PURCHASED]-(other:User)
WHERE u.id = $userId AND NOT (u)-[:PURCHASED]->(p2)<-[:PURCHASED]-(other)
RETURN other, collect(p.name) as commonProducts
```
## CozoDB
```
?[name, email] := *users[name, email, role], role = 'admin'
?[a, b, path] := *follows[a, b], path = [a, b]
?[a, b, path] := ?[a, c, p1], *follows[c, b], path = append(p1, b)
```
## Quand utiliser un graphe
- Relations complexes (social, recommandations)
- Traversal multi-niveaux (amis d'amis)
- Recherche de chemins
- Knowledge graphs
