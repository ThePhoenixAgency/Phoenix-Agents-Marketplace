"""
Script: Threat Feed - Cyber Threat Intelligence Aggregation
Created: 2026-02-18
Last Updated: 2026-02-18

Agregation de feeds CTI publics : AlienVault OTX, AbuseIPDB, VirusTotal.
Correlation d'indicateurs de compromission (IoC).
"""

import sys
import json
import time
import os

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

OTX_API_KEY = os.getenv("OTX_API_KEY", "")
ABUSEIPDB_KEY = os.getenv("ABUSEIPDB_API_KEY", "")
VT_API_KEY = os.getenv("VIRUSTOTAL_API_KEY", "")


def query_otx(indicator, indicator_type="domain"):
    """
    Interroge AlienVault OTX pour un indicateur.

    Args:
        indicator: Valeur de l'indicateur
        indicator_type: domain, ip, url, hostname

    Returns:
        dict: Pulses et IoCs associes
    """
    if not OTX_API_KEY or not HAS_REQUESTS:
        return {"checked": False, "reason": "No OTX API key"}

    type_map = {
        "domain": f"https://otx.alienvault.com/api/v1/indicators/domain/{indicator}/general",
        "ip": f"https://otx.alienvault.com/api/v1/indicators/IPv4/{indicator}/general",
        "hostname": f"https://otx.alienvault.com/api/v1/indicators/hostname/{indicator}/general",
    }

    url = type_map.get(indicator_type, type_map["domain"])
    headers = {"X-OTX-API-KEY": OTX_API_KEY}

    try:
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            pulses = data.get("pulse_info", {}).get("pulses", [])
            return {
                "checked": True,
                "pulse_count": len(pulses),
                "pulses": [
                    {
                        "name": p.get("name", ""),
                        "description": p.get("description", "")[:200],
                        "created": p.get("created", ""),
                        "tags": p.get("tags", [])[:10],
                        "adversary": p.get("adversary", ""),
                    }
                    for p in pulses[:10]
                ],
                "malware_families": data.get("pulse_info", {}).get("related", {}).get("alienvault", {}).get("malware_families", []),
            }
        return {"checked": False, "reason": f"HTTP {resp.status_code}"}
    except requests.RequestException as exc:
        return {"checked": False, "reason": str(exc)}


def query_abuseipdb(ip_address):
    """
    Verifie une IP dans AbuseIPDB.

    Args:
        ip_address: Adresse IP a verifier

    Returns:
        dict: Score d'abus et rapports
    """
    if not ABUSEIPDB_KEY or not HAS_REQUESTS:
        return {"checked": False, "reason": "No AbuseIPDB API key"}

    url = "https://api.abuseipdb.com/api/v2/check"
    headers = {"Key": ABUSEIPDB_KEY, "Accept": "application/json"}
    params = {"ipAddress": ip_address, "maxAgeInDays": 90}

    try:
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        if resp.status_code == 200:
            data = resp.json().get("data", {})
            return {
                "checked": True,
                "abuse_score": data.get("abuseConfidenceScore", 0),
                "total_reports": data.get("totalReports", 0),
                "country": data.get("countryCode", ""),
                "isp": data.get("isp", ""),
                "domain": data.get("domain", ""),
                "is_tor": data.get("isTor", False),
                "is_whitelisted": data.get("isWhitelisted", False),
            }
        return {"checked": False, "reason": f"HTTP {resp.status_code}"}
    except requests.RequestException as exc:
        return {"checked": False, "reason": str(exc)}


def query_virustotal(indicator, indicator_type="domain"):
    """
    Interroge VirusTotal pour un indicateur.

    Args:
        indicator: Valeur de l'indicateur
        indicator_type: domain, ip, url

    Returns:
        dict: Resultats d'analyse
    """
    if not VT_API_KEY or not HAS_REQUESTS:
        return {"checked": False, "reason": "No VirusTotal API key"}

    type_map = {
        "domain": f"https://www.virustotal.com/api/v3/domains/{indicator}",
        "ip": f"https://www.virustotal.com/api/v3/ip_addresses/{indicator}",
    }

    url = type_map.get(indicator_type, type_map["domain"])
    headers = {"x-apikey": VT_API_KEY}

    try:
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code == 200:
            data = resp.json().get("data", {}).get("attributes", {})
            stats = data.get("last_analysis_stats", {})
            return {
                "checked": True,
                "malicious": stats.get("malicious", 0),
                "suspicious": stats.get("suspicious", 0),
                "harmless": stats.get("harmless", 0),
                "undetected": stats.get("undetected", 0),
                "reputation": data.get("reputation", 0),
                "categories": data.get("categories", {}),
            }
        return {"checked": False, "reason": f"HTTP {resp.status_code}"}
    except requests.RequestException as exc:
        return {"checked": False, "reason": str(exc)}


def aggregate_threat_intel(indicator, indicator_type="domain"):
    """
    Agrege le renseignement de menace de toutes les sources.

    Args:
        indicator: Valeur de l'indicateur
        indicator_type: domain, ip, hostname

    Returns:
        dict: Intelligence agrege
    """
    print(f"[*] Threat Feed: {indicator} ({indicator_type})...", file=sys.stderr)

    results = {
        "indicator": indicator,
        "type": indicator_type,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "sources": {},
        "threat_score": 0,
    }

    # AlienVault OTX
    results["sources"]["otx"] = query_otx(indicator, indicator_type)
    time.sleep(1)

    # AbuseIPDB (IP seulement)
    if indicator_type == "ip":
        results["sources"]["abuseipdb"] = query_abuseipdb(indicator)
        time.sleep(1)

    # VirusTotal
    results["sources"]["virustotal"] = query_virustotal(indicator, indicator_type)

    # Calcul du threat score agrege
    score = 0
    otx = results["sources"].get("otx", {})
    if otx.get("pulse_count", 0) > 0:
        score += min(otx["pulse_count"] * 10, 40)

    abuse = results["sources"].get("abuseipdb", {})
    if abuse.get("abuse_score", 0) > 0:
        score += min(abuse["abuse_score"], 40)

    vt = results["sources"].get("virustotal", {})
    if vt.get("malicious", 0) > 0:
        score += min(vt["malicious"] * 5, 40)

    results["threat_score"] = min(score, 100)
    results["threat_level"] = (
        "critical" if score >= 80 else
        "high" if score >= 60 else
        "medium" if score >= 40 else
        "low" if score >= 20 else
        "clean"
    )

    results["stats"] = {
        "sources_checked": len(results["sources"]),
        "sources_available": len([s for s in results["sources"].values() if s.get("checked")]),
        "threat_score": results["threat_score"],
        "threat_level": results["threat_level"],
    }

    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python3 threat_feed.py <indicator> [domain|ip|hostname]"}))
        sys.exit(1)

    ind = sys.argv[1]
    ind_type = sys.argv[2] if len(sys.argv) > 2 else "domain"
    data = aggregate_threat_intel(ind, ind_type)
    print(json.dumps(data, indent=2))
