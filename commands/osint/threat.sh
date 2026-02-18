#!/usr/bin/env bash
# Command: osint/threat - Threat intelligence feeds
# Created: 2026-02-19
# Last Updated: 2026-02-19
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PYTHON="${SCRIPT_DIR}/.venv/bin/python3"
[ ! -f "$PYTHON" ] && PYTHON="python3"
[ $# -lt 1 ] && echo '{"error": "Usage: /osint threat <indicator> [domain|ip|hostname]"}' && exit 1
"$PYTHON" "${SCRIPT_DIR}/scripts/osint/threat_feed.py" "$@"
