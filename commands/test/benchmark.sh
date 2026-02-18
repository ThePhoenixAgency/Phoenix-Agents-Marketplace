#!/bin/bash
# Command: benchmark
# Created: 2026-02-18
set -euo pipefail
echo "=== Benchmark ==="
if [ -f "package.json" ]; then
  echo "[CHECK] Bundle size..."
  if [ -d "dist" ] || [ -d "build" ] || [ -d ".next" ]; then
    du -sh dist/ build/ .next/ 2>/dev/null || true
  fi
  echo ""
  echo "[CHECK] Dependencies count..."
  echo "  Production: $(jq '.dependencies | length' package.json 2>/dev/null || echo 'N/A')"
  echo "  Dev: $(jq '.devDependencies | length' package.json 2>/dev/null || echo 'N/A')"
  echo ""
  echo "[CHECK] node_modules size..."
  du -sh node_modules/ 2>/dev/null || echo "  N/A"
fi
