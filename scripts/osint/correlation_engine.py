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
        Ingere un resultat de scan et extrait les entites.

        Args:
            scan_result: Dictionnaire de resultats d'un module
            source_name: Nom du module source
        """
        self.sources.append(source_name)
        target = scan_result.get("target", "unknown")
        self._add_entity("domain", target, source_name)

        # Sous-domaines
        for sub in scan_result.get("subdomains", []):
            self._add_entity("domain", sub, source_name)
            self._add_relationship(target, sub, "has_subdomain")

        for sub in scan_result.get("unique_subdomains", []):
            self._add_entity("domain", sub, source_name)
            self._add_relationship(target, sub, "has_subdomain")

        # IPs
        ip = scan_result.get("ip", "")
        if ip:
            self._add_entity("ip", ip, source_name)
            self._add_relationship(target, ip, "resolves_to")

        # Emails
        for email in scan_result.get("discovered_emails", []):
            self._add_entity("email", email, source_name)
            self._add_relationship(target, email, "has_email")

        # Technologies
        for tech, count in scan_result.get("technologies_summary", {}).items():
            self._add_entity("technology", tech, source_name)
            self._add_relationship(target, tech, "uses_technology")

        # Services/ports
        for svc in scan_result.get("services", []):
            url = svc.get("url", "")
            if url:
                self._add_entity("service", url, source_name)
                self._add_relationship(target, url, "exposes_service")

        # Leaks
        for leak in scan_result.get("leaks", []):
            repo = leak.get("repository", "")
            if repo:
                self._add_entity("repository", repo, source_name)
                self._add_relationship(target, repo, "leaked_in")

        # Certificate Authorities
        for ca, count in scan_result.get("certificate_authorities", {}).items():
            self._add_entity("ca", ca, source_name)
            self._add_relationship(target, ca, "certified_by")

        # WHOIS
        registrar = scan_result.get("whois", {}).get("registrar", "")
        if registrar:
            self._add_entity("registrar", registrar, source_name)
            self._add_relationship(target, registrar, "registered_via")

        org = scan_result.get("organization", "")
        if org:
            self._add_entity("organization", org, source_name)
            self._add_relationship(target, org, "owned_by")

    def _add_entity(self, entity_type, value, source):
        """Ajoute une entite au graphe."""
        if not value:
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
