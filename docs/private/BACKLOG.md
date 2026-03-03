# Backlog
<!-- Created: 2026-02-18 | Last Updated: 2026-02-23 -->

Source de verite de la gestion de projet. NE JAMAIS EFFACER, marquer DONE.

## Must Have

- [x] Core scripts infrastructure (AMP, Registry, Memory, Router, Security) - 2026-02-18 DONE
- [x] 22 agents specialistes + 6 orchestrateurs - 2026-02-18 DONE
- [x] 57 skills - 2026-02-18 DONE
- [x] 40 commands shell - 2026-02-18 DONE
- [x] 14 hooks lifecycle - 2026-02-18 DONE
- [x] Tests >90% coverage (85 tests, 98% lines) - 2026-02-18 DONE
- [x] JSDoc sur tous les scripts core - 2026-02-18 DONE
- [x] CI/CD workflows (7 pipelines) - 2026-02-18 DONE
- [x] README, CONTRIBUTING, INSTALL, CHANGELOG, LICENSE - 2026-02-18 DONE
- [x] .gitignore + SECURITY.md - 2026-02-18 DONE
- [x] Module-level README files - 2026-02-18 DONE
- [x] Initial commit + push GitHub - 2026-02-18 DONE
- [x] Bug Bounty division : 10 agents securite (osint-analyst, pentester, google-dorker, security-researcher, bounty-hunter, report-writer, platform-manager, bounty-finance, vulnerability-assessor, bounty-orchestrator) - 2026-02-18 DONE
- [x] OSINT toolkit : 16 scripts Python (dns, certs, whois, email, leaks, wayback, market, social, dorker, deep_scan, nuclei, shodan, threat, correlation, report, pipeline) - 2026-02-18 DONE
- [x] 7 skills securite (osint-recon, bug-bounty-workflow, google-dorking, vulnerability-scoring, pentest-methodology, report-templates, platform-management) - 2026-02-18 DONE
- [x] Suppression references Gemini -> AI Assistant - 2026-02-19 DONE
- [x] Sanitisation secrets (base64 patterns, dorks dynamiques, gitignore .venv) - 2026-02-19 DONE
- [x] Integration plugin.json (skills + agents enregistres) - 2026-02-19 DONE
- [x] 11 commandes OSINT (wrappers shell) + commands.json - 2026-02-19 DONE
- [x] Tests validation (18 scripts syntaxe, 11 wrappers, npm test 85/85, scan secrets clean) - 2026-02-19 DONE
- [x] Verifier que tous les CI/CD passent - 2026-02-19 DONE
- [x] Pipeline CI adaptee aux skills OSINT/BB (Python lint + syntax) - 2026-02-19 DONE
- [x] Refactor scripts OSINT : remplacement bs4 par regex natifs - 2026-02-19 DONE
- [ ] Normaliser tous les agents : frontmatter YAML uniforme (name, tier, description, author: PhoenixProject, version: 1.0.0, created, last_updated)
- [ ] Normaliser toutes les skills : capsule documentaire + frontmatter SemVer + author PhoenixProject
- [ ] Reecrire les 64 skills existantes avec noms explicites (pas de prefixe phoenix-)
- [ ] Importer et reecrire les skills du repo antigravity-awesome-skills (trier, fusionner, ameliorer)
- [ ] Supprimer les 8 dossiers phoenix-* (doublons des skills existantes, contenu fusionne)
- [ ] JSDoc/docstring sur tous les scripts (hooks, commands)
- [ ] Mettre a jour README agents/ (dit 21 mais il y en a 33)
- [ ] Integration avec Codex (symlink marketplace.local + config.toml)
- [ ] Integration avec ORCHESTRATION_IA (destroy pods, rebuild from marketplace)
- [ ] Multi-plateforme : valider compatibilite Antigravity, Claude Code, Codex CLI
- [ ] Publier version finale sur GitHub
- [ ] Mise a jour en cascade dans tous les repos dependants :
  - ~/.codex/ (config.toml, AGENTS.override.md, standards/agents/, standards/templates/)
  - ORCHESTRATION_IA (pods, agents, skills)
  - OpenClaw (skills references)
  - Tout futur projet qui pioche dans le marketplace

## Should Have

- [x] Plugin marketplace.json description enrichie - 2026-02-19 DONE
- [ ] CLI installer (`npx phoenix-agents-marketplace install`)
- [ ] Auto-update mechanism pour les skills
- [ ] Dashboard web pour monitoring agents

## Could Have

- [ ] VS Code extension pour marketplace browsing
- [ ] Templates pour creer de nouveaux agents/skills
- [ ] Metrics et analytics sur l'utilisation des agents
- [ ] Integration avec d'autres LLM providers

## Won't Have (v1)

- Custom LLM training pipeline
- SaaS hosting platform
- Billing/subscription management
