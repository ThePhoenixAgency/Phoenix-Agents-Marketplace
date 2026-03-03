"""
Script: DNS Subdomain Discovery (Native Mac)
Created: 2026-02-19
Last Updated: 2026-02-19

Decouverte rapide de sous-domaines via 'dig'.
"""

import sys
import json
import subprocess
import concurrent.futures

# Wordlist minimaliste pour le test
COMMON_SUBS = ["www", "dev", "api", "staging", "mail", "blog", "test", "v1", "v2", "docs", "git", "cloud", "portal"]

def check_subdomain(sub, target):
    domain = f"{sub}.{target}"
    try:
        # dig +short est parfait ici
        result = subprocess.run(["dig", "+short", domain], capture_output=True, text=True, timeout=2)
        ip = result.stdout.strip()
        if ip:
            return {"subdomain": domain, "ip": ip.split("\n")[0]}
    except:
        pass
    return None

def enum_subdomains(target):
    results = []
    print(f"[*] Enumerating subdomains for {target}...", file=sys.stderr)
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_sub = {executor.submit(check_subdomain, sub, target): sub for sub in COMMON_SUBS}
        for future in concurrent.futures.as_completed(future_to_sub):
            res = future.result()
            if res:
                results.append(res)
    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
    print(json.dumps(enum_subdomains(sys.argv[1]), indent=2))
