"""
Script: Native WHOIS Intelligence
Created: 2026-02-19
Last Updated: 2026-02-19
Author: PhoenixProject

Extraction native des donnees WHOIS via le binaire systeme macOS.
Zéro dépendance externe.
"""

import sys
import json
import subprocess
import re
import datetime

def whois_scan(domain):
    """Effectue un WHOIS via la commande native et parse les resultats."""
    try:
        # Appel au binaire whois natif
        result = subprocess.run(["whois", domain], capture_output=True, text=True, timeout=15)
        output = result.stdout
        
        if not output or "No match for" in output or "NOT FOUND" in output:
             return {"target": domain, "error": "Domain not found", "timestamp": datetime.datetime.utcnow().isoformat()}

        # Regex robustes pour les champs standards
        patterns = {
            "registrar": r"Registrar: (.*)",
            "creation_date": r"(Creation Date|Created On): (.*)",
            "expiry_date": r"(Registry Expiry Date|Expiration Date): (.*)",
            "updated_date": r"(Updated Date|Last Updated On): (.*)",
            "registrant_org": r"Registrant Organization: (.*)",
            "registrant_country": r"Registrant Country: (.*)",
            "dnssec": r"DNSSEC: (.*)"
        }
        
        extracted = {}
        for key, pattern in patterns.items():
            match = re.search(pattern, output, re.I)
            extracted[key] = match.group(match.lastindex).strip() if match else ""

        # Cas particuliers (listes)
        nameservers = re.findall(r"Name Server: (.*)", output, re.I)
        status = re.findall(r"Domain Status: (.*)", output, re.I)

        return {
            "target": domain,
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "registrar": extracted["registrar"],
            "dates": {
                "created": extracted["creation_date"],
                "expires": extracted["expiry_date"],
                "updated": extracted["updated_date"]
            },
            "registrant": {
                "organization": extracted["registrant_org"],
                "country": extracted["registrant_country"]
            },
            "network": {
                "nameservers": sorted(list(set([ns.strip().lower() for ns in nameservers]))),
                "status": sorted(list(set([s.strip().lower() for s in status]))),
                "dnssec": extracted["dnssec"]
            },
            "raw_snippet": output[:1000] + ("..." if len(output) > 1000 else "")
        }

    except Exception as e:
        return {"target": domain, "error": str(e), "timestamp": datetime.datetime.utcnow().isoformat()}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python3 whois_intel.py <domain>"}))
        sys.exit(1)
    
    print(json.dumps(whois_scan(sys.argv[1]), indent=2))
