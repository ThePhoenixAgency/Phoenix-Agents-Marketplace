"""
Script: Wayback Scanner - Historical Web Analysis
Created: 2026-02-18
Last Updated: 2026-02-18

Interroge la Wayback Machine pour decouvrir pages supprimees,
anciens endpoints, fichiers sensibles historiques.
"""

import sys
import json
import time
import re

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

SENSITIVE_EXT = [
    ".env", ".bak", ".sql", ".dump", ".log", ".conf",
    ".key", ".pem", ".htpasswd", ".git/config",
    "wp-config.php", "database.yml", ".old", ".backup",
]

INTERESTING_PATHS = [
    r"/admin", r"/api/", r"/debug", r"/staging",
    r"/internal", r"/backup", r"/phpmyadmin",
    r"\.git/", r"/swagger", r"/graphql", r"/console",
]


def query_cdx(domain, limit=500):
    """Interroge l'API CDX Wayback Machine."""
    if not HAS_REQUESTS:
        return []
    url = (
        f"http://web.archive.org/cdx/search/cdx"
        f"?url=*.{domain}/*&output=json&collapse=urlkey"
        f"&limit={limit}&fl=timestamp,original,statuscode"
    )
    try:
        resp = requests.get(url, timeout=30)
        if resp.status_code != 200:
            return []
        data = resp.json()
        if not data:
            return []
        headers = data[0]
        return [dict(zip(headers, row)) for row in data[1:]]
    except Exception as exc:
        print(f"[WARNING] CDX failed: {exc}", file=sys.stderr)
        return []


def find_sensitive(urls):
    """Filtre les URLs sensibles."""
    findings = []
    seen = set()
    for entry in urls:
        url = entry.get("original", "")
        if url in seen:
            continue
        seen.add(url)
        for ext in SENSITIVE_EXT:
            if ext in url.lower():
                sev = "critical" if ext in [".env", ".key", ".pem", ".htpasswd"] else "high"
                findings.append({"url": url, "pattern": ext, "severity": sev,
                                 "timestamp": entry.get("timestamp", "")})
                break
    return findings


def find_endpoints(urls):
    """Identifie endpoints interessants."""
    findings = []
    seen = set()
    for entry in urls:
        url = entry.get("original", "")
        if url in seen:
            continue
        seen.add(url)
        for pat in INTERESTING_PATHS:
            if re.search(pat, url, re.IGNORECASE):
                findings.append({"url": url, "pattern": pat,
                                 "timestamp": entry.get("timestamp", "")})
                break
    return findings[:50]


def wayback_scan(domain):
    """Scan complet Wayback Machine."""
    print(f"[*] Wayback Scanner: {domain}...", file=sys.stderr)
    urls = query_cdx(domain)
    sensitive = find_sensitive(urls)
    endpoints = find_endpoints(urls)
    return {
        "target": domain,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "total_archived": len(urls),
        "sensitive_files": sensitive,
        "interesting_endpoints": endpoints,
        "stats": {
            "total_urls": len(urls),
            "sensitive": len(sensitive),
            "endpoints": len(endpoints),
            "critical": len([f for f in sensitive if f.get("severity") == "critical"]),
        },
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python3 wayback_scanner.py <domain>"}))
        sys.exit(1)
    data = wayback_scan(sys.argv[1])
    print(json.dumps(data, indent=2))
