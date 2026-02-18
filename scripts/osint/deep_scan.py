"""
Script: Deep Scan - Infrastructure Reconnaissance
Created: 2026-02-18
Last Updated: 2026-02-18

Scan passif + actif d'infrastructure : sous-domaines, technologies,
ports exposes. Utilise subfinder + httpx.
"""

import sys
import json
import asyncio
import time


async def run_tool(cmd):
    """
    Execute une commande shell async et retourne stdout.

    Args:
        cmd: Commande shell a executer

    Returns:
        str: Sortie standard de la commande
    """
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()

    if stderr:
        err_text = stderr.decode().strip()
        if err_text:
            print(f"[INFO] Tool stderr: {err_text}", file=sys.stderr)

    return stdout.decode().strip()


async def enumerate_subdomains(target):
    """
    Enumeration passive de sous-domaines via subfinder.

    Args:
        target: Domaine cible

    Returns:
        list: Sous-domaines trouves
    """
    print(f"[*] Subfinder: {target}...", file=sys.stderr)
    output = await run_tool(f"subfinder -d {target} -silent -all 2>/dev/null")
    domains = [d.strip() for d in output.split("\n") if d.strip()]
    return list(set(domains))


async def fingerprint_services(subdomains):
    """
    Detection de technologies et status HTTP via httpx.

    Args:
        subdomains: Liste de sous-domaines a scanner

    Returns:
        list: Resultats de fingerprinting
    """
    if not subdomains:
        return []

    print(f"[*] Httpx: {len(subdomains)} targets...", file=sys.stderr)
    targets_str = "\\n".join(subdomains)
    cmd = f"echo -e '{targets_str}' | httpx -silent -title -tech-detect -status-code -json 2>/dev/null"
    output = await run_tool(cmd)

    services = []
    for line in output.split("\n"):
        if not line.strip():
            continue
        try:
            data = json.loads(line)
            services.append({
                "url": data.get("url", ""),
                "title": data.get("title", ""),
                "technologies": data.get("tech", []),
                "status_code": data.get("status_code", 0),
                "content_length": data.get("content_length", 0),
                "webserver": data.get("webserver", ""),
            })
        except json.JSONDecodeError:
            continue

    return services


async def deep_scan(target):
    """
    Scan complet d'un domaine : subdomains + tech fingerprint.

    Args:
        target: Domaine cible

    Returns:
        dict: Resultats structures
    """
    results = {
        "target": target,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "subdomains": [],
        "services": [],
        "technologies_summary": {},
        "stats": {},
    }

    # Phase 1 : Enumeration passive
    results["subdomains"] = await enumerate_subdomains(target)

    # Phase 2 : Fingerprinting actif
    results["services"] = await fingerprint_services(results["subdomains"])

    # Phase 3 : Agregation des technologies
    tech_count = {}
    for svc in results["services"]:
        for tech in svc.get("technologies", []):
            tech_count[tech] = tech_count.get(tech, 0) + 1
    results["technologies_summary"] = tech_count

    # Stats
    results["stats"] = {
        "subdomains_found": len(results["subdomains"]),
        "services_alive": len(results["services"]),
        "unique_technologies": len(tech_count),
    }

    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python3 deep_scan.py <domain>"}))
        sys.exit(1)

    target = sys.argv[1]
    data = asyncio.run(deep_scan(target))
    print(json.dumps(data, indent=2))
