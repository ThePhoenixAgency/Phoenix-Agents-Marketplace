#!/bin/bash
# Command: license-check
# Created: 2026-02-18
set -euo pipefail
echo "=== License Check ==="
echo ""
if [ -f "package.json" ]; then
  echo "Dependencies licenses:"
  npx license-checker --summary 2>/dev/null || \
    echo "[INFO] Install: npm i -g license-checker"
fi
echo ""
echo "[CHECK] Project license..."
if [ -f "LICENSE" ] || [ -f "LICENSE.md" ]; then
  head -1 LICENSE* 2>/dev/null
  echo "  [OK] License file found"
else
  echo "  [WARNING] No LICENSE file"
fi
