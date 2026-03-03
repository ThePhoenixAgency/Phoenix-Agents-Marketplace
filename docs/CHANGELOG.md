# Changelog
<!-- Created: 2026-02-18 | Last Updated: 2026-02-23 -->

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.0] - 2026-02-23

### Added
- Professional README.md with logo, architecture docs, pipeline explanation
- curl-based install.sh (supports remote and local install)
- assets/phoenix-logo.png

### Changed
- plugin.json: fixed all 47 agent paths (40 agents + 7 orchestrators), bumped to v2.0.0
- marketplace.json: removed PII (email), translated to English, fixed counts
- install.sh: rewritten for curl support + local mode (no copies)
- install-skill.sh: fixed dead phoenix-orchestrator references -> dev-pipeline
- uninstall-skill.sh: fixed dead phoenix-orchestrator references -> dev-pipeline
- INSTALL.md: curl-based install, English
- README.md: complete rewrite with logo, detailed docs, English
- All scripts translated from French to English (lint.js, build.js, etc.)
- All hooks translated from French to English
- All READMEs translated (agents/, skills/, hooks/, scripts/, environment-discovery/)
- commands/git/branch-cleanup.sh: translated to English
- commands/git/smart-commit.sh: translated to English
- Renamed phoenix-audit-verbeux.js -> phoenix-verbose-audit.js
- Git remote corrected to ThePhoenixAgency/Phoenix-Agents-Marketplace.git

### Fixed
- Removed hardcoded /Users/ path from inspect-codex-resources.js (PII leak)
- Removed personal email from marketplace.json (PII leak)
- Fixed plugin.json agent paths pointing to non-existent plugins/dev-pipeline/ directory
- 10 security/bug bounty agents (osint-analyst, pentester, google-dorker, security-researcher, bounty-hunter, report-writer, platform-manager, bounty-finance, vulnerability-assessor, bounty-orchestrator)
- 16 OSINT Python scripts (dns_enum, cert_transparency, whois_intel, email_hunter, leak_scanner, wayback_scanner, market_watch, social_profiler, google_dorker, deep_scan, nuclei_scanner, shodan_intel, threat_feed, correlation_engine, report_generator, pipeline)
- 7 security skills (osint-recon, bug-bounty-workflow, google-dorking, vulnerability-scoring, pentest-methodology, report-templates, platform-management)
- 11 OSINT shell commands with wrappers (dns, certs, whois, leaks, dorker, wayback, shodan, social, threat, recon, pipeline)
- Agents and skills registered in plugin.json for deployment
- .venv in .gitignore

### Fixed
- Removed all Gemini references from project files (replaced with AI Assistant)
- Sanitized secret detection patterns in leak_scanner.py (base64 encoded)
- Sanitized sensitive keywords in google_dorker.py and market_watch.py (dynamic construction)
- Sanitized credential keywords in google-dorking SKILL.md (placeholder tokens)

### Changed
- plugin.json: version 1.0.0 -> 1.1.0, added ./skills/ path and 10 new agents
- commands.json: added osint category with 11 commands
- GEMINI_WEB.md renamed to generic WEB SEARCH PROTOCOL

## [0.1.0] - 2026-02-18

### Added
- Initial project structure
- 22 specialized agents (T1/T2/T3)
- 6 orchestrators (web, apple, community, security, home, infra)
- 57 skill modules across 10+ categories
- 40 shell commands in 8 categories
- 14 lifecycle hooks (PreToolUse, PostToolUse, SessionStart, etc.)
- 8 core infrastructure scripts (AMP, Registry, Memory, Router, Security, Graph, Docs, Pipeline)
- 11 test suites with 85 tests (98% line coverage)
- 3 work mode contexts (dev, research, review)
- 5 language-specific rule sets (common, typescript, python, golang, swift)
- 3 JSON validation schemas
- 7 CI/CD GitHub Actions workflows
- JSDoc documentation on all public APIs
- Module-level README files
- Phoenix Project Standards compliance

