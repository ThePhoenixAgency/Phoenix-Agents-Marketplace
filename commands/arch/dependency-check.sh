#!/bin/bash
# Command: dependency-check
# Created: 2026-02-18
set -euo pipefail
echo "=== Dependency Check ==="
if [ -f "package.json" ]; then
  echo "[CHECK] Outdated packages..."
  npm outdated 2>/dev/null || echo "[OK] All up to date"
  echo ""
  echo "[CHECK] Duplicates..."
  npm ls --all 2>/dev/null | grep -i "deduped" | wc -l | xargs -I{} echo "  {} deduplicated packages"
fi
