"""
Script: DNS Enumeration - DNS Records Intelligence
Created: 2026-02-18
Last Updated: 2026-02-18

Enumeration complete des records DNS : A, AAAA, MX, TXT, NS, SOA, CNAME.
Analyse SPF, DMARC, DKIM pour evaluer la posture email.
"""

import sys
import json
import time
import socket

try:
    import dns.resolver
    HAS_DNSPYTHON = True
except ImportError:
    HAS_DNSPYTHON = False


RECORD_TYPES = ["A", "AAAA", "MX", "TXT", "NS", "SOA", "CNAME", "SRV", "CAA"]


def resolve_records(domain, record_type):
    """
    Resout un type de record DNS pour un domaine.

    Args:
        domain: Domaine cible
        record_type: Type de record (A, MX, TXT, etc.)

    Returns:
        list: Records trouves
    """
    if not HAS_DNSPYTHON:
        return _resolve_fallback(domain, record_type)

    results = []
    try:
        answers = dns.resolver.resolve(domain, record_type)
        for answer in answers:
            record = {"type": record_type, "value": str(answer)}
            if record_type == "MX":
                record["priority"] = answer.preference
                record["exchange"] = str(answer.exchange)
            elif record_type == "SOA":
                record["mname"] = str(answer.mname)
                record["rname"] = str(answer.rname)
                record["serial"] = answer.serial
            results.append(record)
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers):
        pass
    except Exception as exc:
        print(f"[WARNING] DNS {record_type} for {domain}: {exc}", file=sys.stderr)

    return results


def _resolve_fallback(domain, record_type):
    """Fallback quand dnspython n'est pas installe (A records seulement)."""
    if record_type != "A":
        return []
    try:
        ips = socket.getaddrinfo(domain, None)
        seen = set()
        results = []
        for info in ips:
            ip = info[4][0]
            if ip not in seen:
                seen.add(ip)
                results.append({"type": "A", "value": ip})
        return results
    except socket.gaierror:
        return []


def analyze_spf(txt_records):
    """
    Analyse la politique SPF depuis les records TXT.

    Args:
        txt_records: Liste de records TXT

    Returns:
        dict: Analyse SPF
    """
    for record in txt_records:
        value = record.get("value", "")
        if "v=spf1" in value:
            mechanisms = value.split()
            return {
                "found": True,
                "raw": value,
                "includes": [m for m in mechanisms if m.startswith("include:")],
                "ips": [m for m in mechanisms if m.startswith("ip4:") or m.startswith("ip6:")],
                "policy": mechanisms[-1] if mechanisms else "unknown",
                "strict": mechanisms[-1] == "-all" if mechanisms else False,
            }
    return {"found": False, "raw": "", "strict": False}


def analyze_dmarc(domain):
    """
    Analyse la politique DMARC du domaine.

    Args:
        domain: Domaine cible

    Returns:
        dict: Analyse DMARC
    """
    dmarc_domain = f"_dmarc.{domain}"
    records = resolve_records(dmarc_domain, "TXT")

    for record in records:
        value = record.get("value", "")
        if "v=DMARC1" in value:
            parts = {}
            for tag in value.split(";"):
                tag = tag.strip()
                if "=" in tag:
                    key, val = tag.split("=", 1)
                    parts[key.strip()] = val.strip()
            return {
                "found": True,
                "raw": value,
                "policy": parts.get("p", "none"),
                "subdomain_policy": parts.get("sp", ""),
                "report_email": parts.get("rua", ""),
                "percentage": parts.get("pct", "100"),
            }
    return {"found": False, "policy": "none"}


def analyze_email_security(spf_result, dmarc_result, mx_records):
    """
    Evaluation globale de la securite email.

    Args:
        spf_result: Resultat analyse SPF
        dmarc_result: Resultat analyse DMARC
        mx_records: Records MX

    Returns:
        dict: Score et recommandations
    """
    score = 0
    issues = []

    if not mx_records:
        return {"score": 0, "grade": "N/A", "issues": ["No MX records - no email"]}

    if spf_result.get("found"):
        score += 30
        if spf_result.get("strict"):
            score += 20
        else:
            issues.append("SPF policy is not strict (-all recommended)")
    else:
        issues.append("[CRITICAL] No SPF record found")

    if dmarc_result.get("found"):
        score += 30
        if dmarc_result.get("policy") == "reject":
            score += 20
        elif dmarc_result.get("policy") == "quarantine":
            score += 10
        else:
            issues.append("DMARC policy is 'none' - no enforcement")
    else:
        issues.append("[CRITICAL] No DMARC record found")

    grades = {90: "A+", 80: "A", 70: "B", 60: "C", 50: "D", 0: "F"}
    grade = "F"
    for threshold, g in sorted(grades.items(), reverse=True):
        if score >= threshold:
            grade = g
            break

    return {"score": score, "grade": grade, "issues": issues}


def dns_enum(domain):
    """
    Enumeration DNS complete d'un domaine.

    Args:
        domain: Domaine cible

    Returns:
        dict: Resultats structures
    """
    print(f"[*] DNS Enumeration: {domain}...", file=sys.stderr)

    all_records = {}
    for rtype in RECORD_TYPES:
        records = resolve_records(domain, rtype)
        if records:
            all_records[rtype] = records

    # Analyse email
    txt_records = all_records.get("TXT", [])
    mx_records = all_records.get("MX", [])
    spf = analyze_spf(txt_records)
    dmarc = analyze_dmarc(domain)
    email_security = analyze_email_security(spf, dmarc, mx_records)

    return {
        "target": domain,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "dns_provider": not HAS_DNSPYTHON and "fallback (socket)" or "dnspython",
        "records": all_records,
        "email_analysis": {
            "spf": spf,
            "dmarc": dmarc,
            "security_grade": email_security,
        },
        "stats": {
            "total_records": sum(len(v) for v in all_records.values()),
            "record_types_found": list(all_records.keys()),
            "has_email": len(mx_records) > 0,
            "email_grade": email_security.get("grade", "N/A"),
        },
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python3 dns_enum.py <domain>"}))
        sys.exit(1)

    data = dns_enum(sys.argv[1])
    print(json.dumps(data, indent=2))
