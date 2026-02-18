"""
Script: WHOIS Intel - Domain Registration Intelligence
Created: 2026-02-18
Last Updated: 2026-02-18

WHOIS lookup avec analyse de patterns : registrant, dates,
correlation entre domaines lies au meme proprietaire.
"""

import sys
import json
import time
import subprocess


def whois_lookup(domain):
    """
    Execute un WHOIS lookup via la commande systeme.

    Args:
        domain: Domaine cible

    Returns:
        dict: Donnees WHOIS parsees
    """
    try:
        result = subprocess.run(
            ["whois", domain],
            capture_output=True, text=True, timeout=15
        )
        raw = result.stdout
    except (subprocess.TimeoutExpired, FileNotFoundError) as exc:
        return {"error": str(exc), "raw": ""}

    return parse_whois(raw, domain)


def parse_whois(raw_text, domain):
    """
    Parse la sortie brute WHOIS en structure exploitable.

    Args:
        raw_text: Texte brut du WHOIS
        domain: Domaine original

    Returns:
        dict: Donnees structurees
    """
    data = {
        "domain": domain,
        "registrar": "",
        "registrant_org": "",
        "registrant_country": "",
        "creation_date": "",
        "expiry_date": "",
        "updated_date": "",
        "name_servers": [],
        "status": [],
        "dnssec": "",
        "raw": raw_text[:3000],  # Limiter la taille
    }

    field_map = {
        "registrar:": "registrar",
        "registrant organization:": "registrant_org",
        "registrant country:": "registrant_country",
        "creation date:": "creation_date",
        "registry expiry date:": "expiry_date",
        "updated date:": "updated_date",
        "dnssec:": "dnssec",
    }

    for line in raw_text.split("\n"):
        line_lower = line.strip().lower()

        for pattern, field in field_map.items():
            if line_lower.startswith(pattern):
                value = line.split(":", 1)[1].strip()
                if not data[field]:  # Premier match
                    data[field] = value

        if line_lower.startswith("name server:"):
            ns = line.split(":", 1)[1].strip().lower()
            if ns and ns not in data["name_servers"]:
                data["name_servers"].append(ns)

        if line_lower.startswith("domain status:"):
            status = line.split(":", 1)[1].strip().split()[0]
            if status and status not in data["status"]:
                data["status"].append(status)

    return data


def analyze_whois(whois_data):
    """
    Analyse les donnees WHOIS pour extraire des insights.

    Args:
        whois_data: Donnees WHOIS parsees

    Returns:
        dict: Analyse
    """
    insights = []
    risk_score = 0

    # Age du domaine
    creation = whois_data.get("creation_date", "")
    if creation:
        try:
            from datetime import datetime
            created = datetime.fromisoformat(creation.replace("Z", "+00:00"))
            age_days = (datetime.now(created.tzinfo) - created).days
            if age_days < 90:
                insights.append("[WARNING] Domaine tres recent (< 90 jours)")
                risk_score += 30
            elif age_days < 365:
                insights.append("[INFO] Domaine recent (< 1 an)")
                risk_score += 10
        except (ValueError, TypeError):
            pass

    # Privacy guard
    registrant = whois_data.get("registrant_org", "").lower()
    privacy_indicators = ["privacy", "proxy", "redacted", "data protected", "withheld"]
    if any(ind in registrant for ind in privacy_indicators):
        insights.append("[INFO] WHOIS privacy/proxy active")
    elif not registrant:
        insights.append("[INFO] Registrant organization vide")

    # Nameservers
    ns = whois_data.get("name_servers", [])
    ns_providers = set()
    for nameserver in ns:
        if "cloudflare" in nameserver:
            ns_providers.add("Cloudflare")
        elif "awsdns" in nameserver:
            ns_providers.add("AWS Route53")
        elif "google" in nameserver:
            ns_providers.add("Google Cloud DNS")
        elif "azure" in nameserver:
            ns_providers.add("Azure DNS")
        elif "ns1" in nameserver or "ns2" in nameserver:
            ns_providers.add("NS1")
    if ns_providers:
        insights.append(f"[INFO] DNS Provider(s): {', '.join(ns_providers)}")

    # Expiry
    expiry = whois_data.get("expiry_date", "")
    if expiry:
        try:
            from datetime import datetime
            exp = datetime.fromisoformat(expiry.replace("Z", "+00:00"))
            days_left = (exp - datetime.now(exp.tzinfo)).days
            if days_left < 30:
                insights.append("[CRITICAL] Domaine expire dans < 30 jours")
                risk_score += 40
            elif days_left < 90:
                insights.append("[WARNING] Domaine expire dans < 90 jours")
                risk_score += 15
        except (ValueError, TypeError):
            pass

    return {
        "insights": insights,
        "risk_score": min(risk_score, 100),
        "ns_providers": list(ns_providers) if ns_providers else [],
    }


def whois_scan(domain):
    """
    Scan WHOIS complet avec analyse.

    Args:
        domain: Domaine cible

    Returns:
        dict: Resultats structures
    """
    print(f"[*] WHOIS Intel: {domain}...", file=sys.stderr)

    whois_data = whois_lookup(domain)
    analysis = analyze_whois(whois_data)

    # Remove raw from output for cleaner results
    whois_clean = {k: v for k, v in whois_data.items() if k != "raw"}

    return {
        "target": domain,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "whois": whois_clean,
        "analysis": analysis,
        "stats": {
            "name_servers": len(whois_data.get("name_servers", [])),
            "status_flags": len(whois_data.get("status", [])),
            "risk_score": analysis.get("risk_score", 0),
        },
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python3 whois_intel.py <domain>"}))
        sys.exit(1)

    data = whois_scan(sys.argv[1])
    print(json.dumps(data, indent=2))
