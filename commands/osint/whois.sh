#!/usr/bin/env bash
# Command: osint/whois - WHOIS intelligence
# Created: 2026-02-19
# Last Updated: 2026-02-19
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PYTHON="${SCRIPT_DIR}/.venv/bin/python3"
[ ! -f "$PYTHON" ] && PYTHON="python3"
[ $# -lt 1 ] && echo '{"error": "Usage: /osint whois <domain>"}' && exit 1
"$PYTHON" "${SCRIPT_DIR}/scripts/osint/whois_intel.py" "$@"
