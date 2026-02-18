"""
Script: Certificate Transparency - SSL/TLS Intelligence
Created: 2026-02-18
Last Updated: 2026-02-18

Interroge crt.sh pour decouvrir des sous-domaines via les logs
de Certificate Transparency. Source passive, pas de contact direct avec la cible.
"""

import sys
import json
import time
import requests


def query_crtsh(domain, include_expired=False):
    """
    Interroge crt.sh pour un domaine donne.

    Args:
        domain: Domaine cible
        include_expired: Inclure les certificats expires

    Returns:
        list: Certificats trouves avec metadata
    """
    url = f"https://crt.sh/?q=%.{domain}&output=json"
    headers = {"User-Agent": "OSINT-Toolkit/1.0"}

    try:
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        certs = resp.json()
    except (requests.RequestException, json.JSONDecodeError) as exc:
        print(f"[WARNING] crt.sh query failed: {exc}", file=sys.stderr)
        return []

    results = []
    seen_names = set()

    for cert in certs:
        name = cert.get("name_value", "")
        issuer = cert.get("issuer_name", "")
        not_before = cert.get("not_before", "")
        not_after = cert.get("not_after", "")
        cert_id = cert.get("id", "")

        # Chaque name_value peut contenir plusieurs domaines (newline separated)
        for single_name in name.split("\n"):
            single_name = single_name.strip().lower()
            if not single_name or single_name in seen_names:
                continue
            # Filtrer les wildcards resolus
            if single_name.startswith("*."):
                single_name = single_name[2:]

            seen_names.add(single_name)
            results.append({
                "domain": single_name,
                "issuer": issuer,
                "valid_from": not_before,
                "valid_to": not_after,
                "cert_id": cert_id,
            })

    return results


def extract_unique_subdomains(certs, target_domain):
    """
    Extrait les sous-domaines uniques des resultats crt.sh.

    Args:
        certs: Resultats de query_crtsh
        target_domain: Domaine parent pour filtrage

    Returns:
        list: Sous-domaines uniques tries
    """
    subdomains = set()
    for cert in certs:
        domain = cert["domain"]
        if domain.endswith(target_domain) or domain == target_domain:
            subdomains.add(domain)
    return sorted(subdomains)


def analyze_issuers(certs):
    """
    Analyse les CA (Certificate Authorities) utilisees.
    Utile pour identifier les patterns d'infrastructure.

    Args:
        certs: Resultats de query_crtsh

    Returns:
        dict: Comptage par issuer
    """
    issuers = {}
    for cert in certs:
        issuer = cert.get("issuer", "Unknown")
        # Simplifier le nom du CA
        if "Let's Encrypt" in issuer:
            key = "Let's Encrypt"
        elif "DigiCert" in issuer:
            key = "DigiCert"
        elif "Cloudflare" in issuer:
            key = "Cloudflare"
        elif "Amazon" in issuer:
            key = "Amazon (AWS)"
        elif "Google" in issuer:
            key = "Google Trust Services"
        elif "Sectigo" in issuer or "COMODO" in issuer:
            key = "Sectigo/Comodo"
        else:
            key = issuer[:60]
        issuers[key] = issuers.get(key, 0) + 1
    return dict(sorted(issuers.items(), key=lambda x: x[1], reverse=True))


def scan_cert_transparency(domain):
    """
    Scan complet de Certificate Transparency pour un domaine.

    Args:
        domain: Domaine cible

    Returns:
        dict: Resultats structures
    """
    print(f"[*] Certificate Transparency: {domain}...", file=sys.stderr)

    certs = query_crtsh(domain)
    subdomains = extract_unique_subdomains(certs, domain)
    issuers = analyze_issuers(certs)

    return {
        "target": domain,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "total_certificates": len(certs),
        "unique_subdomains": subdomains,
        "subdomains_count": len(subdomains),
        "certificate_authorities": issuers,
        "raw_certs": certs[:50],  # Limiter la sortie brute
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python3 cert_transparency.py <domain>"}))
        sys.exit(1)

    data = scan_cert_transparency(sys.argv[1])
    print(json.dumps(data, indent=2))
