#!/usr/bin/env bash
# Command: osint/recon - Full OSINT reconnaissance pipeline
# Created: 2026-02-19
# Last Updated: 2026-02-19
#
# Lance le pipeline OSINT complet sur un domaine cible.
# Usage: /osint recon <domain>

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PYTHON="${SCRIPT_DIR}/.venv/bin/python3"

if [ ! -f "$PYTHON" ]; then
    PYTHON="python3"
fi

if [ $# -lt 1 ]; then
    echo '{"error": "Usage: /osint recon <domain>"}'
    exit 1
fi

"$PYTHON" "${SCRIPT_DIR}/scripts/osint/pipeline.py" "$@"
