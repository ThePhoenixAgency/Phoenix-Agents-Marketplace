---
name: manuals-research
description: Indexation et recherche sémantique dans la documentation technique et les manuels.
author: PhoenixProject
version: 1.1.0
created: 2026-02-18
last_updated: 2026-02-23
---
# Manuals Research
## Indexation
1. Scanner tous les fichiers .md, .txt, .rst
2. Extraire headers, contenu, metadata
3. Generer des embeddings par chunk
4. Stocker dans un index local (FAISS, SQLite-VSS)
## Recherche
1. Query utilisateur -> embedding
2. Similarity search dans l'index
3. Retourner les K chunks les plus proches
4. Presenter avec context et source
## Format
```
Q: "comment configurer le proxy"
R: 3 resultats trouves
  1. [ARCHITECTURE.md:45] "Proxy Router - Route les requetes..."
  2. [README.md:23] "Configuration du proxy dans..."
  3. [INSTALL.md:15] "Variables d'environnement proxy..."
```
