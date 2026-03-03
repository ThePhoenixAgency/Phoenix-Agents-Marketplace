# Ownership Map — Propriete et Bus Factor

## Objectif

Identifier qui possede quoi dans le codebase :
- Detecter les "bus factor" critiques (1 seul contributeur)
- Trouver le code orphelin (jamais modifie, auteur inconnu)
- Evaluer les risques lies aux departs de developpeurs

## Analyse Git

```bash
# Contributeurs par fichier
git log --follow --format="%an" -- [fichier] | sort | uniq -c | sort -rn

# Top contributeurs par module
git log --format="%an" -- [repertoire]/ | sort | uniq -c | sort -rn | head -10

# Fichiers jamais modifies depuis 1 an
git log --since="1 year ago" --name-only --format="" | sort -u > recent.txt
git ls-files | grep -v -f recent.txt

# Dernier contributeur par fichier
git log --format="%an|%ae|%ad" --date=short -- [fichier] | head -1
```

## Methode d'Analyse

```bash
# 1. Generer la carte des contributeurs
git log --format="%H|%an|%ae|%ad" --date=short --name-only > git_log.txt

# 2. Identifier le "bus factor" par module
# Bus factor = 1 si un seul auteur a touche >80% des commits

# 3. Detecter le code orphelin
git log --since="2 years ago" --name-only --format="" | sort -u > recent_files.txt
git ls-files > all_files.txt
comm -23 <(sort all_files.txt) recent_files.txt > orphan_files.txt

# 4. Verifier les permissions CI/CD
# Qui peut merger sur main ? Qui a les cles de deploiement ?
```

## Indicateurs de Risque

| Indicateur | Seuil Critique | Action |
|------------|----------------|--------|
| Bus factor | = 1 | Documenter + former backup |
| Fichiers orphelins | > 30% | Revue + suppression ou adoption |
| Commits sans review | > 50% | Imposer code review obligatoire |
| Age moyen du code | > 3 ans sans MAJ | Audit de securite prioritaire |

## Rapport Ownership

```markdown
## Carte de Propriete — [REPO]
Date : YYYY-MM-DD

### Modules a Risque (bus factor = 1)
| Module | Proprietaire | Derniere activite | Risque |
|--------|-------------|-------------------|--------|
| auth/  | @alice | 2025-01-15 | CRITIQUE |

### Code Orphelin (>1 an sans modification)
[liste des fichiers]

### Recommandations
1. Former @bob sur auth/ (bus factor mitigation)
2. Auditer et supprimer [liste] de fichiers orphelins
3. Mettre en place CODEOWNERS pour les modules critiques
```

## Fichier CODEOWNERS (GitHub/GitLab)

```
# .github/CODEOWNERS
# Modules critiques — review obligatoire
/src/auth/        @security-team
/src/payments/    @payments-lead @security-team
/.github/         @devops-lead
/Dockerfile*      @devops-lead
```
