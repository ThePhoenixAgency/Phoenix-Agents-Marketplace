#!/bin/bash
# Command: generate (docs)
# Created: 2026-02-18
set -euo pipefail
echo "=== Documentation Generator ==="
echo ""
echo "Scanning for undocumented exports..."
UNDOC=0
find . -name "*.js" -o -name "*.ts" | grep -v node_modules | grep -v coverage | grep -v dist | while read f; do
  EXPORTS=$(grep -n "^module\.exports\|^export " "$f" 2>/dev/null || true)
  JSDOC=$(grep -c "/\*\*" "$f" 2>/dev/null || echo 0)
  if [ -n "$EXPORTS" ] && [ "$JSDOC" -eq 0 ]; then
    echo "  [WARNING] $f has exports but no JSDoc"
    UNDOC=$((UNDOC + 1))
  fi
done
echo ""
echo "[INFO] Add JSDoc comments to all exported functions."
