#!/bin/bash
# Command: deps-check (security)
# Created: 2026-02-18
set -euo pipefail
echo "=== Dependency Security Check ==="
echo ""
if [ -f "package.json" ]; then
  echo "[CHECK] npm audit..."
  npm audit 2>&1 | tail -10
  echo ""
  echo "[CHECK] Known CVEs..."
  npm audit --json 2>/dev/null | jq '.vulnerabilities | length' 2>/dev/null | \
    xargs -I{} echo "  {} vulnerable packages" || echo "  Unable to parse"
fi
