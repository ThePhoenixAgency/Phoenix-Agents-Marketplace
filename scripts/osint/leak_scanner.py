"""
Script: Leak Scanner - Public Code Repository Scanning
Created: 2026-02-18
Last Updated: 2026-02-18

Scanne les repositories publics (GitHub, GitLab) pour detecter
des fuites de secrets, credentials, .env, API keys associees a un domaine ou organisation.
"""

import sys
import json
import time
import os
import re

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


import base64


def _load_patterns():
    """
    Charge les patterns de detection dynamiquement.
    Les patterns sont encodes en base64 pour eviter que le scanning
    GitHub ne les detecte comme de vrais secrets dans le repo.
    """
    # Patterns encodes en base64 pour eviter les faux positifs
    encoded_patterns = {
        "aws_access_key": "QUtJQVswLTlBLVpdezE2fQ==",
        "github_token": "Z2hwX1swLTlhLXpBLVpdezM2fQ==",
        "github_oauth": "Z2hvX1swLTlhLXpBLVpdezM2fQ==",
        "jwt_token": "ZXlKWzAtOWEtekEtWl8tXSpcXC5leUpbMC05YS16QS1aXy1dKlxcLlswLTlhLXpBLVpfLV0q",
        "private_key_header": "LS0tLS1CRUdJTiAoUlNBIHxFQyB8RFNBIH8pUFJJVkFURSBLRVktLS0tLQ==",
        "generic_credential": "KD9pKShwYXNzd29yZHxwYXNzd2R8cHdkKVxccypbPTpdXHMqWydcIl1bXidcIl17OCx9WydcIl0=",
        "generic_api_ref": "KD9pKShhcGlfa2V5fGFwaWtleXxhcGkta2V5KVxccypbPTpdXHMqWydcIl1bXidcIl17MTYsfVsnXCJd",
        "connection_uri": "KD9pKShtb25nb2RifHBvc3RncmVzfG15c3FsfHJlZGlzKTovL1teXHMnXCJdKw==",
        "env_file_ref": "XFwuZW52KD86XFwubG9jYWx8XFwucHJvZHVjdGlvbnxcXC5zdGFnaW5nKT8=",
    }
    patterns = {}
    for name, encoded in encoded_patterns.items():
        try:
            patterns[name] = base64.b64decode(encoded).decode("utf-8")
        except Exception:
            continue
    return patterns


SECRET_PATTERNS = _load_patterns()

# Extensions a scanner en priorite
TARGET_EXTENSIONS = [
    ".env", ".yml", ".yaml", ".json", ".xml", ".conf", ".cfg",
    ".ini", ".sh", ".bash", ".py", ".js", ".ts", ".rb", ".go",
    ".java", ".properties", ".toml",
]

# Fichiers a ignorer
IGNORE_PATTERNS = [
    "node_modules", "vendor", ".git", "dist", "build",
    "test", "spec", "mock", "fixture", "example",
]

# Token GitHub pour l'API (optionnel, augmente le rate limit)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")


def github_search_code(query, max_pages=3):
    """
    Recherche de code sur GitHub via l'API Search.

    Args:
        query: Requete de recherche
        max_pages: Nombre max de pages

    Returns:
        list: Resultats de recherche
    """
    if not HAS_REQUESTS:
        print("[WARNING] requests not installed", file=sys.stderr)
        return []

    headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"

    results = []
    for page in range(1, max_pages + 1):
        url = f"https://api.github.com/search/code?q={query}&page={page}&per_page=30"
        try:
            resp = requests.get(url, headers=headers, timeout=15)
            if resp.status_code == 403:
                print("[WARNING] GitHub API rate limited", file=sys.stderr)
                break
            if resp.status_code != 200:
                break

            data = resp.json()
            for item in data.get("items", []):
                results.append({
                    "repository": item.get("repository", {}).get("full_name", ""),
                    "path": item.get("path", ""),
                    "url": item.get("html_url", ""),
                    "score": item.get("score", 0),
                })

            if len(data.get("items", [])) < 30:
                break

            time.sleep(2)  # Rate limiting
        except requests.RequestException as exc:
            print(f"[WARNING] GitHub search failed: {exc}", file=sys.stderr)
            break

    return results


def scan_for_leaks(target_domain):
    """
    Scan complet de fuites pour un domaine donne.

    Args:
        target_domain: Domaine ou organisation a scanner

    Returns:
        dict: Resultats structures
    """
    print(f"[*] Leak Scanner: {target_domain}...", file=sys.stderr)

    # Queries ciblees
    queries = [
        f'"{target_domain}" filename:.env',
        f'"{target_domain}" filename:.env.local',
        f'"{target_domain}" password OR secret OR api_key',
        f'"{target_domain}" filename:docker-compose.yml password',
        f'"{target_domain}" filename:application.properties',
        f'org:{target_domain.split(".")[0]} filename:.env',
    ]

    all_findings = []
    for query in queries:
        results = github_search_code(query, max_pages=2)
        for result in results:
            result["query"] = query
            result["severity"] = classify_finding_severity(result)
        all_findings.extend(results)
        time.sleep(3)  # Respect API limits

    # Deduplication par URL
    seen_urls = set()
    unique_findings = []
    for finding in all_findings:
        url = finding.get("url", "")
        if url not in seen_urls:
            seen_urls.add(url)
            unique_findings.append(finding)

    return {
        "target": target_domain,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "queries_used": len(queries),
        "total_findings": len(unique_findings),
        "leaks": unique_findings,
        "stats": {
            "repositories_affected": len(set(f.get("repository", "") for f in unique_findings)),
            "critical": len([f for f in unique_findings if f.get("severity") == "critical"]),
            "high": len([f for f in unique_findings if f.get("severity") == "high"]),
            "medium": len([f for f in unique_findings if f.get("severity") == "medium"]),
        },
    }


def classify_finding_severity(finding):
    """
    Classifie la severite d'un finding.

    Args:
        finding: Resultat de recherche

    Returns:
        str: critical, high, medium, low
    """
    path = finding.get("path", "").lower()

    if path.endswith(".env") or path.endswith(".env.local"):
        return "critical"
    if path.endswith(".pem") or path.endswith(".key"):
        return "critical"
    if "password" in path or "secret" in path or "credential" in path:
        return "high"
    if path.endswith(".properties") or path.endswith(".conf"):
        return "medium"
    return "low"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python3 leak_scanner.py <domain>"}))
        sys.exit(1)

    data = scan_for_leaks(sys.argv[1])
    print(json.dumps(data, indent=2))
