#!/bin/bash
# Command: complexity-report
# Created: 2026-02-18
set -euo pipefail
echo "=== Complexity Report ==="
echo ""
echo "Files by size (top 20):"
find . -name "*.js" -o -name "*.ts" -o -name "*.tsx" -o -name "*.jsx" | \
  grep -v node_modules | grep -v coverage | grep -v dist | \
  while read f; do
    LINES=$(wc -l < "$f" 2>/dev/null || echo 0)
    echo "  $LINES $f"
  done | sort -rn | head -20
echo ""
echo "[WARNING] Files > 300 lines should be reviewed for splitting."
