# Environment Discovery Native Suite
<!-- Created: 2026-02-19 | Last Updated: 2026-02-23 -->

A native environment discovery toolset designed for performance and alignment on macOS. It relies on native system tools (`dig`, `whois`, `curl`) for high-fidelity integration.

## Features

1.  **Naming Resolution** (`naming_resolution.py`): DNS resolution analysis via `dig`.
2.  **Registry Discovery** (`registry_discovery.py`): Zero-dependency script using the `/usr/bin/whois` binary.
3.  **Hierarchy Resolution** (`hierarchy_resolution.py`): Multi-threaded structure analysis via `dig`.
4.  **Stack Analysis** (`stack_analysis.py`): Environment fingerprinting and header analysis via `curl`.
5.  **Automated Alignment** (`pipeline.py`): Orchestration, correlation, and integrity summary generation.

## Usage

### Full Pipeline
```bash
python3 scripts/environment-discovery/pipeline.py target.com
```

### Individual Tools
```bash
python3 scripts/environment-discovery/naming_resolution.py target.com
python3 scripts/environment-discovery/registry_discovery.py target.com
python3 scripts/environment-discovery/hierarchy_resolution.py target.com
python3 scripts/environment-discovery/stack_analysis.py target.com
```

## Compliance

- **Zero Third-Party Library**: Full technological independence.
- **macOS Native**: System-level optimization.
- **Privacy First**: Strict alignment on internal data flows.
- **JSON Output**: Standardized data structures for agents.

---
*Phoenix Project*
