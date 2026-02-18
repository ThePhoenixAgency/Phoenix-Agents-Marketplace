"""
Hook: On Scan Complete - Notification post-scan
Created: 2026-02-18
Last Updated: 2026-02-18

Envoie une notification Discord/Webhook quand un scan OSINT est termine.
Le resultat JSON du scan est passe en argument.
"""

import sys
import json
import os
import time

# [PRIVATE] URL du webhook Discord via variable d'environnement
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK_URL")
SEVERITY_COLORS = {
    "critical": 0xFF0000,
    "high": 0xFF6600,
    "medium": 0xFFCC00,
    "low": 0x00FF00,
    "info": 0x0099FF,
}


def classify_severity(scan_data):
    """
    Determine la severite globale d'un scan.

    Args:
        scan_data: Resultats du scan

    Returns:
        str: Niveau de severite (critical, high, medium, low, info)
    """
    vulns = len(scan_data.get("vulns", []))
    leaks = len(scan_data.get("leaks", []))
    findings = len(scan_data.get("findings", []))

    if vulns > 0 or leaks > 0:
        return "critical"
    if findings > 10:
        return "high"
    if findings > 5:
        return "medium"
    if findings > 0:
        return "low"
    return "info"


def build_summary(scan_data):
    """
    Construit le resume du scan pour notification.

    Args:
        scan_data: Resultats du scan

    Returns:
        str: Resume formate
    """
    target = scan_data.get("target", scan_data.get("product", "Unknown"))
    stats = scan_data.get("stats", {})

    lines = [
        f"**Cible:** `{target}`",
        f"**Date:** {scan_data.get('timestamp', 'N/A')}",
    ]

    if stats:
        for key, value in stats.items():
            label = key.replace("_", " ").title()
            lines.append(f"**{label}:** {value}")

    vulns = scan_data.get("vulns", [])
    if vulns:
        lines.append(f"\n[CRITICAL] **{len(vulns)} vulnerabilites detectees**")
        for vuln in vulns[:5]:
            lines.append(f"  - {vuln.get('id', 'N/A')}: {vuln.get('description', '')[:100]}")

    leaks = scan_data.get("leaks", [])
    if leaks:
        lines.append(f"\n[WARNING] **{len(leaks)} fuites de donnees detectees**")

    return "\n".join(lines)


def notify_discord(summary, severity="info"):
    """
    Envoie une notification Discord via webhook.

    Args:
        summary: Texte du message
        severity: Niveau de severite pour la couleur
    """
    if not DISCORD_WEBHOOK:
        print("[INFO] DISCORD_WEBHOOK_URL not set, skipping notification", file=sys.stderr)
        return

    try:
        import requests
    except ImportError:
        print("[WARNING] requests not installed, skipping Discord notification", file=sys.stderr)
        return

    color = SEVERITY_COLORS.get(severity, 0x0099FF)
    severity_label = severity.upper()

    data = {
        "embeds": [{
            "title": f"[{severity_label}] Rapport de Scan OSINT",
            "description": summary,
            "color": color,
            "footer": {
                "text": f"OSINT Orchestrator | {time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())}"
            },
        }]
    }

    try:
        resp = requests.post(DISCORD_WEBHOOK, json=data, timeout=10)
        resp.raise_for_status()
        print("[OK] Discord notification sent", file=sys.stderr)
    except requests.RequestException as exc:
        print(f"[ERROR] Discord notification failed: {exc}", file=sys.stderr)


def notify_file(summary, severity, output_dir="/tmp/osint_reports"):
    """
    Sauvegarde le rapport dans un fichier local (fallback si pas de webhook).

    Args:
        summary: Resume du scan
        severity: Niveau de severite
        output_dir: Dossier de sortie
    """
    os.makedirs(output_dir, exist_ok=True)
    filename = f"report_{int(time.time())}_{severity}.txt"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w") as f:
        f.write(f"OSINT Scan Report\n")
        f.write(f"Severity: {severity.upper()}\n")
        f.write(f"{'=' * 50}\n\n")
        f.write(summary)

    print(f"[OK] Report saved: {filepath}", file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("[ERROR] Usage: python3 on_scan_complete.py <result.json>", file=sys.stderr)
        sys.exit(1)

    result_file = sys.argv[1]

    try:
        with open(result_file, "r") as f:
            scan_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        print(f"[ERROR] Cannot read result file: {exc}", file=sys.stderr)
        sys.exit(1)

    severity = classify_severity(scan_data)
    summary = build_summary(scan_data)

    # Notification multicanal
    notify_discord(summary, severity)
    notify_file(summary, severity)

    # Sortie JSON pour chainage
    print(json.dumps({
        "status": "notified",
        "severity": severity,
        "target": scan_data.get("target", scan_data.get("product", "unknown")),
    }))
