"""
Script: DNS Enumeration (Native Dig)
Created: 2026-02-19
Last Updated: 2026-02-19
Author: PhoenixProject

Utilise la commande native 'dig' de macOS pour une enumeration rapide et precise.
Zéro dépendance externe.
"""

import sys
import json
import subprocess
import time

RECORD_TYPES = ["A", "AAAA", "MX", "TXT", "NS", "SOA", "CNAME", "CAA"]

def resolve_records(domain, record_type):
    """Execution native de dig."""
    try:
        # +short permet d'avoir juste la valeur brute, +nord permet de ne pas recurser si on veut juste le cache
        result = subprocess.run(["dig", "+short", record_type, domain], capture_output=True, text=True, timeout=5)
        lines = result.stdout.strip().split("\n")
        
        results = []
        for line in lines:
            line = line.strip().strip('"')
            if not line: continue
            
            record = {"type": record_type, "value": line}
            
            # Formatage specifique pour MX (Priority Exchange)
            if record_type == "MX":
                parts = line.split()
                if len(parts) >= 2:
                    record["priority"] = int(parts[0])
                    record["exchange"] = parts[1]
            
            results.append(record)
        return results
    except Exception:
        return []

def analyze_email_security(records, domain):
    """Analyse SPF/DMARC a partir des records TXT."""
    txt = [r["value"] for r in records.get("TXT", [])]
    spf = next((t for t in txt if "v=spf1" in t), "")
    
    # Pour DMARC on fait un lookup specifique
    dmarc_recs = resolve_records(f"_dmarc.{domain}", "TXT")
    dmarc = next((r["value"] for r in dmarc_recs if "v=DMARC1" in r["value"].upper()), "")
    
    policy = "unknown"
    if dmarc:
        if "p=reject" in dmarc.lower(): policy = "reject"
        elif "p=quarantine" in dmarc.lower(): policy = "quarantine"
        elif "p=none" in dmarc.lower(): policy = "none"
    
    return {
        "spf": {
            "found": bool(spf),
            "raw": spf,
            "strict": "-all" in spf
        },
        "dmarc": {
            "found": bool(dmarc),
            "raw": dmarc,
            "policy": policy
        }
    }

def dns_enum(domain):
    """Orchestration de l'enumeration."""
    results = {"target": domain, "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "records": {}}
    
    for rtype in RECORD_TYPES:
        recs = resolve_records(domain, rtype)
        if recs:
            results["records"][rtype] = recs
            
    results["email_security"] = analyze_email_security(results["records"], domain)
    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python3 dns_enum.py <domain>"}))
        sys.exit(1)
    
    print(json.dumps(dns_enum(sys.argv[1]), indent=2))
