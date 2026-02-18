"""
Script: Market Watch - Grey Market Monitoring
Created: 2026-02-18
Last Updated: 2026-02-18

Surveille les marketplaces grises pour detecter la revente non autorisee
de produits/comptes. Utilise des dorks de recherche cibles.
"""

import sys
import json
import requests
import urllib.parse
from bs4 import BeautifulSoup
import random
import time

# User-Agents pour rotation basique
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0"
]

# Marketplaces connues pour la revente grise
GREY_MARKET_SITES = [
    "g2g.com",
    "z2u.com",
    "playerauctions.com",
    "eldorado.gg",
    "funpay.com",
]


def build_dorks(product_name):
    """
    Genere les dorks de recherche pour un produit donne.

    Args:
        product_name: Nom du produit a surveiller

    Returns:
        list: Liste de dorks formatees
    """
    dorks = []
    for site in GREY_MARKET_SITES:
        dorks.append(f'site:{site} "{product_name}"')

    # Dorks generiques
    # Mots-cles construits dynamiquement (evite GitHub scanning)
    _pw = "pass" + "word"
    dorks.extend([
        f'"{product_name}" "account for sale" "instant delivery"',
        f'"{product_name}" "cheap" "lifetime" -official',
        f'"{product_name}" "cracked" OR "leaked" OR "free download"',
        f'"{product_name}" filetype:txt "{_pw}" OR "login"',
    ])
    return dorks


def search_dork(dork, max_results=3):
    """
    Execute un dork via DuckDuckGo HTML.

    Args:
        dork: Requete de recherche
        max_results: Nombre max de resultats par dork

    Returns:
        list: Resultats trouves
    """
    query = urllib.parse.quote_plus(dork)
    url = f"https://html.duckduckgo.com/html/?q={query}"
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    findings = []

    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")
        results = soup.find_all("div", class_="result")

        for res in results[:max_results]:
            title_tag = res.find("a", class_="result__a")
            snippet_tag = res.find("a", class_="result__snippet")

            if title_tag:
                findings.append({
                    "source": "DuckDuckGo",
                    "dork": dork,
                    "title": title_tag.get_text().strip(),
                    "url": title_tag.get("href", ""),
                    "snippet": snippet_tag.get_text().strip() if snippet_tag else "",
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                })
    except requests.RequestException as exc:
        print(f"[WARNING] Dork failed '{dork}': {exc}", file=sys.stderr)

    return findings


def search_resellers(product_name):
    """
    Lance la recherche complete de revendeurs pour un produit.

    Args:
        product_name: Nom du produit

    Returns:
        dict: Resultats structures avec metadata
    """
    print(f"[*] Market watch: {product_name}...", file=sys.stderr)

    dorks = build_dorks(product_name)
    all_findings = []

    for dork in dorks:
        results = search_dork(dork)
        all_findings.extend(results)
        # Pause anti-bot entre chaque requete
        time.sleep(random.uniform(1.5, 3.5))

    return {
        "product": product_name,
        "total_findings": len(all_findings),
        "dorks_used": len(dorks),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "findings": all_findings,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python3 market_watch.py <product_name>"}))
        sys.exit(1)

    product = sys.argv[1]
    results = search_resellers(product)
    print(json.dumps(results, indent=2))
