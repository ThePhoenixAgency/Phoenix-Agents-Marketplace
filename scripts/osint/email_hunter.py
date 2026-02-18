"""
Script: Email Hunter - Email Pattern Discovery & Validation
Created: 2026-02-18
Last Updated: 2026-02-18

Decouverte de patterns d'email d'un domaine, validation MX,
et verification de breaches via Have I Been Pwned.
"""

import sys
import json
import time
import socket
import os

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


# Patterns d'email courants en entreprise
EMAIL_PATTERNS = [
    "{first}.{last}",
    "{first}{last}",
    "{f}{last}",
    "{first}_{last}",
    "{first}-{last}",
    "{first}",
    "{last}.{first}",
    "{f}.{last}",
    "{first}.{l}",
]

# API Key HIBP (optionnelle, via ENV)
HIBP_API_KEY = os.getenv("HIBP_API_KEY", "")


def generate_email_variants(first_name, last_name, domain):
    """
    Genere les variantes d'email possibles pour un nom.

    Args:
        first_name: Prenom
        last_name: Nom de famille
        domain: Domaine email

    Returns:
        list: Emails possibles
    """
    first = first_name.lower().strip()
    last = last_name.lower().strip()
    f = first[0] if first else ""
    l = last[0] if last else ""

    emails = []
    for pattern in EMAIL_PATTERNS:
        email = pattern.format(first=first, last=last, f=f, l=l)
        emails.append(f"{email}@{domain}")

    return emails


def verify_mx(domain):
    """
    Verifie si un domaine a des records MX valides.

    Args:
        domain: Domaine a verifier

    Returns:
        dict: Resultats MX
    """
    try:
        import dns.resolver
        answers = dns.resolver.resolve(domain, "MX")
        mx_records = []
        for answer in answers:
            mx_records.append({
                "priority": answer.preference,
                "exchange": str(answer.exchange),
            })
        return {"valid": True, "records": sorted(mx_records, key=lambda x: x["priority"])}
    except ImportError:
        # Fallback sans dnspython
        try:
            socket.getaddrinfo(f"mail.{domain}", 25)
            return {"valid": True, "records": [{"note": "fallback check only"}]}
        except socket.gaierror:
            return {"valid": False, "records": []}
    except Exception:
        return {"valid": False, "records": []}


def check_hibp(email):
    """
    Verifie si un email a ete compromis via Have I Been Pwned.
    Necessite une API key (payante).

    Args:
        email: Email a verifier

    Returns:
        dict: Resultats de breach
    """
    if not HIBP_API_KEY or not HAS_REQUESTS:
        return {"checked": False, "reason": "No HIBP API key or requests not installed"}

    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
    headers = {
        "hibp-api-key": HIBP_API_KEY,
        "User-Agent": "OSINT-Toolkit/1.0",
    }

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            breaches = resp.json()
            return {
                "checked": True,
                "breached": True,
                "breach_count": len(breaches),
                "breaches": [
                    {
                        "name": b.get("Name", ""),
                        "date": b.get("BreachDate", ""),
                        "data_classes": b.get("DataClasses", []),
                    }
                    for b in breaches[:10]
                ],
            }
        elif resp.status_code == 404:
            return {"checked": True, "breached": False, "breach_count": 0}
        else:
            return {"checked": False, "reason": f"HTTP {resp.status_code}"}
    except requests.RequestException as exc:
        return {"checked": False, "reason": str(exc)}


def discover_emails_from_web(domain):
    """
    Tente de decouvrir des emails via Google Dorking.

    Args:
        domain: Domaine cible

    Returns:
        list: Emails trouves
    """
    if not HAS_REQUESTS:
        return []

    import urllib.parse
    import random
    from bs4 import BeautifulSoup

    dorks = [
        f'"@{domain}" email',
        f'site:linkedin.com "@{domain}"',
        f'site:github.com "@{domain}"',
    ]

    found_emails = set()
    email_regex = rf"[a-zA-Z0-9._%+-]+@{domain.replace('.', '[.]')}"

    for dork in dorks:
        query = urllib.parse.quote_plus(dork)
        url = f"https://html.duckduckgo.com/html/?q={query}"
        try:
            resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            if resp.status_code == 200:
                # Chercher les emails dans le texte brut
                matches = set(re.findall(email_regex, resp.text, re.IGNORECASE))
                found_emails.update(matches)
            time.sleep(random.uniform(2, 4))
        except Exception:
            continue

    return sorted(found_emails)


def email_hunt(domain, known_names=None):
    """
    Recherche complete d'emails pour un domaine.

    Args:
        domain: Domaine cible
        known_names: Liste optionnelle de tuples (prenom, nom)

    Returns:
        dict: Resultats structures
    """
    print(f"[*] Email Hunter: {domain}...", file=sys.stderr)

    # Verification MX
    mx_result = verify_mx(domain)

    # Emails generes depuis des noms connus
    generated = []
    if known_names:
        for first, last in known_names:
            variants = generate_email_variants(first, last, domain)
            generated.extend(variants)

    # Emails decouverts via web
    try:
        import re
        discovered = discover_emails_from_web(domain)
    except Exception:
        discovered = []

    # Deduplication
    all_emails = sorted(set(generated + discovered))

    # Breach check sur les emails decouverts (rate limited)
    breach_results = {}
    for email in discovered[:5]:  # Limiter les appels HIBP
        breach_results[email] = check_hibp(email)
        time.sleep(1.5)  # HIBP rate limit

    return {
        "target": domain,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "mx_valid": mx_result.get("valid", False),
        "mx_records": mx_result.get("records", []),
        "email_patterns": EMAIL_PATTERNS,
        "generated_emails": generated,
        "discovered_emails": discovered,
        "all_unique_emails": all_emails,
        "breach_results": breach_results,
        "stats": {
            "mx_valid": mx_result.get("valid", False),
            "generated_count": len(generated),
            "discovered_count": len(discovered),
            "total_unique": len(all_emails),
            "breached_count": sum(1 for b in breach_results.values() if b.get("breached")),
        },
    }


if __name__ == "__main__":
    import re

    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python3 email_hunter.py <domain> [first:last,first:last,...]"}))
        sys.exit(1)

    target_domain = sys.argv[1]
    names = None
    if len(sys.argv) > 2:
        names = [tuple(n.split(":")) for n in sys.argv[2].split(",")]

    data = email_hunt(target_domain, names)
    print(json.dumps(data, indent=2))
