#!/bin/bash
# Command: dead-code
# Created: 2026-02-18
set -euo pipefail
echo "=== Dead Code Detection ==="
echo ""
echo "Unreferenced exports:"
find . -name "*.js" -o -name "*.ts" | grep -v node_modules | grep -v coverage | grep -v dist | while read f; do
  BASENAME=$(basename "$f" | sed 's/\.[^.]*$//')
  REFS=$(grep -rl "$BASENAME" --include="*.js" --include="*.ts" . 2>/dev/null | grep -v node_modules | grep -v "$f" | wc -l | tr -d ' ')
  if [ "$REFS" -eq 0 ]; then
    EXPORTS=$(grep -c "module\.exports\|export " "$f" 2>/dev/null || echo 0)
    if [ "$EXPORTS" -gt 0 ]; then
      echo "  [WARNING] $f has exports but no importers"
    fi
  fi
done
echo ""
echo "[INFO] Review before deleting."
