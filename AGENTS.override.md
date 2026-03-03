# [PRIVATE] AGENTS OVERRIDE - LOIS DE GOUVERNANCE PHOENIXPROJECT

**Version** : 1.5.0 (SemVer)
**Statut** : PRIORITÉ ABSOLUE SUR TOUT AUTRE DOCUMENT
**Dernière mise à jour** : 2026-02-25

## 🚨 RÈGLES CRITIQUES D'EXÉCUTION (ZÉRO TOLÉRANCE)

### 1. STANDARDS DE COMMUNICATION (RÈGLE #0)
- **RELecture SYSTÉMATIQUE.** L'agent doit relire l'intégralité de ce document de gouvernance (AGENTS.override.md) AVANT et APRÈS chaque action individuelle.
- **ZERO EMOJI.** Interdiction absolue dans le code, les commits, la documentation et les logs.
- Utilisez exclusivement les balises textuelles : `[OK]`, `[WARNING]`, `[ERROR]`, `[INFO]`, `[PRIVATE]`.

### 2. SÉCURITÉ ACTIVE & SECRET ABSOLU
- [ERROR] **BANNISSEMENT DES TERMES SENSIBLES.** Les mots `password` et `credentials` sont **PROSCRITS**.
- [OK] **CONSULTATION OBLIGATOIRE.** L'agent doit systématiquement consulter le dashboard **GitGuardian** (via navigateur) avant toute action pour identifier les fuites de secrets orphelines.
- [CRITICAL] **SECRET ABSOLU.** Ne jamais révéler la stratégie technique, les vecteurs d'attaque, ou les détails de remédiation de sécurité dans le `README.md`, les commits, les PR ou toute autre documentation publique.
- Utilisez : `secret`, `token`, `code`, `identifiant`, `key`, `authenticator`.
- **E-mails.** Interdiction d'écrire des adresses mail en dur. Utilisation exclusive des GitHub Secrets et des pipelines CI/CD.
- **Keychain.** Masquage des constantes Apple (ex: `kSecClassGenericPassword`) derrière des alias sécurisés.

### 3. INTÉGRITÉ DU CODE & UPSTREAM
- [ERROR] **NON-DESTRUCTIF (SIDE-ONLY).** Interdiction de modifier le code existant ou l'interface d'un Upstream (ex: `openclaw`).
- **Implémentation.** On implémente exclusivement des fonctionnalités "Side" (Wrappers, Extensions, Modules Sidecar).
- [ERROR] **INTERDICTION D'INVENTER.** Respect absolu des noms de fichiers, dossiers, dépôts et projets existants.

### 4. QUALITÉ SÉNIOR & TRANSPARENCE
- [ERROR] **ZÉRO PLACEHOLDER.** Interdiction des stubs, `TODO`, `pass` ou données fictives. Tout code est complet et fonctionnel.
- [ERROR] **VÉRACITÉ ABSOLUE.** Interdiction de mentir sur l'état d'avancement ou la réussite d'un test.
- **Documentation.** Docstring systématique (paramètres/retours/exceptions) et commentaires par bloc logique détaillés.
- **SemVer 2.0.0.** Suivre strictement le versionnement sémantique.

### 5. PIPELINE DE DÉVELOPPEMENT (RÉFÉRENCE)
- Respect strict des 9 phases du **dev-pipeline** (Marketplace Skill) :
  1. Classification
  2. Spécification
  3. Recherche
  4. Architecture
  5. Implémentation (TDD strict)
  6. Sécurité (Zero Trust)
  7. QA (Tests unitaires / Intégration)
  8. Accessibilité (WCAG 2.2 AAA)
  9. Performance
  - Exigence obligatoire et permanente:
  - Découverte locale IA en continu sur LAN (`192.168.x.x`, plage configurable), avec prise en charge explicite des providers locaux (Ollama, LM Studio, OpenAI-compatible) et des déploiements Docker.
  - Choix explicite utilisateur via /local ou /remote; fallback automatique vers IA locale obligatoire quand le quota distant est épuisé ou en cas d’erreur/timeout du provider distant.
  - Monitoring d’usage cross-provider obligatoire (tokens, coût estimé, ratio réduction via compactage), incluant Copilot même en mode payant.
  - Compaction de session obligatoire de type Claude: résumer l’essentiel, compacter le reste, réinjecter le résumé dans la session active puis en fallback vers session secondaire / notes locales.
  - Cette règle est transversale et doit être appliquée systématiquement, quel que soit le lot de travail.
- Contrôle préalable obligatoire avant implémentation:
  - Revue ciblée OWASP Top 10 (site officiel OWASP) pour les technologies impliquées dans la pile (VS Code extension, TypeScript, Node.js, webview).
  - Revue CVE/alertes sécurité pour les dépendances et APIs touchées (NVD/CVE, GitHub Advisory Database).
  - Centraliser les artefacts sécurité et de remédiation dans `docs/private/security.md`.
  - Revue d’existant avant réécriture: `vscode-antigravity-cockpit` pour la logique de suivi de quota/status bar, et `cockpit-tools` pour la coordination multi-plateforme de quota.
  - Traces obligatoires dans le backlog: sources consultées + version/date des vérifications.

### 6. WORKFLOW & AUTORISATION (HITL)
- **Autorisation de Lecture.** Lecture autorisée sans demande préalable pour comprendre le contexte.
- **Confirmation d'Écriture.** Confirmation `Oui / Non` obligatoire avant toute action impactante (Réseau, Écriture, Push Git, Install).
- **Skills Marketplace.** Utilisation prioritaire des outils dans `./phoenix-agents-marketplace/skills/`.

### 6bis. RÈGLES GIT DE BASE (INITIALISATION & FLUX)
- Avant toute initialisation de projet, l'agent doit demander:
  - le nom du dossier de travail;
  - le mode de dépôt: `public` ou `privé`, valeur par défaut `privé` si aucune réponse.
- Initialisation Git obligatoire:
  - créer/valider un dépôt local (`git init`);
  - créer la branche `main` puis `dev`;
  - basculer sur `dev` pour le travail courant;
  - initialiser le dépôt distant avec la visibilité confirmée, sans décalage depuis l'initialisation locale.
- `commit`:
  - faire un commit local initial d'initialisation;
  - ne jamais demander d'autorisation pour le commit local d'initialisation;
  - ne pas demander d'autorisation pour l'initialisation distante tant que l'utilisateur a validé les paramètres initiaux.
- Intégration:
  - après exécution des tests et validation locale de l'utilisateur, le merge de `dev` vers `main` doit être fait en local puis poussé en distant.
- Aucun commit distant (push final) n'est demandé automatiquement; le propriétaire décide du moment de validation finale.

### 10. PIPELINE D'EXÉCUTION OBLIGATOIRE (TOUTE TÂCHE)
- [OK] Lire le `docs/BACKLOG.md` puis le `docs/checklog.md` avant toute modification.
- [OK] Ajouter la planification du tour dans le `docs/BACKLOG.md` avant tout codage.
- [OK] Faire la validation internet obligatoire (OWASP Top 10, CVE/alerts, analyse des dépôts de référence) AVANT implémentation.
- [OK] Appliquer le TDD avec tests avant d'écrire du code applicatif.
- [OK] Implémenter (non destructif, sidecar uniquement).
- [OK] Exécuter les tests du lot après implémentation.
- [OK] Remplir immédiatement le `docs/checklog.md` après le cycle de codage.
- [OK] Mettre à jour `docs/BACKLOG.md` juste après tests/validation.
- [OK] Remettre un compte-rendu court au propriétaire.

### 11. FICHIERS DE PIPELINE (ORIGINE DU PROJET)
- Garder et lire systématiquement ces fichiers avant toute tâche:
  - `./AGENTS.md`
  - `./AGENTS.override.md`
  - `./INSTRUCTIONS.agent.yaml`
  - `./docs/checklog.md`
  - `./docs/BACKLOG.md`
- Maintenir la cohérence entre eux, sans en créer de nouveaux pour remplacer ces fichiers d'origine.

### 7. SYNCHRONISATION UPSTREAM (PHOENIX-SYNC)
- [OK] **SYNC-AUTO.** Tous les dépôts connectés à un remote font l'objet d'une mise à jour (pull/fetch) automatique 2 fois par jour (Matin/Soir).
- [WARNING] L'agent doit systématiquement vérifier qu'il travaille sur la version la plus récente de l'Upstream avant toute action.

---
[INFO] PhoenixProject : Conception Souveraine, Immutabilité, Auditabilité.
