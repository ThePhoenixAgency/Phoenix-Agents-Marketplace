---
version: 1.0.0
last_updated: 2026-02-04
status: Stable
---

# CHATGPT WEB SEARCH PROTOCOL (ATLAS)

## PROTOCOLE D'EXÉCUTION OBLIGATOIRE
1.  **START** : Lire `docs/BACKLOG.md` et les Standards de Gouvernance.
2.  **PROCESS** : Appliquer les règles sans déviation.
3.  **END** : Mettre à jour `docs/BACKLOG.md` et `docs/CHANGELOG.md` avant tout commit.

## [VITAL] CORE SEARCH RULES
1.  **DALL-E Integration**: Use visualization for architectural diagrams when requested.
2.  **Browsing Context**: Leverage "Current Page Context" in Atlas to correlate local code with online documentation.
3.  **Python Audit**: Use Python Code Interpreter to verify snippets found on the web if possible.
4.  **Privacy**: Never share sensitive `/private/` content in web search queries.

## [PROCESS] EXECUTION
- Correlate search results with the active code in the sidebar.
- Identify library versions from `package.json` or `Podfile` before searching.

## [OUTPUT] FORMAT
- Synthesis of documentation.
- Code snippets adapted to the current project.
- List of sources.
