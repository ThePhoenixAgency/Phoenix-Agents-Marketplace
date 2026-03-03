"""
Script: Web Technology & Header Scanner (Native)
Created: 2026-02-19
Last Updated: 2026-02-19

Fingerprinting d'un serveur web via ses headers HTTP (CURL).
Zéro dépendance.
"""

import sys
import json
import subprocess
import time

def scan_web(domain):
    """Analyse les headers HTTP du domaine."""
    target_url = f"https://{domain}"
    print(f"[*] Scanning Web Headers: {target_url}...", file=sys.stderr)
    
    cmd = ["curl", "-I", "-s", "-L", "--max-time", "10", target_url]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        output = result.stdout
        
        if not output:
             return {"target": domain, "error": "No response"}

        lines = output.strip().split("\n")
        headers = {}
        for line in lines:
            if ":" in line:
                key, val = line.split(":", 1)
                headers[key.strip().lower()] = val.strip()

        # Analyse des technos et securite
        analysis = {
            "server": headers.get("server", "unknown"),
            "technologies": [],
            "security": {
                "hsts": "strict-transport-security" in headers,
                "csp": "content-security-policy" in headers,
                "x_frame": headers.get("x-frame-options", "not set"),
                "x_content_type": headers.get("x-content-type-options", "not set")
            }
        }
        
        # Detection technos classiques
        if "x-powered-by" in headers:
            analysis["technologies"].append(headers["x-powered-by"])
        if "via" in headers:
            analysis["technologies"].append(f"Via: {headers['via']}")
        if "cf-ray" in headers:
            analysis["technologies"].append("Cloudflare")
        if "github" in headers.get("server", "").lower():
            analysis["technologies"].append("GitHub Pages")

        return {
            "target": domain,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "headers_count": len(headers),
            "analysis": analysis,
            "raw_headers": headers
        }

    except Exception as e:
        return {"target": domain, "error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
    print(json.dumps(scan_web(sys.argv[1]), indent=2))
