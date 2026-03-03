---
name: check-deps
description: Verification des dependances vulnerables (npm audit, pip-audit, composer audit, bundle audit, govulncheck)
argument-hint: "[path]"
allowed-tools: ["Read", "Glob", "Grep", "Bash", "Write", "WebSearch"]
---

# /security-audit:check-deps

Verification des dependances vulnerables selon l'ecosysteme detecte.

## Execution

1. Identifier la cible (argument ou repertoire courant)
2. Detecter l'ecosysteme en cherchant les fichiers manifestes :

| Fichier | Ecosysteme | Commande |
|---------|------------|----------|
| `package.json` | Node.js | `npm audit --json` |
| `requirements.txt` / `pyproject.toml` | Python | `pip-audit --format json` ou `safety check --json` |
| `composer.json` | PHP | `composer audit` |
| `Gemfile` | Ruby | `bundle audit` |
| `go.mod` | Go | `govulncheck ./...` |
| `Cargo.toml` | Rust | `cargo audit` |
| `pom.xml` / `build.gradle` | Java | `mvn dependency-check:check` |

3. Pour chaque dependance vulnerable trouvee :
   - Rechercher le CVE sur NVD : `site:nvd.nist.gov "[CVE-ID]"`
   - Obtenir le score CVSS et la severite
   - Identifier la version corrigee

4. Generer un rapport dans `docs/private/security/DEPS_AUDIT.md` :
```markdown
# Audit des Dependances
**Date**: YYYY-MM-DD
**Ecosysteme**: [detected]

## Resume
| Severite | Nombre |
|----------|--------|
| CRITIQUE | X |
| HAUTE    | X |
| MOYENNE  | X |
| BASSE    | X |

## Vulnerabilites
### [CRITIQUE] [package@version]
- **CVE**: CVE-YYYY-XXXXX
- **CVSS**: X.X
- **Description**: ...
- **Version corrigee**: X.X.X
- **Action**: `npm install package@X.X.X`
```

5. S'assurer que `docs/private/` est dans `.gitignore`
6. Ajouter une note dans `/private/securite/AUDIT_JOURNAL.md` mentionnant que l'audit des dépendances a été généré et que le bloc reflète l'étape (pas de duplication).
