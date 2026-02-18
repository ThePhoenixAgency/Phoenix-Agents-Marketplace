---
name: osint-recon
description: Full passive reconnaissance workflow using OSINT toolkit
---

# OSINT Reconnaissance Skill

## When to Use

When performing passive reconnaissance on a target domain, organization, or individual for Bug Bounty or security assessment.

## Prerequisites

- Python 3.9+
- `requests`, `beautifulsoup4`, `dnspython` installed
- Optional API keys: SHODAN_API_KEY, HIBP_API_KEY, GITHUB_TOKEN

## Steps

### 1. Certificate Transparency

```bash
python3 scripts/osint/cert_transparency.py <domain> > /tmp/osint_ct.json
```

Discovers subdomains via CT logs. Fully passive, no target interaction.

### 2. DNS Enumeration

```bash
python3 scripts/osint/dns_enum.py <domain> > /tmp/osint_dns.json
```

Full DNS records + SPF/DMARC email security analysis.

### 3. WHOIS Intelligence

```bash
python3 scripts/osint/whois_intel.py <domain> > /tmp/osint_whois.json
```

Domain age, registrar, NS provider, expiry risk.

### 4. Email Discovery

```bash
python3 scripts/osint/email_hunter.py <domain> > /tmp/osint_email.json
```

Pattern discovery, MX validation, HIBP breach check.

### 5. Leak Scanning

```bash
python3 scripts/osint/leak_scanner.py <domain> > /tmp/osint_leaks.json
```

GitHub public repos for secrets, .env, credentials.

### 6. Wayback Analysis

```bash
python3 scripts/osint/wayback_scanner.py <domain> > /tmp/osint_wayback.json
```

Historical pages, removed content, sensitive files.

### 7. Shodan Intelligence

```bash
python3 scripts/osint/shodan_intel.py <domain> > /tmp/osint_shodan.json
```

Open ports, services, known CVEs. Requires SHODAN_API_KEY.

### 8. Threat Intelligence

```bash
python3 scripts/osint/threat_feed.py <domain> domain > /tmp/osint_threat.json
```

OTX + AbuseIPDB + VirusTotal aggregation.

### 9. Correlation

```bash
python3 scripts/osint/correlation_engine.py /tmp/osint_*.json > /tmp/osint_corr.json
```

Cross-reference all findings, build entity graph.

### 10. Report Generation

```bash
python3 scripts/osint/report_generator.py <domain> /tmp/osint_*.json > /tmp/osint_report.json
```

Risk scoring, executive summary, actionable recommendations.

## Output

All modules output JSON to stdout. Chain them via files or pipes.
