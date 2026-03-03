"""
Script: Correlation Engine - Entity Relationship Analysis
Created: 2026-02-18
Last Updated: 2026-02-18

Correle les resultats de tous les modules OSINT pour construire
un graphe de relations entre entites (domaines, IPs, emails, personnes, technologies).
"""

import sys
import json
import time
from collections import defaultdict


class CorrelationEngine:
    """Moteur de correlation inter-sources OSINT."""

    def __init__(self):
        self.entities = {}
        self.relationships = []
        self.sources = []

    def ingest(self, scan_result, source_name):
        """
        Ingere un resultat de scan et extrait les entites de maniere robuste.
        """
        if not scan_result or not isinstance(scan_result, (dict, list)):
            return
            
        self.sources.append(source_name)
        
        # Cas ou le resultat est une liste (ex: subdomain_enum)
        if isinstance(scan_result, list):
            for item in scan_result:
                if isinstance(item, dict):
                    sub = item.get("subdomain")
                    ip = item.get("ip")
                    if sub:
                        self._add_entity("domain", sub, source_name)
                        if ip:
                            self._add_entity("ip", ip, source_name)
                            self._add_relationship(sub, ip, "resolves_to")
            return

        # Cas dictionnaire (format standard)
        target = scan_result.get("target") or scan_result.get("domain") or "unknown"
        self._add_entity("domain", target, source_name)

        # DNS Records
        records = scan_result.get("records", {})
        if isinstance(records, dict):
            for rtype, rec_list in records.items():
                for r in rec_list:
                    val = r.get("value")
                    if val:
                        self._add_entity("dns_record", f"{rtype}:{val}", source_name)
                        self._add_relationship(target, f"{rtype}:{val}", "has_dns_record")

        # WHOIS
        whois_data = scan_result.get("whois") or scan_result
        if isinstance(whois_data, dict):
            registrar = whois_data.get("registrar")
            if registrar:
                self._add_entity("registrar", registrar, source_name)
                self._add_relationship(target, registrar, "registered_via")
            
            org = whois_data.get("registrant", {}).get("organization") or whois_data.get("organization")
            if org:
                self._add_entity("organization", org, source_name)
                self._add_relationship(target, org, "owned_by")

        # Emails
        emails = scan_result.get("all_unique_emails") or scan_result.get("discovered_emails") or []
        for email in emails:
            self._add_entity("email", email, source_name)
            self._add_relationship(target, email, "has_email")

    def _add_entity(self, entity_type, value, source):
        """Ajoute une entite au graphe."""
        if not value or not isinstance(value, str):
            return
        key = f"{entity_type}:{value}"
        if key not in self.entities:
            self.entities[key] = {
                "type": entity_type,
                "value": value,
                "sources": [],
                "first_seen": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            }
        if source not in self.entities[key]["sources"]:
            self.entities[key]["sources"].append(source)

    def _add_relationship(self, source_entity, target_entity, rel_type):
        """Ajoute une relation entre deux entites."""
        if not source_entity or not target_entity:
            return
        rel = {
            "source": source_entity,
            "target": target_entity,
            "type": rel_type,
        }
        if rel not in self.relationships:
            self.relationships.append(rel)

    def get_entity_summary(self):
        """Resume par type d'entite."""
        summary = defaultdict(int)
        for entity in self.entities.values():
            summary[entity["type"]] += 1
        return dict(summary)

    def get_cross_referenced(self):
        """Entites vues dans plusieurs sources (haute confiance)."""
        return [
            e for e in self.entities.values()
            if len(e["sources"]) > 1
        ]

    def get_hub_entities(self, min_connections=3):
        """Entites avec le plus de connexions (hubs)."""
        connection_count = defaultdict(int)
        for rel in self.relationships:
            connection_count[rel["source"]] += 1
            connection_count[rel["target"]] += 1

        hubs = [
            {"entity": entity, "connections": count}
            for entity, count in connection_count.items()
            if count >= min_connections
        ]
        return sorted(hubs, key=lambda x: x["connections"], reverse=True)

    def export(self):
        """Exporte le graphe complet."""
        return {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "sources_ingested": self.sources,
            "entities": list(self.entities.values()),
            "relationships": self.relationships,
            "summary": self.get_entity_summary(),
            "cross_referenced": self.get_cross_referenced(),
            "hubs": self.get_hub_entities(),
            "stats": {
                "total_entities": len(self.entities),
                "total_relationships": len(self.relationships),
                "sources": len(set(self.sources)),
                "cross_referenced": len(self.get_cross_referenced()),
            },
        }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python3 correlation_engine.py <file1.json> [file2.json ...]"}))
        sys.exit(1)

    engine = CorrelationEngine()
    for filepath in sys.argv[1:]:
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
            source = filepath.split("/")[-1].replace(".json", "")
            engine.ingest(data, source)
        except Exception as exc:
            print(f"[WARNING] Failed to ingest {filepath}: {exc}", file=sys.stderr)

    print(json.dumps(engine.export(), indent=2))
