---
version: 1.0.0
last_updated: 2026-02-04
status: Stable
---

# GEMINI WEB SEARCH PROTOCOL

## PROTOCOLE D'EXÉCUTION OBLIGATOIRE
1.  **START** : Lire `docs/BACKLOG.md` et les Standards de Gouvernance.
2.  **PROCESS** : Appliquer les règles sans déviation.
3.  **END** : Mettre à jour `docs/BACKLOG.md` et `docs/CHANGELOG.md` avant tout commit.

## [VITAL] CORE SEARCH RULES
1.  **Prioritize Official Sources**: Always prefer `developer.google.com`, `docs.apple.com`, `developer.apple.com`.
2.  **Experimental Tagging**: If a feature is marked "Experimental" or "Beta", explicitly state it in the synthesis.
3.  **Cross-Platform Verification**: When researching for Apple/macOS, check both SwiftUI and AppKit documentation unless specified.
4.  **Citations**: Use Markdown links for EVERY claim.

## [PROCESS] EXECUTION
- Use `search_web` for broad discovery.
- Use `read_url_content` for deep dives.
- Scan for "Deprecation notices" as a priority.

## [OUTPUT] FORMAT
- Summary of findings.
- Recommendation based on PhoenixProject Standards.
- List of URLs visited.
