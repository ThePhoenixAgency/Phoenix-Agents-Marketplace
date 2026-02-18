"""
Script: Nuclei Scanner - Template-Based Vulnerability Scanning
Created: 2026-02-18
Last Updated: 2026-02-18

Wrapper pour Nuclei (projectdiscovery) avec gestion des templates,
filtrage par severite, et output JSON structure.
Necessite nuclei installe (go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest)
"""

import sys
import json
import time
import asyncio
import os


NUCLEI_TEMPLATE_CATEGORIES = [
    "cves",
    "exposures",
    "misconfiguration",
    "default-logins",
    "takeovers",
    "technologies",
    "vulnerabilities",
]


async def run_nuclei(targets, severity="critical,high", templates=None, rate_limit=50):
    """
    Execute Nuclei sur une liste de cibles.

    Args:
        targets: Liste d'URLs ou fichier de cibles
        severity: Niveaux de severite a scanner
        templates: Categories de templates (None = auto)
        rate_limit: Requests par seconde

    Returns:
        list: Vulnerabilites detectees
    """
    # Construire la commande
    cmd_parts = ["nuclei", "-silent", "-json", "-rate-limit", str(rate_limit)]

    if isinstance(targets, list):
        targets_str = "\n".join(targets)
        cmd_parts = [f"echo '{targets_str}' | nuclei -silent -json -rate-limit {rate_limit}"]
    elif os.path.isfile(targets):
        cmd_parts.extend(["-l", targets])
    else:
        cmd_parts.extend(["-u", targets])

    cmd_parts.extend(["-severity", severity])

    if templates:
        for tmpl in templates:
            cmd_parts.extend(["-t", tmpl])

    cmd = " ".join(cmd_parts) if isinstance(targets, list) else " ".join(cmd_parts)

    try:
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()

        if stderr:
            err = stderr.decode().strip()
            if err and "nuclei" not in err.lower():
                print(f"[WARNING] Nuclei stderr: {err[:200]}", file=sys.stderr)

        results = []
        for line in stdout.decode().split("\n"):
            if not line.strip():
                continue
            try:
                finding = json.loads(line)
                results.append({
                    "template_id": finding.get("template-id", ""),
                    "name": finding.get("info", {}).get("name", ""),
                    "severity": finding.get("info", {}).get("severity", ""),
                    "type": finding.get("type", ""),
                    "host": finding.get("host", ""),
                    "matched_at": finding.get("matched-at", ""),
                    "description": finding.get("info", {}).get("description", "")[:300],
                    "reference": finding.get("info", {}).get("reference", [])[:5],
                    "tags": finding.get("info", {}).get("tags", []),
                    "curl_command": finding.get("curl-command", ""),
                })
            except json.JSONDecodeError:
                continue

        return results
    except Exception as exc:
        print(f"[ERROR] Nuclei execution failed: {exc}", file=sys.stderr)
        return []


async def scan(target, severity="critical,high,medium"):
    """
    Scan complet avec Nuclei.

    Args:
        target: URL ou domaine cible
        severity: Niveaux de severite

    Returns:
        dict: Resultats structures
    """
    print(f"[*] Nuclei Scanner: {target}...", file=sys.stderr)

    results = await run_nuclei(target, severity)

    # Grouper par severite
    by_severity = {"critical": [], "high": [], "medium": [], "low": [], "info": []}
    for finding in results:
        sev = finding.get("severity", "info").lower()
        if sev in by_severity:
            by_severity[sev].append(finding)

    return {
        "target": target,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "scanner": "nuclei",
        "severity_filter": severity,
        "vulns": results,
        "by_severity": {k: v for k, v in by_severity.items() if v},
        "stats": {
            "total": len(results),
            "critical": len(by_severity["critical"]),
            "high": len(by_severity["high"]),
            "medium": len(by_severity["medium"]),
            "low": len(by_severity["low"]),
        },
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python3 nuclei_scanner.py <target> [severity]"}))
        sys.exit(1)

    target_input = sys.argv[1]
    sev = sys.argv[2] if len(sys.argv) > 2 else "critical,high,medium"
    data = asyncio.run(scan(target_input, sev))
    print(json.dumps(data, indent=2))
