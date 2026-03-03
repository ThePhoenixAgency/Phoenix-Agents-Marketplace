# Threat Modeling — Modelisation de Menaces

## Quand l'Utiliser

- Nouveau systeme en conception
- Ajout d'une fonctionnalite sensible (auth, paiements, upload)
- Audit de securite architecture
- Revue pre-production

## Methode STRIDE

| Menace | Description | Exemple |
|--------|-------------|---------|
| **S**poofing | Usurpation d'identite | Faux token JWT, IP spoofing |
| **T**ampering | Modification de donnees | Alteration requete, injection SQL |
| **R**epudiation | Deni d'action | Absence de logs, logs falsifiables |
| **I**nformation Disclosure | Fuite d'info | Erreurs verbeux, logs avec secrets |
| **D**enial of Service | Indisponibilite | Rate limiting absent, boucle infinie |
| **E**levation of Privilege | Escalade de droits | IDOR, SSRF vers services internes |

## Processus

### 1. Decomposer le Systeme

Identifier :
- **Assets** : donnees sensibles, services critiques, cles
- **Points d'entree** : APIs publiques, formulaires, fichiers uploadables
- **Limites de confiance** : frontiere internet/intranet, user/admin
- **Composants** : DB, cache, files queues, services tiers

Diagramme minimal :
```
[Utilisateur] → [Load Balancer] → [API] → [DB]
                                    ↓
                               [File Storage]
                                    ↓
                              [Service Tiers]
```

### 2. Identifier les Menaces (STRIDE)

Pour chaque composant et chaque flux de donnees :
```
Composant : API d'authentification
Flux : POST /auth/login (user → API → DB)

Menaces :
- S : Credential stuffing, faux tokens
- T : SQL injection dans username/password
- R : Absence de log des echecs de connexion
- I : Message d'erreur different si user inexistant
- D : Pas de rate limiting sur les tentatives
- E : Token avec privileges eleves accessible
```

### 3. Evaluer et Prioriser

```
Pour chaque menace :
Probabilite (P) : 1 (faible) a 5 (eleve)
Impact (I) : 1 (faible) a 5 (critique)
Score = P * I → prioritiser les scores > 15
```

### 4. Contre-Mesures

| Menace | Contre-mesure |
|--------|---------------|
| Spoofing | MFA, certificats, validation stricte des tokens |
| Tampering | Validation entrees, prepared statements, signatures HMAC |
| Repudiation | Logs immutables (append-only), audit trail |
| Info Disclosure | Erreurs generiques, masquage des donnees sensibles |
| DoS | Rate limiting, CAPTCHA, circuit breakers |
| Privilege Escalation | RBAC strict, moindre privilege, separation des roles |

## Rapport Threat Model

```markdown
## Threat Model — [SYSTEME]
Date : YYYY-MM-DD
Version : X.X

### Perimetre
[Description du systeme analyse]

### Assets Critiques
| Asset | Sensibilite | Proprietaire |
|-------|-------------|--------------|
| Base users | CRITIQUE | DBA |

### Limites de Confiance
[Diagramme textuel des frontieres]

### Menaces Identifiees

#### [STRIDE-ID] Titre de la menace
- **Categorie STRIDE** : [S/T/R/I/D/E]
- **Composant** : [API auth / DB / ...]
- **Probabilite** : X/5
- **Impact** : X/5
- **Score** : X
- **Description** : [scenario d'attaque]
- **Contre-mesure** : [action concrete]
- **Statut** : OUVERT / EN COURS / RESOLU

### Plan d'Action Prioritaire
1. [Score le plus eleve]
2. ...
```

## Outils de Support

- **OWASP Threat Dragon** : modelisation graphique (open source)
- **Microsoft Threat Modeling Tool** : templates STRIDE
- **draw.io** : diagrammes d'architecture manuels
- **MITRE ATT&CK** : catalogue de techniques d'attaque reelles
