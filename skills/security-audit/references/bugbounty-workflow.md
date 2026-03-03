# Bug Bounty — Workflow et Bonnes Pratiques

## Avant de Commencer

1. **Lire le programme** : scope, exclusions, recompenses, regles
2. **Verifier le scope** : domaines, IPs, applications inclus/exclus
3. **Confirmer l'autorisation** : ne tester QUE ce qui est dans le scope
4. **Ouvrir un journal** : `private/securite/AUDIT_JOURNAL.md`

Plateformes principales : HackerOne, Bugcrowd, Intigriti, Synack, YesWeHack

## Methodologie

### 1. Reconnaissance (voir osint-recon.md)
- Enumeration de sous-domaines
- Cartographie des endpoints
- Identification des technologies

### 2. Priorisation des Cibles

Priorite haute :
- Authentification et gestion de session
- Fonctions de paiement
- Upload de fichiers
- Endpoints API avec donnees sensibles
- Fonctions admin / privilegiees

### 3. Tests Adaptes au Scope

**Web Application** : voir `references/pentest-web.md`

**API REST** :
```
- Enumeration des endpoints (Swagger, WSDL, OpenAPI)
- Mass assignment : POST /api/user avec champs admin
- Rate limiting : boucle de requetes, enumeration
- BOLA/IDOR : modifier les IDs dans les requetes
- Verb tampering : PUT/DELETE sur ressources non prevues
```

**Mobile (si dans scope)** :
```
- Extraction de l'APK/IPA
- Recherche de secrets dans le code (strings, config)
- Interception du trafic (proxy Burp/mitmproxy)
- Validation cote serveur uniquement (pas client)
```

## Severity et Recompenses Typiques

| Severite | Exemple | Fourchette (USD) |
|----------|---------|-----------------|
| CRITICAL | RCE, SQLi sur prod, Account Takeover | 5 000 – 50 000+ |
| HIGH | SSRF interne, Privilege Escalation | 1 000 – 10 000 |
| MEDIUM | XSS stocke, CSRF sensible, IDOR | 300 – 2 000 |
| LOW | Info disclosure, open redirect | 50 – 500 |

## Redaction du Rapport

Structure obligatoire :

```markdown
## [SEVERITY] Titre court et explicite

**Plateforme** : HackerOne / Bugcrowd / ...
**Programme** : [Nom du programme]
**Date** : YYYY-MM-DD

### Synthese
[1–2 phrases : quoi, impact immédiat]

### Etapes de Reproduction
1. Aller sur https://target.com/endpoint
2. Entrer le payload suivant : [payload exact]
3. Observer : [comportement attendu]

### Impact
[Impact concret : donnees exposees, comptes compromis, etc.]

### Preuve (PoC)
[Screenshots, videos, output de commandes — OBLIGATOIRE]

### Remediation Recommandee
[Action precise : patch, validation, configuration]

### CVSS v3.1
Score : X.X
Vecteur : CVSS:3.1/AV:N/AC:L/...
```

## Regles d'Or

- Ne jamais exfiltrer de donnees reelles (captures d'ecran suffisent)
- Ne jamais modifier ou supprimer des donnees de production
- Stopper le test si decouverte d'une donnee sensible reelle
- Divulgation responsable : signaler au programme AVANT toute publication
- Delai de divulgation : respecter le delai du programme (generalement 90 jours)

## Outils Utiles

```bash
# Fuzzing endpoints
ffuf -w wordlist.txt -u https://target.com/FUZZ

# Scan de sous-domaines (passif)
subfinder -d target.com

# HTTP probing
httpx -l domains.txt -status-code -title

# Capture trafic
# Burp Suite (proxy local 127.0.0.1:8080)
```
