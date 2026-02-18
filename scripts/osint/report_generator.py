"""
Script: Report Generator - Structured OSINT Report
Created: 2026-02-18
Last Updated: 2026-02-18

Genere un rapport OSINT structure avec scoring de risque,
timeline, et recommandations actionnables.
"""

import sys
import json
import time


RISK_THRESHOLDS = {
    "critical": 80,
    "high": 60,
    "medium": 40,
    "low": 20,
    "info": 0,
}


def calculate_global_risk(scan_results):
    """
    Calcule le score de risque global a partir de tous les scans.

    Args:
        scan_results: Liste de resultats de scan

    Returns:
        dict: Score global et breakdown
    """
    scores = []
    breakdown = {}

    for result in scan_results:
        stats = result.get("stats", {})
        source = result.get("target", "unknown")
        score = stats.get("risk_score", 0)

        # Heuristiques additionnelles
        if stats.get("critical", 0) > 0:
            score = max(score, 80)
        if stats.get("sensitive", 0) > 0 or stats.get("sensitive_files", 0) > 0:
            score = max(score, 60)
        if stats.get("breached_count", 0) > 0:
            score = max(score, 70)
        if stats.get("known_vulns", 0) > 0:
            score += 20

        scores.append(min(score, 100))
        breakdown[source] = score

    global_score = max(scores) if scores else 0

    severity = "info"
    for sev, threshold in sorted(RISK_THRESHOLDS.items(), key=lambda x: x[1], reverse=True):
        if global_score >= threshold:
            severity = sev
            break

    return {
        "global_score": global_score,
        "severity": severity,
        "breakdown": breakdown,
    }


def generate_executive_summary(scan_results, risk):
    """
    Genere le resume executif.

    Args:
        scan_results: Resultats de scan
        risk: Score de risque

    Returns:
        str: Resume formate
    """
    lines = [
        f"Score de risque global: {risk['global_score']}/100 ({risk['severity'].upper()})",
        "",
    ]

    # Aggreger les stats
    total_subdomains = 0
    total_services = 0
    total_leaks = 0
    total_vulns = 0
    total_emails = 0

    for result in scan_results:
        stats = result.get("stats", {})
        total_subdomains += stats.get("subdomains_found", stats.get("subdomains_count", 0))
        total_services += stats.get("services_alive", 0)
        total_leaks += stats.get("total_findings", 0)
        total_vulns += stats.get("known_vulns", 0)
        total_emails += stats.get("discovered_count", stats.get("total_unique", 0))

    lines.append(f"Surface d'attaque decouverte:")
    lines.append(f"  - Sous-domaines: {total_subdomains}")
    lines.append(f"  - Services exposes: {total_services}")
    lines.append(f"  - Fuites potentielles: {total_leaks}")
    lines.append(f"  - Vulnerabilites connues: {total_vulns}")
    lines.append(f"  - Emails decouverts: {total_emails}")

    return "\n".join(lines)


def generate_recommendations(scan_results, risk):
    """
    Genere les recommandations basees sur les findings.

    Args:
        scan_results: Resultats de scan
        risk: Score de risque

    Returns:
        list: Recommandations priorisees
    """
    recommendations = []
    priority = 0

    for result in scan_results:
        stats = result.get("stats", {})

        if stats.get("critical", 0) > 0 or stats.get("critical_exposures", 0) > 0:
            priority += 1
            recommendations.append({
                "priority": priority,
                "severity": "critical",
                "action": "Corriger immediatement les expositions critiques detectees",
                "detail": "Services critiques exposes sur Internet (DB, RDP, etc.)",
            })

        if stats.get("sensitive", 0) > 0 or stats.get("sensitive_files", 0) > 0:
            priority += 1
            recommendations.append({
                "priority": priority,
                "severity": "critical",
                "action": "Supprimer les fichiers sensibles des archives publiques",
                "detail": "Fichiers .env, .key, .pem detectes dans l'historique",
            })

        email_grade = stats.get("email_grade", "")
        if email_grade in ["D", "F"]:
            priority += 1
            recommendations.append({
                "priority": priority,
                "severity": "high",
                "action": "Configurer SPF strict (-all) et DMARC (p=reject)",
                "detail": f"Score email securite: {email_grade}",
            })

        if stats.get("breached_count", 0) > 0:
            priority += 1
            recommendations.append({
                "priority": priority,
                "severity": "high",
                "action": "Forcer le reset des mots de passe des comptes compromis",
                "detail": "Emails trouves dans des breaches connues",
            })

    if not recommendations:
        recommendations.append({
            "priority": 1,
            "severity": "info",
            "action": "Maintenir la surveillance continue",
            "detail": "Aucun finding critique detecte",
        })

    return sorted(recommendations, key=lambda x: x["priority"])


def generate_report(scan_results, target="unknown"):
    """
    Genere le rapport OSINT complet.

    Args:
        scan_results: Liste de resultats de scan
        target: Cible principale

    Returns:
        dict: Rapport structure
    """
    risk = calculate_global_risk(scan_results)
    summary = generate_executive_summary(scan_results, risk)
    recommendations = generate_recommendations(scan_results, risk)

    return {
        "title": f"OSINT Assessment Report - {target}",
        "classification": "CONFIDENTIAL",
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "target": target,
        "risk_assessment": risk,
        "executive_summary": summary,
        "recommendations": recommendations,
        "modules_used": len(scan_results),
        "raw_results_count": sum(
            len(r.get("findings", r.get("leaks", r.get("subdomains", []))))
            for r in scan_results
        ),
    }


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Usage: python3 report_generator.py <target> <file1.json> [file2.json ...]"}))
        sys.exit(1)

    target = sys.argv[1]
    results = []
    for filepath in sys.argv[2:]:
        try:
            with open(filepath, "r") as f:
                results.append(json.load(f))
        except Exception as exc:
            print(f"[WARNING] Cannot read {filepath}: {exc}", file=sys.stderr)

    report = generate_report(results, target)
    print(json.dumps(report, indent=2))
