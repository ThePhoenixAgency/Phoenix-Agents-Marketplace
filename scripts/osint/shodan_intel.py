"""
Script: Shodan Intel - Internet-Facing Asset Intelligence
Created: 2026-02-18
Last Updated: 2026-02-18

Interroge l'API Shodan pour decouvrir les services exposes,
ports ouverts, vulnerabilites connues. Necessite une API key Shodan.
"""

import sys
import json
import time
import os
import socket

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

SHODAN_API_KEY = os.getenv("SHODAN_API_KEY", "")
SHODAN_BASE_URL = "https://api.shodan.io"

# Ports critiques dont l'exposition est un red flag
CRITICAL_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    445: "SMB",
    1433: "MSSQL",
    1521: "Oracle",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    5900: "VNC",
    6379: "Redis",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt",
    9200: "Elasticsearch",
    11211: "Memcached",
    27017: "MongoDB",
}


def resolve_domain(domain):
    """
    Resout un domaine en adresse IP.

    Args:
        domain: Domaine a resoudre

    Returns:
        str: Adresse IP ou None
    """
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except socket.gaierror:
        return None


def shodan_host_lookup(ip):
    """
    Interroge Shodan pour les informations sur un hote.

    Args:
        ip: Adresse IP

    Returns:
        dict: Donnees Shodan
    """
    if not SHODAN_API_KEY or not HAS_REQUESTS:
        return {"error": "No Shodan API key or requests not installed"}

    url = f"{SHODAN_BASE_URL}/shodan/host/{ip}?key={SHODAN_API_KEY}"
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200:
            return resp.json()
        elif resp.status_code == 404:
            return {"ip": ip, "ports": [], "data": [], "note": "No data in Shodan"}
        else:
            return {"error": f"HTTP {resp.status_code}"}
    except requests.RequestException as exc:
        return {"error": str(exc)}


def shodan_search(query, max_results=100):
    """
    Recherche Shodan avec un filtre.

    Args:
        query: Requete Shodan (ex: "hostname:example.com")
        max_results: Nombre max de resultats

    Returns:
        list: Resultats
    """
    if not SHODAN_API_KEY or not HAS_REQUESTS:
        return []

    url = f"{SHODAN_BASE_URL}/shodan/host/search?key={SHODAN_API_KEY}&query={query}"
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("matches", [])[:max_results]
    except requests.RequestException:
        pass
    return []


def analyze_exposure(shodan_data):
    """
    Analyse l'exposition des services detectes par Shodan.

    Args:
        shodan_data: Donnees Shodan

    Returns:
        dict: Analyse de risque
    """
    findings = []
    risk_score = 0
    open_ports = shodan_data.get("ports", [])

    # Check ports critiques
    for port in open_ports:
        if port in CRITICAL_PORTS:
            service = CRITICAL_PORTS[port]
            severity = "critical" if port in [23, 445, 3389, 5900, 6379, 27017, 9200, 11211] else "high"
            findings.append({
                "port": port,
                "service": service,
                "severity": severity,
                "description": f"{service} exposed on port {port}",
            })
            risk_score += 20 if severity == "critical" else 10

    # Check vulnerabilites
    vulns = shodan_data.get("vulns", [])
    for vuln in vulns:
        findings.append({
            "type": "CVE",
            "id": vuln,
            "severity": "high",
            "description": f"Known vulnerability: {vuln}",
        })
        risk_score += 15

    # Check services dans les bannieres
    for service_data in shodan_data.get("data", []):
        product = service_data.get("product", "")
        version = service_data.get("version", "")
        port = service_data.get("port", 0)

        # Detection de versions obsoletes (heuristique)
        if product and version:
            findings.append({
                "type": "service",
                "port": port,
                "product": product,
                "version": version,
                "severity": "info",
                "description": f"{product} {version} on port {port}",
            })

    return {
        "open_ports": open_ports,
        "critical_exposures": [f for f in findings if f.get("severity") == "critical"],
        "all_findings": findings,
        "known_vulns": vulns,
        "risk_score": min(risk_score, 100),
    }


def shodan_scan(target):
    """
    Scan Shodan complet pour un domaine ou IP.

    Args:
        target: Domaine ou IP

    Returns:
        dict: Resultats structures
    """
    print(f"[*] Shodan Intel: {target}...", file=sys.stderr)

    # Resolver le domaine si besoin
    ip = target
    domain = None
    try:
        socket.inet_aton(target)
    except socket.error:
        domain = target
        ip = resolve_domain(target)
        if not ip:
            return {
                "target": target,
                "error": f"Cannot resolve {target}",
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            }

    # Lookup Shodan
    shodan_data = shodan_host_lookup(ip)
    if "error" in shodan_data:
        return {
            "target": target,
            "ip": ip,
            "error": shodan_data["error"],
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }

    # Analyse
    analysis = analyze_exposure(shodan_data)

    return {
        "target": target,
        "ip": ip,
        "domain": domain,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "organization": shodan_data.get("org", ""),
        "asn": shodan_data.get("asn", ""),
        "isp": shodan_data.get("isp", ""),
        "os": shodan_data.get("os", ""),
        "country": shodan_data.get("country_name", ""),
        "city": shodan_data.get("city", ""),
        "analysis": analysis,
        "stats": {
            "open_ports": len(analysis["open_ports"]),
            "critical_exposures": len(analysis["critical_exposures"]),
            "known_vulns": len(analysis["known_vulns"]),
            "risk_score": analysis["risk_score"],
        },
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python3 shodan_intel.py <domain|ip>"}))
        sys.exit(1)

    data = shodan_scan(sys.argv[1])
    print(json.dumps(data, indent=2))
