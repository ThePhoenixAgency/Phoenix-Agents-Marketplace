---
name: web-research
description: Procedural guidance for conducting deep web research, technical audits, and market analysis. Use when an agent needs to gather information from the internet to validate technical choices or analyze market trends.
metadata:
  short-description: Deep web research and analysis
---

# Web Research Skill

## PROTOCOLE D'EXÉCUTION OBLIGATOIRE
1.  **START** : Lire `docs/BACKLOG.md` et les Standards de Gouvernance.
2.  **PROCESS** : Appliquer les règles sans déviation.
3.  **END** : Mettre à jour `docs/BACKLOG.md` et `docs/CHANGELOG.md` avant tout commit.

This skill provides a structured methodology for technical and strategic research on the web.

## Research Protocol

1.  **Define Scope**: Clearly identify the keywords and the specific technical or business question.
2.  **Source Identification**:
    - **Tier 1**: Official documentation, GitHub repos, academic papers.
    - **Tier 2**: StackOverflow, Reddit (specialized subs), corporate blogs (Engineering blogs).
    - **Tier 3**: News articles, general forums.
3.  **Cross-Validation**: Always verify a claim across at least two independent sources.
4.  **Version Checking**: Ensure the information is relevant to the versions being used in the project.

## Information Synthesis

-   Collect links for every critical finding.
-   Identify "Breaking Changes" or deprecated features.
-   Synthesize findings into `docs/research/RESEARCH_REPORT.md`.

## Tools

-   `search_web`: For broad queries.
-   `read_url_content`: For deep dives into specific documentation.
-   `grep_search`: (Internal) To find relevant snippets in local research history.
