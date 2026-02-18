#!/bin/bash
# Command: conflict-resolve
# Created: 2026-02-18
set -euo pipefail
echo "=== Conflict Resolution Helper ==="
CONFLICTS=$(git diff --name-only --diff-filter=U 2>/dev/null || echo "")
if [ -z "$CONFLICTS" ]; then
  echo "[OK] No merge conflicts detected."
  exit 0
fi
echo "[WARNING] Files with conflicts:"
echo "$CONFLICTS" | while read f; do
  COUNT=$(grep -c "<<<<<<< " "$f" 2>/dev/null || echo 0)
  echo "  $f ($COUNT conflicts)"
done
echo ""
echo "After resolving:"
echo "  git add <files>"
echo "  git commit"
