#!/bin/bash
# Command: api-diff
# Created: 2026-02-18
set -euo pipefail
BASE=${1:-main}
echo "=== API Diff vs $BASE ==="
echo ""
echo "Changed API files:"
git diff "$BASE" --name-only -- '*.ts' '*.js' 2>/dev/null | \
  grep -iE "(route|controller|handler|api|endpoint)" || echo "  (none detected)"
echo ""
echo "Changed exports:"
git diff "$BASE" -- '*.ts' '*.js' 2>/dev/null | \
  grep -E "^[+-].*(export|module\.exports)" | head -20 || echo "  (none)"
