#!/usr/bin/env bash
# Command: osint/social - Social media profiler
# Created: 2026-02-19
# Last Updated: 2026-02-19
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PYTHON="${SCRIPT_DIR}/.venv/bin/python3"
[ ! -f "$PYTHON" ] && PYTHON="python3"
[ $# -lt 1 ] && echo '{"error": "Usage: /osint social <username>"}' && exit 1
"$PYTHON" "${SCRIPT_DIR}/scripts/osint/social_profiler.py" "$@"
