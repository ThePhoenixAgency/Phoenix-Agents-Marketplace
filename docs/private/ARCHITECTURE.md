# ARCHITECTURE - Systeme Multi-Agents
# Created: 2026-02-18
# Last Updated: 2026-02-18 19:47

Source de verite de l'architecture du systeme multi-agents.
Propriete de ThePhoenixAgency. Aucune dependance externe.

---

## VISION

Systeme autonome d'agents IA organise comme une entreprise.
- Model-agnostic : Ollama, LM Studio, OpenAI, Anthropic, ou tout endpoint compatible
- Self-contained : aucune dependance tiers obligatoire
- Plugin marketplace natif
- 6 orchestrateurs specialises par mission, en parallele

---

## DEPLOIEMENT

```
Couche 1 : Plugin Marketplace
  Format natif (.claude-plugin/marketplace.json)
  Agents, skills, commands, hooks, rules, scripts
  |
Couche 2 : Proxy Router
  Route vers n'importe quel backend LLM
  Configuration par tier (T1/T2/T3)
  |
  +-- Ollama (local, gratuit)
  +-- LM Studio (local, gratuit)
  +-- OpenAI (distant, optionnel)
  +-- Anthropic (distant, optionnel)
  +-- Tout endpoint OpenAI-compatible
  |
Couche 3 : Orchestration
  Multi-machine mesh peer-to-peer
  Communication inter-agents (AMP)
  Memoire persistante + consolidation
  Gateways (Slack, Discord, Email, WhatsApp)
```

Cout par defaut : 0. Tout tourne en local sur modeles gratuits.
Modeles payants = optionnels, jamais obligatoires.

---

## TIERS DE COMPLEXITE

| Tier | Capacite | Modeles compatibles |
|------|----------|---------------------|
| T1 | Triage, classification, taches systematiques | llama3:8b, mistral:7b, phi-3, gemma2:9b |
| T2 | Raisonnement, redaction, analyse | llama3:70b, mixtral:8x7b, qwen2:72b, deepseek-v2 |
| T3 | Architecture, code complexe, securite | llama3:405b, deepseek-coder-v2, qwen2.5-coder:32b |

---

## ORCHESTRATEURS (6)

Chaque orchestrateur coordonne une mission. 3 au moins tournent H24, les autres a la demande.
Le project-manager delegue aux orchestrateurs.

```
project-manager (chef d'orchestre global)
 |
 +-- web-orchestrator --------- Dev web (a la demande)
 +-- apple-orchestrator -------- Dev macOS/iOS (a la demande)
 +-- community-orchestrator ---- Redaction, reseaux, automatisation (a la demande)
 |
 +-- security-orchestrator ----- Securite interieure (H24)
 +-- home-orchestrator --------- Domotique, IoT (H24)
 +-- infra-orchestrator -------- Serveurs, reseau, monitoring (H24)
```

| # | Orchestrateur | Mission | Agents mobilises | Mode |
|---|--------------|---------|------------------|------|
| O1 | web-orchestrator | Sites web, apps web, SaaS | SoftArch, Dev, Designer, QA, DevOps, Secu, DataAI | Demande |
| O2 | apple-orchestrator | macOS, iOS, watchOS, tvOS | SoftArch, Dev (swift), Designer, QA, Secu | Demande |
| O3 | community-orchestrator | Contenu, reseaux sociaux, automation | CM, BizMgr, ExecAssist, Designer | Demande |
| O4 | security-orchestrator | Securite physique, reseau, cameras, alarmes | Secu, NetArch, Sysadmin, Maker | H24 |
| O5 | home-orchestrator | Domotique, automatisation maison, IoT | Maker, Sysadmin, NetArch, DataAI | H24 |
| O6 | infra-orchestrator | Serveurs, monitoring, deploiement, incident | Sysadmin, DevOps, NetArch, Secu | H24 |

Les sous-agents meta (agent-organizer, context-manager, task-distributor, error-coordinator,
knowledge-synthesizer, workflow-orchestrator, multi-agent-coordinator) sont partages
entre les 6 orchestrateurs.

---

## AGENTS SPECIALISTES (21)

### Direction & Gestion

| # | Agent | Role | Tier |
|---|-------|------|------|
| 1 | project-manager | Pilotage global, planning, validation, agile, sprint | T2 |
| 2 | product-owner | Vision produit, backlog, priorisation, acceptation | T2 |

### Business & Communication

| # | Agent | Role | Tier |
|---|-------|------|------|
| 3 | business-analyst | Analyse besoins, specs, faisabilite, processus | T2 |
| 4 | business-manager | Vente, marketing, pricing, go-to-market, growth, SEO | T2 |
| 5 | community-manager | Contenu, reseaux sociaux, bots, automatisation publication | T2 |
| 6 | support-agent | Tickets, knowledge base, escalation, satisfaction | T1 |
| 7 | executive-assistant | Planning, mails, coordination, gestion du temps | T2 |

### Engineering

| # | Agent | Role | Tier |
|---|-------|------|------|
| 8 | software-architect | Architecture, patterns, decisions, MCP, DX | T3 |
| 9 | fullstack-dev | Code tous langages, TDD, frontend/backend/mobile/CLI | T3 |
| 10 | security-auditor | Pentest, OSINT, bug bounty, audit, blockchain, TOUTES skills | T3 |
| 11 | qa-engineer | Tests, accessibilite, performance, chaos, resilience | T2 |
| 12 | devops-engineer | CI/CD, containers, cloud, K8s, Terraform, SRE, incident | T2 |

### Infrastructure

| # | Agent | Role | Tier |
|---|-------|------|------|
| 13 | network-architect | Topologie reseau, firewalls, VPN, securite perimetre | T3 |
| 14 | sysadmin | Serveurs, maintenance, hardware, Raspberry Pi, monitoring | T2 |

### Design & Data

| # | Agent | Role | Tier |
|---|-------|------|------|
| 15 | ui-ux-designer | Design, prototypage, design system, branding, UX research | T2 |
| 16 | data-analyst | BI, dashboards, metriques, recherche, tendances, benchmarks | T2 |

### Data & IA

| # | Agent | Role | Tier |
|---|-------|------|------|
| 17 | data-ai-lead | IA, ML, DL, LLM, NLP, computer vision, data engineering | T3 |

### Maker

| # | Agent | Role | Tier |
|---|-------|------|------|
| 18 | maker-specialist | Electronique, 3D, firmware, IoT, robotique, domotique | T3 |

### Conformite & Finance

| # | Agent | Role | Tier |
|---|-------|------|------|
| 19 | legal-advisor | Contrats, licences, propriete intellectuelle, brevets | T2 |
| 20 | finance-controller | Budget, facturation, pricing, tresorerie, gestion du risque | T1 |
| 21 | compliance-officer | RGPD, AI Act, DPO, ethique IA, Privacy by Design | T2 |

---

## MATRICE DE DELEGATION : Agent -> Sous-agents

### project-manager (1)
classifier, spec-writer, web-researcher, code-reviewer, hub-manager,
scrum-master, git-workflow-manager

### product-owner (2)
classifier, spec-writer, hub-manager, market-analyst, web-researcher

### business-analyst (3)
classifier, spec-writer, web-researcher, threat-modeler,
accessibility-auditor, performance-auditor, market-analyst,
market-researcher, benchmarking-specialist

### business-manager (4)
web-researcher, copywriter, market-analyst, sales-strategist,
sales-engineer, customer-success-manager, seo-specialist,
content-strategist, growth-engineer, marketing-analyst,
content-marketer, pricing-optimizer

### community-manager (5)
web-researcher, copywriter, social-poster, bot-manager,
blog-writer, social-media-writer, newsletter-writer,
social-automator, video-scripter

### support-agent (6)
classifier, web-researcher, ticket-handler, knowledge-writer

### executive-assistant (7)
web-researcher, copywriter, ticket-handler, hub-manager,
social-poster, bot-manager, calendar-scheduler

### software-architect (8)
architect, code-reviewer, threat-modeler, performance-auditor,
web-researcher, mcp-developer, dx-optimizer, refactoring-specialist,
monorepo-tooling, api-documentation

### fullstack-dev (9)
web-researcher, architect, implementer, mobile-dev, code-reviewer,
qa-tester, firmware-dev, cli-developer, build-engineer,
dependency-manager, legacy-modernizer, tooling-engineer,
vscode-extension-dev, testing-infrastructure,
typescript-pro, python-pro, golang-pro, rust-engineer,
swift-expert, java-architect, react-specialist, nextjs-developer,
blockchain-developer, game-developer, fintech-engineer,
payment-integrator, e-commerce-engineer, media-streaming-dev,
geospatial-engineer

### security-auditor (10)
web-researcher, pentester, osint-recon, bug-bounty-hunter,
code-reviewer, threat-modeler, ownership-analyzer,
blockchain-auditor, chaos-engineer, debugger,
security-researcher

[REGLE SPECIALE]
Le security-auditor a acces a TOUTES les skills du systeme au niveau BASE minimum.
Ses skills en securite sont au niveau EXPERT.
Il doit comprendre chaque technologie pour pouvoir l'auditer.

### qa-engineer (11)
web-researcher, code-reviewer, qa-tester, accessibility-auditor,
performance-auditor, monitoring-agent, chaos-engineer, debugger,
error-detective, test-automator, benchmarking-specialist,
testing-infrastructure

### devops-engineer (12)
web-researcher, pipeline-builder, container-manager, deploy-agent,
monitoring-agent, code-reviewer, kubernetes-specialist,
terraform-engineer, sre-engineer, cloud-architect,
platform-engineer, incident-responder, database-administrator,
developer-portal

### network-architect (13)
architect, web-researcher, network-designer, firewall-manager,
threat-modeler

### sysadmin (14)
web-researcher, server-manager, monitoring-agent,
hardware-inventory, firewall-manager

### ui-ux-designer (15)
web-researcher, wireframer, visual-designer, ux-researcher,
copywriter, brand-guardian, mobile-ux-optimizer

### data-analyst (16)
web-researcher, data-collector, report-builder, visualization-agent,
market-analyst, search-specialist, trend-analyst,
competitive-analyst, data-researcher, marketing-analyst,
technology-scout, benchmarking-specialist, patent-analyst,
academic-researcher

### data-ai-lead (17)
web-researcher, ai-engineer, data-engineer, data-scientist,
database-optimizer, llm-architect, ml-engineer, mlops-engineer,
nlp-engineer, prompt-engineer, computer-vision-engineer,
recommendation-engine, etl-specialist, vector-db-engineer,
feature-engineer

### maker-specialist (18)
web-researcher, electronics-designer, 3d-modeler, firmware-dev,
hardware-inventory, iot-engineer, robotics-engineer,
voice-assistant-dev, embedded-systems

### legal-advisor (19)
web-researcher, contract-reviewer, compliance-checker,
license-auditor, patent-analyst

### finance-controller (20)
web-researcher, budget-tracker, invoice-manager, pricing-optimizer,
market-analyst, risk-manager

### compliance-officer (21)
web-researcher, rgpd-auditor, ai-ethics-reviewer,
data-mapping-agent, consent-manager, compliance-checker,
healthcare-compliance (si domaine sante actif)

---

## SOUS-AGENTS META (partages entre orchestrateurs)

| Sous-agent | Role |
|-----------|------|
| agent-organizer | Organisation et routage entre agents |
| context-manager | Compression contexte, resumes de session |
| task-distributor | Allocation et distribution des taches |
| error-coordinator | Gestion erreurs dans workflows multi-agents |
| knowledge-synthesizer | Compression info, graphes de connaissances |
| workflow-orchestrator | Pipelines multi-agents complexes |
| multi-agent-coordinator | Execution parallele, fusion des resultats |

---

## CATALOGUE COMPLET DES SOUS-AGENTS (142)

### Gestion & Coordination (8)
classifier, spec-writer, web-researcher, hub-manager,
scrum-master, calendar-scheduler, git-workflow-manager,
agent-organizer

### Code & Architecture (10)
architect, implementer, mobile-dev, code-reviewer,
mcp-developer, refactoring-specialist, dx-optimizer,
legacy-modernizer, monorepo-tooling, api-documentation

### Specialistes Langages (12)
typescript-pro, python-pro, golang-pro, rust-engineer,
swift-expert, java-architect, react-specialist, nextjs-developer,
blockchain-developer, game-developer, fintech-engineer,
payment-integrator

### Dev Tools (6)
cli-developer, build-engineer, dependency-manager,
tooling-engineer, vscode-extension-dev, testing-infrastructure

### Securite & Audit (8)
pentester, osint-recon, bug-bounty-hunter, threat-modeler,
ownership-analyzer, blockchain-auditor, debugger,
security-researcher

### Qualite & Tests (7)
qa-tester, accessibility-auditor, performance-auditor,
chaos-engineer, error-detective, test-automator,
benchmarking-specialist

### DevOps & Cloud (8)
pipeline-builder, container-manager, deploy-agent,
kubernetes-specialist, terraform-engineer, sre-engineer,
cloud-architect, developer-portal

### Infra (7)
platform-engineer, incident-responder, database-administrator,
network-designer, firewall-manager, server-manager,
monitoring-agent

### Design (5)
wireframer, visual-designer, ux-researcher,
brand-guardian, mobile-ux-optimizer

### Business & Vente (9)
market-analyst, sales-strategist, sales-engineer,
customer-success-manager, seo-specialist, content-strategist,
growth-engineer, marketing-analyst, content-marketer

### Communication & Support (6)
copywriter, social-poster, bot-manager, ticket-handler,
knowledge-writer, risk-manager

### Contenu & Redaction (5)
blog-writer, social-media-writer, newsletter-writer,
social-automator, video-scripter

### Data & Recherche (9)
data-collector, report-builder, visualization-agent,
search-specialist, trend-analyst, competitive-analyst,
data-researcher, technology-scout, academic-researcher

### Data & IA (11)
ai-engineer, data-engineer, data-scientist, database-optimizer,
llm-architect, ml-engineer, mlops-engineer, nlp-engineer,
prompt-engineer, computer-vision-engineer, recommendation-engine

### Data Engineering (3)
etl-specialist, vector-db-engineer, feature-engineer

### Maker & IoT (5)
electronics-designer, 3d-modeler, firmware-dev,
iot-engineer, robotics-engineer

### Domaines specialises (6)
e-commerce-engineer, media-streaming-dev, geospatial-engineer,
voice-assistant-dev, embedded-systems, hardware-inventory

### Legal & Compliance (8)
contract-reviewer, compliance-checker, license-auditor,
patent-analyst, budget-tracker, invoice-manager,
pricing-optimizer, rgpd-auditor

### Conformite avancee (3)
ai-ethics-reviewer, data-mapping-agent, consent-manager

### Healthcare (1)
healthcare-compliance

### Meta & Orchestration (6)
context-manager, task-distributor, error-coordinator,
knowledge-synthesizer, workflow-orchestrator,
multi-agent-coordinator

---

## SKILLS (57)

### Universelles (TOUS les agents)

| Skill | Description |
|-------|-------------|
| continuous-learning | Veille techno, extraction de patterns, adaptation |
| web-research | Recherche multi-sources, cross-validation, synthese |
| documentation | Redaction technique, JSDoc/SwiftDoc |
| communication | Rapports, echanges, comptes-rendus |
| secure-coding | Securite de base (Zero Trust), niveau variable |
| agent-messaging | Communication AMP inter-agents |
| memory-search | Recherche semantique dans memoire persistante |

### Architecture & Code (12)

| Skill | Description |
|-------|-------------|
| tdd-mastery | Red-green-refactor, test-first, couverture cible |
| api-design-patterns | REST, versioning, pagination, gestion erreurs |
| frontend-excellence | Architecture composants, state management, perf |
| react-patterns | Hooks, server components, suspense, error boundaries |
| nextjs-mastery | App Router, RSC, ISR, server actions, middleware |
| graphql-design | Schema, DataLoader, subscriptions, pagination |
| typescript-advanced | Generics, conditional types, mapped types |
| rust-systems | Ownership, traits, async patterns |
| microservices-design | Event-driven, saga pattern, service mesh |
| websocket-realtime | Socket.io, SSE, reconnection, scaling |
| mobile-development | React Native, Flutter, responsive layouts |
| git-advanced | Worktrees, bisect, interactive rebase, hooks |

### Data & IA (4)

| Skill | Description |
|-------|-------------|
| data-engineering | ETL pipelines, Spark, star schema, qualite donnees |
| machine-learning | Pipelines ML, training, evaluation, deploiement |
| prompt-engineering | Chain-of-thought, few-shot, structured outputs |
| llm-integration | Streaming, function calling, RAG, optimisation cout |

### Infrastructure & DevOps (7)

| Skill | Description |
|-------|-------------|
| kubernetes-operations | Deployments, Helm charts, HPA, troubleshooting |
| docker-best-practices | Multi-stage builds, compose, optimisation images |
| cloud-patterns | Lambda, DynamoDB, CDK, S3, services manages |
| ci-cd-pipelines | GitHub Actions, GitLab CI, matrix builds |
| infrastructure-as-code | Terraform, IaC patterns, state management |
| monitoring-observability | OpenTelemetry, Prometheus, structured logging |
| redis-patterns | Caching, rate limiting, pub/sub, streams |

### Base de donnees (3)

| Skill | Description |
|-------|-------------|
| database-optimization | Query planning, indexing, N+1, connection pooling |
| postgres-optimization | EXPLAIN ANALYZE, indexes, partitioning, JSONB |
| graph-query | CozoDB, Neo4j, requetes graphe |

### Securite (4)

| Skill | Description |
|-------|-------------|
| security-hardening | Input validation, auth, secrets management, CSP |
| authentication-patterns | JWT, OAuth2 PKCE, RBAC, session management |
| blockchain | Smart contracts, DeFi, audit, crypto |
| pentest-workflow | OWASP, reconnaissance, exploitation, rapport |

### Qualite (4)

| Skill | Description |
|-------|-------------|
| testing-strategies | Contract, snapshot, property-based testing |
| accessibility-wcag | ARIA, keyboard navigation, contraste couleurs |
| performance-optimization | Code splitting, image optim, Core Web Vitals |
| chaos-testing | Injection pannes, resilience, blast radius |

### Langages specifiques (5)

| Skill | Description |
|-------|-------------|
| python-best-practices | Type hints, dataclasses, async/await, packaging |
| golang-idioms | Error handling, interfaces, concurrency, layout |
| django-patterns | DRF, ORM optimization, signals, middleware |
| springboot-patterns | JPA, REST controllers, layered architecture |
| swift-apple-ecosystem | SwiftUI, MVVM, async/await, Combine, Xcode |

### Business & Contenu (4)

| Skill | Description |
|-------|-------------|
| market-knowledge | Analyse marche, TAM/SAM/SOM, pricing |
| social-media-automation | Scheduling, cross-posting, analytics, growth hacking |
| content-strategy | Calendrier editorial, SEO content, funnels |
| copywriting | Redaction persuasive, storytelling, conversion |

### Meta (3)

| Skill | Description |
|-------|-------------|
| project-planning | Agile, sprint, estimation, priorisation |
| agents-management | Coordination multi-agents, delegation, suivi |
| docs-search | Indexation et recherche dans documentation |

### Hardware & Maker (4)

| Skill | Description |
|-------|-------------|
| hardware-knowledge | Composants, assemblage, diagnostic, Raspberry Pi |
| apple-ecosystem | macOS, iOS, watchOS, integration Apple |
| iot-domotique | MQTT, edge computing, digital twins, capteurs |
| electronics-firmware | PCB, microcontroleurs, protocoles, firmware |

---

## COMMANDS (42)

### Git (7)
| Commande | Description |
|----------|-------------|
| /commit | Commit conventionnel depuis les changes staged |
| /pr-create | Creer PR avec resume, plan de test, labels |
| /changelog | Generer changelog depuis l'historique |
| /release | Release taggee avec notes auto-generees |
| /worktree | Setup git worktrees pour dev parallele |
| /fix-issue | Corriger une issue par numero |
| /pr-review | Review PR avec feedback structure |

### Testing (6)
| Commande | Description |
|----------|-------------|
| /tdd | Cycle TDD complet |
| /test-coverage | Analyser couverture, suggerer tests manquants |
| /e2e | Generer scenarios end-to-end |
| /integration-test | Tests integration pour endpoints API |
| /snapshot-test | Tests snapshot/golden file |
| /test-fix | Diagnostiquer et corriger tests echouants |

### Architecture (6)
| Commande | Description |
|----------|-------------|
| /plan | Plan d'implementation avec evaluation risques |
| /refactor | Workflow refactoring structure |
| /migrate | Migration framework ou librairie |
| /adr | Ecrire Architecture Decision Record |
| /diagram | Generer diagrammes Mermaid depuis le code |
| /design-review | Conduire design review structuree |

### Documentation (5)
| Commande | Description |
|----------|-------------|
| /doc-gen | Generer documentation depuis le code |
| /update-codemap | Mettre a jour code map projet |
| /api-docs | Generer docs API depuis les handlers |
| /onboard | Creer guide d'onboarding pour nouveaux devs |
| /memory-bank | Mettre a jour la banque memoire |

### Securite (5)
| Commande | Description |
|----------|-------------|
| /audit | Audit securite code et dependances |
| /hardening | Appliquer mesures de durcissement |
| /secrets-scan | Scanner secrets et credentials fuites |
| /csp | Generer headers Content Security Policy |
| /dependency-audit | Auditer dependances pour vulnerabilites |

### Refactoring (5)
| Commande | Description |
|----------|-------------|
| /dead-code | Trouver et supprimer code mort |
| /simplify | Reduire complexite du fichier courant |
| /extract | Extraire fonction, composant ou module |
| /rename | Renommer symbole dans toute la codebase |
| /cleanup | Supprimer code mort et imports inutilises |

### DevOps (5)
| Commande | Description |
|----------|-------------|
| /dockerfile | Generer Dockerfile optimise |
| /ci-pipeline | Generer config pipeline CI/CD |
| /k8s-manifest | Generer manifests Kubernetes |
| /deploy | Deployer vers environnement configure |
| /monitor | Setup monitoring et alerting |

### Workflow (3)
| Commande | Description |
|----------|-------------|
| /checkpoint | Sauvegarder progression et contexte |
| /wrap-up | Terminer session avec resume et apprentissages |
| /orchestrate | Lancer pipeline workflow multi-agents |

---

## HOOKS (14)

### PreToolUse
| Hook | Matcher | Role |
|------|---------|------|
| block-dev-outside-tmux | Bash | Bloquer dev server hors tmux |
| tmux-reminder | Bash | Rappel tmux pour commandes longues |
| git-push-review | Bash | Rappel review avant git push |
| block-random-docs | Write | Bloquer creation fichiers .md inutiles |
| suggest-compact | Edit/Write | Suggerer compaction a intervalles logiques |

### PreCompact
| Hook | Matcher | Role |
|------|---------|------|
| pre-compact-save | * | Sauvegarder etat avant context compaction |

### SessionStart
| Hook | Matcher | Role |
|------|---------|------|
| session-start | * | Charger contexte precedent, detecter package manager |

### PostToolUse
| Hook | Matcher | Role |
|------|---------|------|
| pr-log | Bash | Logger URL PR apres creation |
| post-edit-format | Edit | Auto-format avec Prettier apres edits |
| post-edit-typecheck | Edit | TypeScript check apres edit .ts/.tsx |
| post-edit-console-warn | Edit | Warning console.log apres edits |

### Stop
| Hook | Matcher | Role |
|------|---------|------|
| check-console-log | * | Checker console.log dans fichiers modifies |

### SessionEnd
| Hook | Matcher | Role |
|------|---------|------|
| session-end | * | Persister etat de session |
| evaluate-session | * | Evaluer session pour patterns extractables |

---

## CONTEXTS (3)

| Contexte | Role |
|----------|------|
| dev | Developpement (TDD, code, build, debug) |
| research | Recherche (web, analyse, rapport, benchmark) |
| review | Review (code review, PR, audit, securite) |

---

## RULES (5)

| Categorie | Role |
|-----------|------|
| common | Regles communes tous langages |
| golang | Regles Go |
| python | Regles Python |
| typescript | Regles TypeScript |
| swift | Regles Swift/Apple |

---

## SCHEMAS (3)

| Schema | Role |
|--------|------|
| hooks.schema.json | Validation format hooks |
| package-manager.schema.json | Validation config package manager |
| plugin.schema.json | Validation format plugin marketplace |

---

## SCRIPTS

### Core
| Script | Role |
|--------|------|
| lib/helpers.sh | Fonctions partagees (logs, validation) |
| lib/config.sh | Chargement config agent + modele |

### Pipeline
| Script | Role |
|--------|------|
| pipeline/preflight.sh | Verification pre-lancement |
| pipeline/spec-gate.sh | Validation specifications |
| pipeline/develop.sh | Lancement dev TDD |
| pipeline/test.sh | Execution tests |
| pipeline/audit-security.sh | Scan securite |
| pipeline/validate.sh | Validation humain |
| pipeline/deploy.sh | Deploiement |
| pipeline/post-deploy.sh | Verification post-deploy |

### Communication inter-agents (AMP)
| Script | Role |
|--------|------|
| amp/init.sh | Initialiser identite agent |
| amp/send.sh | Envoyer un message |
| amp/inbox.sh | Consulter boite de reception |
| amp/read.sh | Lire un message |
| amp/reply.sh | Repondre |
| amp/delete.sh | Supprimer |
| amp/fetch.sh | Recuperer messages externes |
| amp/register.sh | Enregistrer aupres d'un provider |
| amp/status.sh | Statut agent et registrations |
| amp/identity.sh | Gestion identite |
| amp/security.sh | Securite des messages |

### Documentation
| Script | Role |
|--------|------|
| docs/index.sh | Indexer la documentation |
| docs/index-delta.sh | Indexation incrementale |
| docs/search.sh | Rechercher dans la doc |
| docs/list.sh | Lister les documents |
| docs/get.sh | Recuperer un document |
| docs/find-by-type.sh | Chercher par type |
| docs/stats.sh | Statistiques documentation |

### Graph
| Script | Role |
|--------|------|
| graph/index-delta.sh | Indexation incrementale code graph |
| graph/find-callers.sh | Trouver les appelants |
| graph/find-callees.sh | Trouver les appeles |
| graph/find-related.sh | Trouver le code lie |
| graph/find-associations.sh | Trouver les associations |
| graph/find-by-type.sh | Chercher par type de noeud |
| graph/find-path.sh | Chemin entre deux noeuds |
| graph/describe.sh | Decrire un noeud |

### Memory & Agents
| Script | Role |
|--------|------|
| memory/search.sh | Recherche semantique |
| agents/list.sh | Lister tous les agents |
| agents/export.sh | Exporter un agent |
| agents/import.sh | Importer un agent |

### Hooks (JS)
| Script | Role |
|--------|------|
| hooks/session-start.js | Charger contexte + detecter PM |
| hooks/session-end.js | Persister etat |
| hooks/pre-compact.js | Sauver avant compaction |
| hooks/suggest-compact.js | Suggerer compaction |
| hooks/post-edit-format.js | Auto-format Prettier |
| hooks/post-edit-typecheck.js | TypeScript check |
| hooks/post-edit-console-warn.js | Warning console.log |
| hooks/check-console-log.js | Checker console.log |
| hooks/evaluate-session.js | Evaluer session |

---

## CI/CD WORKFLOWS

| Workflow | Role |
|----------|------|
| ci.yml | Integration continue |
| release.yml | Release automatique |
| security-scan.yml | Scan securite automatique |
| maintenance.yml | Maintenance automatique |
| reusable-test.yml | Tests reutilisables |
| reusable-validate.yml | Validation reutilisable |
| reusable-release.yml | Release reutilisable |

---

## INFRASTRUCTURE

### Modules coeur

| Module | Role | Priorite |
|--------|------|----------|
| AMP | Communication inter-agents (Ed25519) | MUST |
| Agent Registry | Registre persistant des agents | MUST |
| Content Security | Detection prompt injection | MUST |
| Memory | Memoire persistante | MUST |

### Modules avances

| Module | Role | Priorite |
|--------|------|----------|
| Cerebellum | Sous-systeme memoire + buffer terminal | SHOULD |
| CozoDB | Base de donnees graph | SHOULD |
| Host Mesh | Multi-machines peer-to-peer | SHOULD |
| Subconscient | Indexation arriere-plan, consolidation | SHOULD |
| Gateways | Slack, Discord, Email, WhatsApp | SHOULD |
| Equipes + Kanban | Teams, reunions, suivi taches | SHOULD |
| Voice | Interactions vocales avec agents | COULD |
| Domain Service | Multi-organisations | COULD |
| Agent Identity | Avatars, personnalites | COULD |

---

## TOTAUX

| Categorie | Nombre |
|-----------|--------|
| Orchestrateurs | 6 |
| Agents specialistes | 21 |
| Sous-agents (mutualises) | 142 |
| Sous-agents meta (partages) | 7 |
| Skills | 57 |
| Commands | 42 |
| Hooks | 14 |
| Contexts | 3 |
| Rules | 5 |
| Schemas | 3 |
| Scripts pipeline | 8 |
| Scripts AMP | 11 |
| Scripts docs | 7 |
| Scripts graph | 8 |
| Scripts memory/agents | 4 |
| Scripts hooks (JS) | 9 |
| CI/CD workflows | 7 |
| Modules infrastructure | 13 |
| **TOTAL composants** | **367** |
