#!/bin/bash
# Command: api-docs
# Created: 2026-02-18
set -euo pipefail
echo "=== API Documentation ==="
echo ""
echo "Endpoints detected:"
grep -rn "app\.\(get\|post\|put\|patch\|delete\)\|router\.\(get\|post\|put\|patch\|delete\)" \
  --include="*.js" --include="*.ts" . 2>/dev/null | \
  grep -v node_modules | head -30 || echo "  (no routes detected)"
