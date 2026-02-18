#!/bin/bash
# Command: rename-symbol
# Created: 2026-02-18
set -euo pipefail
OLD=${1:-""}
NEW=${2:-""}
if [ -z "$OLD" ] || [ -z "$NEW" ]; then
  echo "Usage: rename-symbol <old_name> <new_name>"
  exit 1
fi
echo "=== Rename Symbol: $OLD -> $NEW ==="
echo ""
echo "Occurrences found:"
grep -rn "$OLD" --include="*.js" --include="*.ts" --include="*.tsx" --include="*.jsx" . 2>/dev/null | \
  grep -v node_modules | grep -v coverage || echo "  (none)"
echo ""
echo "To rename: sed -i '' 's/$OLD/$NEW/g' <files>"
echo "[WARNING] Always run tests after rename."
