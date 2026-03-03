"""
Script: Alignment Orchestrator - Full Automated Discovery Pipeline
Created: 2026-02-18
Last Updated: 2026-02-23

Pipeline complet qui exécute tous les modules de découverte en séquence,
correle les résultats, et génère un résumé d'alignement.
"""

import sys
import json
import time
import os
import importlib.util


MODULES_DIR = os.path.dirname(os.path.abspath(__file__))


def load_module(module_name):
    """Charge dynamiquement un module de découverte."""
    filepath = os.path.join(MODULES_DIR, f"{module_name}.py")
    if not os.path.exists(filepath):
        return None
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    module = importlib.util.module_from_spec(spec)
    if spec.loader:
        spec.loader.exec_module(module)
    return module


def run_passive_discovery(target, output_dir="/tmp/discovery"):
    """
    Exécute tous les modules de découverte passive.
    """
    os.makedirs(output_dir, exist_ok=True)
    results = {}
    modules = [
        ("naming_resolution", "resolve_names"),
        ("registry_discovery", "discover_registry"),
        ("hierarchy_resolution", "resolve_hierarchy"),
        ("stack_analysis", "analyze_stack"),
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


def run_extended_discovery(target, output_dir="/tmp/discovery"):
    """
    Exécute les modules de découverte étendue (paramètres requis).
    """
    results = {}
    api_modules = [
        ("node_discovery", "discover_node", "SHODAN_API_KEY"),
        ("incident_feed", "aggregate_incident_data", None),
        ("contact_discovery", "discover_contacts", None),
        ("integrity_audit", "audit_integrity", "GITHUB_TOKEN"),
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


def run_relation_analysis(results, target, output_dir="/tmp/discovery"):
    """
    Corréle tous les résultats et génère le résumé d'alignement.
    """
    print(f"\n[*] Running relation engine...", file=sys.stderr)

    # Relation Engine
    rel_mod = load_module("relation_engine")
    if rel_mod:
        engine = rel_mod.RelationEngine()
        for module_name, result in results.items():
            if "data" in result:
                engine.ingest(result["data"], module_name)
        rel_data = engine.export()
        rel_path = os.path.join(output_dir, "relation.json")
        with open(rel_path, "w") as f:
            json.dump(rel_data, f, indent=2)

    # Summary
    print(f"[*] Generating final alignment summary...", file=sys.stderr)
    sum_mod = load_module("summary_generator")
    if sum_mod:
        discovery_results = [r["data"] for r in results.values() if "data" in r]
        summary = sum_mod.generate_summary(discovery_results, target)
        summary_path = os.path.join(output_dir, "alignment_summary.json")
        with open(summary_path, "w") as f:
            json.dump(summary, f, indent=2)
        print(f"  [OK] Alignment summary: {summary_path}", file=sys.stderr)
        return summary

    return {}


def full_alignment_pipeline(target, output_dir=None):
    """
    Pipeline d'alignement complet.
    """
    if not output_dir:
        output_dir = f"/tmp/discovery_{target.replace('.', '_')}_{int(time.time())}"

    print(f"{'=' * 60}", file=sys.stderr)
    print(f"[*] Alignment Pipeline - Domain: {target}", file=sys.stderr)
    print(f"[*] Output Area: {output_dir}", file=sys.stderr)
    print(f"{'=' * 60}", file=sys.stderr)

    start = time.time()

    # Phase 1 : Passive discovery
    results = run_passive_discovery(target, output_dir)

    # Phase 2 : Extended discovery
    ext_results = run_extended_discovery(target, output_dir)
    results.update(ext_results)

    # Phase 3 : Relation Mapping + Summary
    summary = run_relation_analysis(results, target, output_dir)

    elapsed = time.time() - start
    print(f"\n{'=' * 60}", file=sys.stderr)
    print(f"[OK] Pipeline complete in {elapsed:.1f}s", file=sys.stderr)
    print(f"[OK] Results in: {output_dir}", file=sys.stderr)
    print(f"{'=' * 60}", file=sys.stderr)

    return summary


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python3 pipeline.py <domain> [output_dir]"}))
        sys.exit(1)

    domain = sys.argv[1]
    out_dir = sys.argv[2] if len(sys.argv) > 2 else None
    summary = full_alignment_pipeline(domain, out_dir)
    print(json.dumps(summary, indent=2))
