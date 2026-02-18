#!/bin/bash
# Command: module-graph
# Created: 2026-02-18
set -euo pipefail
echo "=== Module Graph ==="
echo ""
echo "Import dependencies:"
find . -name "*.js" -o -name "*.ts" | grep -v node_modules | grep -v coverage | while read f; do
  IMPORTS=$(grep -cE "^(import |const .* = require)" "$f" 2>/dev/null || echo 0)
  if [ "$IMPORTS" -gt 5 ]; then
    echo "  [WARNING] $f has $IMPORTS imports (high coupling)"
  fi
done
echo ""
echo "[INFO] Files with > 5 imports may indicate high coupling."
