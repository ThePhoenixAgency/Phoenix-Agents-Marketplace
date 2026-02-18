"""
Script: OSINT Pipeline - Full Automated Reconnaissance Pipeline
Created: 2026-02-18
Last Updated: 2026-02-18

Pipeline complet qui execute tous les modules OSINT en sequence,
correle les resultats, et genere un rapport final.
"""

import sys
import json
import time
import os
import asyncio
import importlib.util


MODULES_DIR = os.path.dirname(os.path.abspath(__file__))


def load_module(module_name):
    """Charge dynamiquement un module OSINT."""
    filepath = os.path.join(MODULES_DIR, f"{module_name}.py")
    if not os.path.exists(filepath):
        return None
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_passive_recon(target, output_dir="/tmp/osint"):
    """
    Execute tous les modules de recon passive.

    Args:
        target: Domaine cible
        output_dir: Dossier de sortie

    Returns:
        dict: Chemins des fichiers de resultats
    """
    os.makedirs(output_dir, exist_ok=True)
    results = {}
    modules = [
        ("cert_transparency", "scan_cert_transparency"),
        ("dns_enum", "dns_enum"),
        ("whois_intel", "whois_scan"),
        ("wayback_scanner", "wayback_scan"),
        ("google_dorker", "run_dorking"),
    ]

    for module_name, func_name in modules:
        print(f"\n[*] Running {module_name}...", file=sys.stderr)
        try:
            mod = load_module(module_name)
            if mod and hasattr(mod, func_name):
                func = getattr(mod, func_name)
                result = func(target)
                filepath = os.path.join(output_dir, f"{module_name}.json")
                with open(filepath, "w") as f:
                    json.dump(result, f, indent=2)
                results[module_name] = {"path": filepath, "data": result}
                print(f"  [OK] {module_name}: saved to {filepath}", file=sys.stderr)
            else:
                print(f"  [WARNING] {module_name}: module or function not found", file=sys.stderr)
        except Exception as exc:
            print(f"  [ERROR] {module_name}: {exc}", file=sys.stderr)
            results[module_name] = {"error": str(exc)}

    return results


def run_api_modules(target, output_dir="/tmp/osint"):
    """
    Execute les modules qui necessitent des API keys.

    Args:
        target: Domaine cible
        output_dir: Dossier de sortie

    Returns:
        dict: Resultats
    """
    results = {}
    api_modules = [
        ("shodan_intel", "shodan_scan", "SHODAN_API_KEY"),
        ("threat_feed", "aggregate_threat_intel", None),
        ("email_hunter", "email_hunt", None),
        ("leak_scanner", "scan_for_leaks", "GITHUB_TOKEN"),
    ]

    for module_name, func_name, env_key in api_modules:
        if env_key and not os.getenv(env_key):
            print(f"  [SKIP] {module_name}: {env_key} not set", file=sys.stderr)
            continue

        print(f"\n[*] Running {module_name}...", file=sys.stderr)
        try:
            mod = load_module(module_name)
            if mod and hasattr(mod, func_name):
                func = getattr(mod, func_name)
                result = func(target)
                filepath = os.path.join(output_dir, f"{module_name}.json")
                with open(filepath, "w") as f:
                    json.dump(result, f, indent=2)
                results[module_name] = {"path": filepath, "data": result}
                print(f"  [OK] {module_name}: saved to {filepath}", file=sys.stderr)
        except Exception as exc:
            print(f"  [ERROR] {module_name}: {exc}", file=sys.stderr)
            results[module_name] = {"error": str(exc)}

    return results


def run_correlation(results, target, output_dir="/tmp/osint"):
    """
    Correle tous les resultats et genere le rapport final.

    Args:
        results: Resultats de tous les modules
        target: Cible
        output_dir: Dossier de sortie

    Returns:
        dict: Rapport final
    """
    print(f"\n[*] Running correlation engine...", file=sys.stderr)

    # Correlation
    corr_mod = load_module("correlation_engine")
    if corr_mod:
        engine = corr_mod.CorrelationEngine()
        for module_name, result in results.items():
            if "data" in result:
                engine.ingest(result["data"], module_name)
        corr_data = engine.export()
        corr_path = os.path.join(output_dir, "correlation.json")
        with open(corr_path, "w") as f:
            json.dump(corr_data, f, indent=2)

    # Report
    print(f"[*] Generating final report...", file=sys.stderr)
    report_mod = load_module("report_generator")
    if report_mod:
        scan_results = [r["data"] for r in results.values() if "data" in r]
        report = report_mod.generate_report(scan_results, target)
        report_path = os.path.join(output_dir, "final_report.json")
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)
        print(f"  [OK] Final report: {report_path}", file=sys.stderr)
        return report

    return {}


def full_pipeline(target, output_dir=None):
    """
    Pipeline OSINT complet.

    Args:
        target: Domaine cible
        output_dir: Dossier de sortie

    Returns:
        dict: Rapport final
    """
    if not output_dir:
        output_dir = f"/tmp/osint_{target}_{int(time.time())}"

    print(f"{'=' * 60}", file=sys.stderr)
    print(f"[*] OSINT Pipeline - Target: {target}", file=sys.stderr)
    print(f"[*] Output: {output_dir}", file=sys.stderr)
    print(f"{'=' * 60}", file=sys.stderr)

    start = time.time()

    # Phase 1 : Passive recon
    results = run_passive_recon(target, output_dir)

    # Phase 2 : API modules
    api_results = run_api_modules(target, output_dir)
    results.update(api_results)

    # Phase 3 : Correlation + Report
    report = run_correlation(results, target, output_dir)

    elapsed = time.time() - start
    print(f"\n{'=' * 60}", file=sys.stderr)
    print(f"[OK] Pipeline complete in {elapsed:.1f}s", file=sys.stderr)
    print(f"[OK] Results in: {output_dir}", file=sys.stderr)
    print(f"{'=' * 60}", file=sys.stderr)

    return report


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python3 pipeline.py <domain> [output_dir]"}))
        sys.exit(1)

    domain = sys.argv[1]
    out_dir = sys.argv[2] if len(sys.argv) > 2 else None
    report = full_pipeline(domain, out_dir)
    print(json.dumps(report, indent=2))
