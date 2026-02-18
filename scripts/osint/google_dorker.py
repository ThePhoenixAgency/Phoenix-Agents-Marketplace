"""
Script: Google Dorker - Advanced Search Engine Dorking
Created: 2026-02-18
Last Updated: 2026-02-18

Moteur de dorking automatise avec categories pre-definies,
rotation de moteurs de recherche, et classification des resultats.
"""

import sys
import json
import time
import random
import urllib.parse

try:
    import requests
    from bs4 import BeautifulSoup
    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
]

DORK_CATEGORIES = {
    "admin_panels": [
        'site:{target} inurl:admin',
        'site:{target} intitle:"login" OR intitle:"sign in"',
        'site:{target} inurl:dashboard',
        'site:{target} inurl:portal',
    ],
    "config_files": [
        'site:{target} filetype:env',
        'site:{target} filetype:yml password',
        'site:{target} filetype:conf',
        'site:{target} filetype:ini',
        'site:{target} filetype:xml password',
    ],
    "database": [
        'site:{target} inurl:phpmyadmin',
        'site:{target} filetype:sql',
        'site:{target} "index of" database',
    ],
    "api_discovery": [
        'site:{target} inurl:api inurl:v1 OR inurl:v2',
        'site:{target} inurl:swagger OR inurl:api-docs',
        'site:{target} inurl:graphql',
        'site:{target} filetype:json api_key OR apiKey',
    ],
    "sensitive_docs": [
        'site:{target} filetype:pdf confidential OR internal',
        'site:{target} filetype:xlsx password',
        'site:{target} filetype:doc restricted',
    ],
    "errors_debug": [
        'site:{target} "stack trace" OR "traceback"',
        'site:{target} "SQL syntax"',
        'site:{target} inurl:debug OR inurl:test',
    ],
    "backups": [
        'site:{target} filetype:bak OR filetype:old',
        'site:{target} filetype:tar.gz OR filetype:zip',
        'site:{target} "index of" backup',
    ],
    "credentials": [
        'site:{target} filetype:log password',
        '"{target}" site:pastebin.com',
        '"{target}" site:trello.com password OR key',
        '"{target}" "BEGIN RSA PRIVATE KEY"',
    ],
    "git_exposure": [
        'site:{target} "index of /" .git',
        'site:{target} inurl:.git/config',
        '"{target}" site:github.com password OR secret OR api_key',
    ],
}


def generate_dorks(target, categories=None):
    """
    Genere les dorks pour une cible.

    Args:
        target: Domaine cible
        categories: Liste de categories (None = toutes)

    Returns:
        list: Dorks generes avec leur categorie
    """
    cats = categories or list(DORK_CATEGORIES.keys())
    dorks = []
    for cat in cats:
        if cat not in DORK_CATEGORIES:
            continue
        for template in DORK_CATEGORIES[cat]:
            dorks.append({
                "category": cat,
                "dork": template.format(target=target),
            })
    return dorks


def search_ddg(dork, max_results=5):
    """
    Execute un dork via DuckDuckGo HTML.

    Args:
        dork: Requete de recherche
        max_results: Nombre max de resultats

    Returns:
        list: Resultats trouves
    """
    if not HAS_DEPS:
        return []

    query = urllib.parse.quote_plus(dork)
    url = f"https://html.duckduckgo.com/html/?q={query}"

    try:
        resp = requests.get(
            url,
            headers={"User-Agent": random.choice(USER_AGENTS)},
            timeout=15,
        )
        if resp.status_code != 200:
            return []

        soup = BeautifulSoup(resp.text, "html.parser")
        results = []
        for res in soup.find_all("div", class_="result")[:max_results]:
            title_tag = res.find("a", class_="result__a")
            snippet_tag = res.find("a", class_="result__snippet")
            if title_tag:
                results.append({
                    "title": title_tag.get_text().strip(),
                    "url": title_tag.get("href", ""),
                    "snippet": snippet_tag.get_text().strip() if snippet_tag else "",
                })
        return results
    except requests.RequestException:
        return []


def classify_severity(category, result_count):
    """Classifie la severite basee sur la categorie et le nombre de resultats."""
    critical_cats = ["credentials", "git_exposure", "config_files"]
    high_cats = ["database", "backups"]
    if category in critical_cats and result_count > 0:
        return "critical"
    if category in high_cats and result_count > 0:
        return "high"
    if result_count > 0:
        return "medium"
    return "info"


def run_dorking(target, categories=None):
    """
    Lance le dorking complet sur une cible.

    Args:
        target: Domaine cible
        categories: Categories a scanner (None = toutes)

    Returns:
        dict: Resultats structures
    """
    print(f"[*] Google Dorker: {target}...", file=sys.stderr)

    dorks = generate_dorks(target, categories)
    all_findings = []
    category_summary = {}

    for dork_entry in dorks:
        cat = dork_entry["category"]
        dork = dork_entry["dork"]

        results = search_ddg(dork)
        severity = classify_severity(cat, len(results))

        for result in results:
            result["category"] = cat
            result["dork"] = dork
            result["severity"] = severity

        all_findings.extend(results)

        if cat not in category_summary:
            category_summary[cat] = {"count": 0, "severity": "info"}
        category_summary[cat]["count"] += len(results)
        if len(results) > 0:
            category_summary[cat]["severity"] = severity

        if results:
            print(f"  [{severity.upper()}] {cat}: {len(results)} results", file=sys.stderr)

        time.sleep(random.uniform(2, 4))

    return {
        "target": target,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "dorks_executed": len(dorks),
        "total_findings": len(all_findings),
        "findings": all_findings,
        "category_summary": category_summary,
        "stats": {
            "dorks": len(dorks),
            "findings": len(all_findings),
            "critical": len([f for f in all_findings if f.get("severity") == "critical"]),
            "high": len([f for f in all_findings if f.get("severity") == "high"]),
            "categories_with_results": len([c for c in category_summary.values() if c["count"] > 0]),
        },
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python3 google_dorker.py <domain> [category1,category2,...]"}))
        sys.exit(1)

    target_domain = sys.argv[1]
    cats = sys.argv[2].split(",") if len(sys.argv) > 2 else None
    data = run_dorking(target_domain, cats)
    print(json.dumps(data, indent=2))
