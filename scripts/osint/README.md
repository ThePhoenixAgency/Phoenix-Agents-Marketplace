# OSINT Toolkit

Created: 2026-02-18
Last Updated: 2026-02-18

## Overview

Suite de 15 modules Python pour l'OSINT professionnel et le Bug Bounty. Chaque module est autonome (CLI) et produit du JSON structure pour le chainage. Le pipeline complet execute tout en sequence.

## Modules

### Reconnaissance Passive

| Module | Description |
|--------|-------------|
| `cert_transparency.py` | Sous-domaines via Certificate Transparency logs (crt.sh) |
| `dns_enum.py` | Records DNS complets + analyse SPF/DMARC/email security |
| `whois_intel.py` | WHOIS lookup + analyse age/registrar/NS/expiry |
| `email_hunter.py` | Pattern discovery + validation MX + HIBP breaches |
| `leak_scanner.py` | Scan repos GitHub pour secrets/credentials/.env |
| `wayback_scanner.py` | Fichiers sensibles historiques + endpoints via Wayback Machine |
| `market_watch.py` | Surveillance grey market (revente non autorisee) |
| `social_profiler.py` | Presence username cross-platform (24 plateformes) |
| `google_dorker.py` | Dorking avance multi-categorie (9 categories) |

### Reconnaissance Active

| Module | Description |
|--------|-------------|
| `deep_scan.py` | Subdomain enum (subfinder) + tech fingerprint (httpx) |
| `nuclei_scanner.py` | Vulnerability scanning template-based (wrapper Nuclei) |
| `shodan_intel.py` | Ports, services, CVEs via API Shodan |

### Threat Intelligence

| Module | Description |
|--------|-------------|
| `threat_feed.py` | Agregation OTX + AbuseIPDB + VirusTotal + scoring |

### Analysis & Reporting

| Module | Description |
|--------|-------------|
| `correlation_engine.py` | Graphe entites/relations inter-sources |
| `report_generator.py` | Rapport structure + risk scoring + recommandations |
| `pipeline.py` | Pipeline complet automatise (tous les modules) |

### Hooks

| Module | Description |
|--------|-------------|
| `on_scan_complete.py` | Notification Discord/fichier post-scan |

## Quick Start

```bash
# Module individuel
python3 scripts/osint/dns_enum.py example.com

# Pipeline complet (tous les modules)
python3 scripts/osint/pipeline.py example.com

# Pipeline avec output custom
python3 scripts/osint/pipeline.py example.com /path/to/output
```

## Dependencies

```
pip install requests beautifulsoup4 dnspython
```

### API Keys (optionnelles, via ENV)

| Variable | Service |
|----------|---------|
| `SHODAN_API_KEY` | Shodan |
| `HIBP_API_KEY` | Have I Been Pwned |
| `GITHUB_TOKEN` | GitHub API (rate limit) |
| `OTX_API_KEY` | AlienVault OTX |
| `ABUSEIPDB_API_KEY` | AbuseIPDB |
| `VIRUSTOTAL_API_KEY` | VirusTotal |
| `DISCORD_WEBHOOK_URL` | Notifications Discord |

### CLI Tools (optionnels)

| Tool | Usage |
|------|-------|
| `subfinder` | Subdomain enumeration |
| `httpx` | HTTP probing |
| `nuclei` | Template-based scanning |
| `whois` | Domain registration |

## Output Format

Tous les modules : JSON sur stdout, erreurs sur stderr avec prefixes `[WARNING]`, `[ERROR]`, `[INFO]`, `[OK]`.
