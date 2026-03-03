---
name: project-tracker
description: Suivi event-driven de l'etat des projets. Alternative aux Kanban boards. Invoquer quand une tache importante est terminee, bloquee, ou prise de decision. Lie automatiquement les commits git aux phases du projet. Produit des summaries de session lisibles.
argument-hint: "action: progress|blocker|decision|pivot - description de l'evenement"
---

# SKILL : project-tracker
# Created: 2026-03-02
# Last Updated: 2026-03-02
# Principe : les events sont logs DANS le checklog.md existant du projet.
# Pas de base de donnees supplementaire. Zero friction.

## POURQUOI

Les BACKLOG.md deviennent statiques et ne capturent pas le "pourquoi" des decisions.
Ce skill enrichit le cycle BACKLOG.md + checklog.md avec :
- Traçage des commits git lies aux phases
- Journalisation des blocages et decisions avec leur contexte
- Summary de session auto-genere

## QUAND INVOQUER

- "J'ai fini [tache]" -> log progress, mettre a jour MEMORY.md
- "Bloque sur [probleme]" -> log blocker dans checklog.md, MEMORY.md section next_action
- "Decision : [choix]" -> log decision avec justification dans ARCHIVE.md
- "Pivot vers [nouvelle approche]" -> log pivot + raison dans ARCHIVE.md
- "Status du projet ?" -> generer un summary depuis BACKLOG.md + checklog.md + git log

## PHASES D'EXECUTION

### Phase 1 - Identifier le type d'evenement

Classifier l'entree :
- PROGRES  : tache terminee, avancement
- BLOCAGE  : impediment, attente externe
- DECISION : choix architectural, technique, ou produit
- PIVOT    : changement de direction significatif
- QUERY    : demande de status (lecture seule)

### Phase 2 - Lier aux commits git (si applicable)

Pour les evenements PROGRES :
```bash
git log --oneline --since="1 hour ago" 2>/dev/null | head -5
```
Inclure les SHA des commits pertinents dans le log de l'evenement.

### Phase 3 - Logger l'evenement

**PROGRES et BLOCAGE** -> `<repo>/docs/checklog.md`
Format :
```
### [YYYY-MM-DD HH:MM] [TYPE] [phase courante]
- Description : [evenement]
- Commits lies : [SHA si applicable]
- Impact BACKLOG : [item mis a jour]
```

**DECISION et PIVOT** -> `~/.agents/ARCHIVE.md` (persistance inter-sessions)
Format :
```
### Decision du YYYY-MM-DD : [sujet]
Contexte : [pourquoi ce choix]
Alternatives ecartees : [ce qui n'a pas ete choisi et pourquoi]
Impact : [fichiers / direction affectes]
```

### Phase 4 - Mettre a jour MEMORY.md

Appeler : `~/.agents/hooks/write-memory.sh [agent] [projet] "[last]" "[next]" [version] [branch]`

### Phase 5 - Summary de session (uniquement si QUERY ou fin de session)

Generer depuis les sources existantes :
```
SUMMARY [date]
- Ce qui est fait depuis la derniere session : [depuis checklog.md]
- Commits recents : [git log --oneline -10]
- Blocages ouverts : [grep -i "BLOCAGE" docs/checklog.md | tail -5]
- Prochaines actions : [BACKLOG.md section EN_COURS]
```

## REGLES

- Pas de base de donnees externe. Tout dans les fichiers existants.
- DECISIONS et PIVOTS -> ARCHIVE.md (persistant, inter-projets)
- PROGRES et BLOCAGES -> checklog.md du repo (local au projet)
- MEMORY.md mis a jour apres chaque evenement significatif
- Zero duplication avec BACKLOG.md : checklog = journal, BACKLOG = plan
