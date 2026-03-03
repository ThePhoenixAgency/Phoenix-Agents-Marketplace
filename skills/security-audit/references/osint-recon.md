# OSINT & Reconnaissance Passive

## Principes

- Reconnaissance PASSIVE uniquement : aucune interaction directe avec la cible
- Toutes les sources sont publiques et legales
- Documenter chaque source et timestamp
- Ne jamais depasser le scope defini

## Enumeration DNS

```bash
# Sous-domaines (passif)
# Via crt.sh (Certificate Transparency)
WebFetch: https://crt.sh/?q=%.[target.com]&output=json

# Via dnsdumpster (outil en ligne)
WebFetch: https://dnsdumpster.com

# Transfert de zone (si autorise)
dig axfr @nameserver target.com

# Reverse DNS
host [IP] || nslookup [IP]
```

## WHOIS & Enregistrement

```bash
whois target.com
whois [IP]
# Informations : registrar, dates, nameservers, contacts
```

## Google Dorks

```
site:target.com filetype:pdf
site:target.com inurl:admin
site:target.com intitle:"index of"
site:target.com ext:env OR ext:config OR ext:sql
"target.com" password OR secret OR api_key
site:github.com "target.com" token
site:pastebin.com "target.com"
```

## Shodan & Censys

```
# Shodan (requires API key)
org:"target company"
hostname:target.com
ssl:"target.com"
http.title:"target"

# Censys
parsed.names: target.com
parsed.subject.organization: "Company Name"
```

## Fuites de Donnees

Sources a verifier :
- **Have I Been Pwned** : `https://haveibeenpwned.com/api/v3/breachedaccount/{email}`
- **DeHashed** : recherche email/domaine
- **LeakCheck** : credentials compromis
- **GitHub** : secrets commites (chercher avec dork)
- **Pastebin** : `site:pastebin.com "target.com"`

## Profil Technique de la Cible

```bash
# Headers HTTP (fingerprinting)
curl -I https://target.com

# Technologies (BuiltWith, Wappalyzer)
WebFetch: https://builtwith.com/target.com

# ASN et CIDR
# Via Hurricane Electric
WebFetch: https://bgp.he.net/dns/target.com

# Emails
# Via Hunter.io (si disponible)
WebFetch: https://api.hunter.io/v2/domain-search?domain=target.com&api_key=KEY
```

## Archive Web (Wayback Machine)

```
# Pages historiques
WebFetch: https://web.archive.org/web/*/target.com/*

# Endpoints anciens potentiellement toujours actifs
# Chercher : /admin, /api, /backup, /config, /test

# CDX API pour inventaire URLs
WebFetch: http://web.archive.org/cdx/search/cdx?url=target.com/*&output=json&fl=original&collapse=urlkey
```

## Metadata de Fichiers

```bash
# PDF, DOCX, images — exifdata
exiftool document.pdf
# Infos : auteur, logiciel, date, chemin interne, username

# Images
exiftool photo.jpg | grep -E "GPS|Author|Creator|Software"
```

## Reseaux Sociaux et OSINT Personnel

- LinkedIn : employes, technologies utilisees, organigramme
- Twitter/X : annonces techniques, erreurs exposees
- GitHub : code source, historique de commits, secrets commites
- Glassdoor : tech stack mentionnee dans les offres d'emploi

## Rapport OSINT

```markdown
## Synthese OSINT — [TARGET]
Date : YYYY-MM-DD

### Infrastructure
- Domaines trouves : [liste]
- IPs/CIDRs : [liste]
- Technologies identifiees : [stack]
- Services exposes : [ports/services]

### Fuites detectees
- Credentials compromis : [oui/non + source]
- Secrets dans repos publics : [oui/non + URL]
- Documents sensibles indexees : [liste]

### Surface d'attaque
[Evaluation de la surface exposee]
```
