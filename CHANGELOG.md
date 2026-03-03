# Changelog

All notable changes to this project will be documented in this file.
Format: [Conventional Commits](https://www.conventionalcommits.org/)
Versioning: [SemVer 2.0.0](https://semver.org/)

---

## [2.0.0] - 2026-02-27

### Added
- OSINT toolkit: cert_transparency, dns_enum, email_hunter, google_dorker, shodan_intel, social_profiler, wayback_scanner, whois_intel
- Bug bounty division: bounty-orchestrator, bounty-hunter, bounty-finance agents
- Security plugin: security-audit plugin with dedicated SKILL.md
- 59 new skills (116 total): crypto-trading, agent-economics, voice-interface, computer-vision, etc.
- Codex-compatible agent variants: fullstack-dev, qa-engineer, security-auditor, software-architect, spec-writer
- New orchestrators: bounty-orchestrator
- install.sh v2: curl-safe, symlink-based, zero file copy
- hooks/pre-compact.js: state preservation before context compaction
- hooks/suggest-compact.js: compact suggestion every 50 edits
- CI workflows: continuous-integrity.yml, quad-daily-guard.yml
- standards/ directory: governance docs (00-06 + domain-specific)
- schemas/: hooks, package-manager, plugin JSON schemas
- commands/: security, test, git, arch, docs, refactor, devops categories

### Changed
- plugin.json: 47 agents (40 specialists + 7 orchestrators, all paths verified)
- marketplace.json: updated metadata, model-agnostic keywords
- All scripts, hooks, and README translated EN
- Architecture documented in docs/private/ARCHITECTURE.md (367 components)

### Removed
- Gemini references from all project files
- Personal email from marketplace.json
- Hardcoded /Users/ paths from scripts

---

## [1.0.0] - 2026-02-18

### Added
- Initial release: 21 specialist agents, 6 orchestrators
- 57 core skills
- 14 hooks (PreToolUse, PostToolUse, SessionStart, SessionEnd)
- dev-pipeline plugin (9-phase pipeline)
- AMP protocol for inter-agent communication
- Memory system (MemorySystem class)
- Build validation script
- Jest test suite: amp-protocol, agent-registry, memory-system, proxy-router, hooks, amp-signing
