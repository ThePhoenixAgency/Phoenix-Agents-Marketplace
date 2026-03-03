# BACKLOG : PHOENIX PROJECT
**Version:** 2.0
**Dernière mise à jour:** 2026-02-23

---

## 1. URGENCES (MUST HAVE)
- [ ] Étudier et réutiliser l'existant `vscode-antigravity-cockpit` + `cockpit-tools` pour le nouveau cockpit local (inclut quota, statut, multi-compte, wakeup), avant tout prototypage.
- [ ] Rétablir l'intégrité du pipeline Codex/Goose (EN COURS)
- [ ] Restaurer le skill `web-research` et l'accès réseau
- [ ] Valider la présence de `AGENTS.md` dans tous les workspaces

## 2. DÉVELOPPEMENT (SHOULD HAVE)
- [ ] Refonte des outils de certification (Scan CVE, Module Validator)
- [ ] Nettoyage des caches système profonds (.npm, CloudKit)
- [ ] Audit final de la RAM (Surgical Audit)

## 3. MAINTENANCE (COULD HAVE)
- [ ] Mise à jour de la documentation private
- [ ] Optimisation des performances TUI

---

## SESSION 2026-02-23 : Préparation publication Marketplace

### DONE
- [x] Fix plugin.json (chemins agents corrigés, 40 agents + 7 orchestrateurs)
- [x] Fix remote git -> ThePhoenixAgency/Phoenix-Agents-Marketplace.git
- [x] Suppression email personnel de marketplace.json
- [x] Suppression chemin dur /Users/ dans inspect-codex-resources.js
- [x] Traduction FR->EN : scripts/, hooks/, commands/git/, READMEs
- [x] Réécriture install.sh (curl + local, zero copie)
- [x] Fix install-skill.sh (phoenix-orchestrator -> dev-pipeline)
- [x] Fix uninstall-skill.sh (phoenix-orchestrator -> dev-pipeline)
- [x] Renommage phoenix-audit-verbeux.js -> phoenix-verbose-audit.js
- [x] Réécriture README.md avec logo, doc complète, EN
- [x] Mise à jour marketplace.json (comptages, EN, tags)
- [x] Mise à jour INSTALL.md (curl, EN)

### TODO
- [x] Traduire les 40 agents individuels en anglais (44 fichiers, TDD verified)
- [ ] Publier sur GitHub ThePhoenixAgency
- [ ] Installer plugin dans Claude Code depuis GitHub
- [ ] Configurer Gemini et Codex
- [ ] Auditer les 1.6 GO de cache local
- [ ] Nettoyer dossier plugins/ (legacy)

## SESSION 2026-02-27 : Étude existerant `Antigravity Cockpit` (et réutilisation adaptée)

### DONE
- [x] Relevé des fonctionnalités clés de `vscode-antigravity-cockpit` (dashboard webview/quickpick, quotas, status bar multi-modèles, seuils, notifications, modes local/autorisé, auto wake-up, multi-comptes).
- [x] Relevé des fonctionnalités clés de `cockpit-tools` (multi-comptes multi-instances, wake-up, quota monitor multi-plateformes, WebSocket local, orchestration d’apps).
- [x] Inventaire des commandes/settings de réutilisation: `agCockpit.*` (commands, statusBar, quotas, accountTree, thresholds) et flux de compte/notifications de `cockpit-tools`.

### SOURCES CONSULTÉES
- https://github.com/jlcodes99/vscode-antigravity-cockpit
- https://github.com/jlcodes99/cockpit-tools
- `README.en.md` et `README.md` (2 dépôts)
- `package.json` de `vscode-antigravity-cockpit` (contributions, commandes, configuration)

### PLAN D’EXTRACTION
- [x] Créer `docs/private/ANTIGRAVITY_COCKPIT_REUSE_PLAN.md` avec mapping:
  - réutilisable: commandés/config, status bar, seuils, wake-up, multi-compte
  - anti-patterns à éviter
  - mapping d’API (usage/limits/bascule)
  - plan d’itérations et critères d’acceptance

### DÉCISIONS PRODUIT
- [x] Ne pas faire une réécriture 1:1 de `vscode-antigravity-cockpit`; réutiliser les motifs adaptés.
- [x] Ne pas se limiter à l’existant antigravity : intégrer en même temps IA locale, fallback cross-provider, et compactage de contexte.
- [x] UI en français et/ou anglais uniquement (pas d’UI asiatique dans la solution cible).

---

## SESSION 2026-03-03 : Gouvernance immuable + Phoenix Orchestrateur

### VISION PRODUIT
Phoenix = ecosysteme agnostique de gestion de vie entiere par agents IA.
Vendre un package auto-installable pour Mac/PC/mobile/serveur/entreprise.
Pilotage vocal et texte. Multimodal. Toujours parallele. Toujours compact.

### DONE
- [x] Fusion security-audit SKILL.md v2.0.0 (249 lignes sub-plugin + modulaire)
- [x] 5 fichiers references/ crees (secure-coding, osint-recon, bugbounty, ownership, threat-modeling)
- [x] agents/security-reviewer.md v2.0.0 avec directive skill explicite
- [x] agents/security-auditor/agent.md v2.0.0 avec directive skill explicite
- [x] skills/governance-standards/SKILL.md v1.0.0 (hub 9 standards S00-S08)
- [x] agents/standards-enforcer.md v1.0.0 (sous-agent haiku parallele non-bloquant)
- [x] skills/dev-pipeline/SKILL.md v2.1.0 (integration standards-enforcer parallele)
- [x] agents/orchestrators/phoenix-orchestrator.md v1.0.0 (orchestrateur maitre T0)
- [x] Injection governance-standards dans 7 sous-orchestrateurs
- [x] ~/.agents/MEMORY.md mis a jour (standards_path, phoenix_orchestrator)
- [x] ~/.agents/AGENTS.override.md secs 12+13 (standards + monitoring contexte %)

### TODO
- [ ] Completer les agents manquants du marketplace (skill-creator, agent-creator)
- [ ] Skill context-monitor : afficher [CTX: XX%] en continu
- [ ] phoenix-orchestrator : ajouter web-researcher en phase 0 (recherche avant action)
- [ ] Audit dossier phoenix-orchestrator legacy (~/.claude/skills/phoenix-orchestrator/)
- [ ] Publier sur GitHub ThePhoenixAgency
- [ ] Package auto-installable (install.sh) pour Mac/PC/Docker
- [ ] Nettoyer dossier plugins/ (legacy)

### DECISIONS PRODUIT
- Standards S00-S08 sont immuables. Aucun agent ne les modifie.
- Phoenix est l'orchestrateur T0 : le seul interlocuteur de l'utilisateur.
- Tout est parallele. standards-enforcer tourne toujours en arriere-plan.
- Compaction automatique a 70%, obligatoire a 85%.
- Agnostique Claude/Codex/OpenClaw/Docker.
