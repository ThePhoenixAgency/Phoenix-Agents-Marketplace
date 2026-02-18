#!/bin/bash
# Command: move-file
# Created: 2026-02-18
set -euo pipefail
SRC=${1:-""}
DEST=${2:-""}
if [ -z "$SRC" ] || [ -z "$DEST" ]; then
  echo "Usage: move-file <source> <destination>"
  exit 1
fi
echo "=== Move File: $SRC -> $DEST ==="
echo ""
echo "Files importing $SRC:"
BASENAME=$(basename "$SRC" | sed 's/\.[^.]*$//')
grep -rn "$BASENAME" --include="*.js" --include="*.ts" --include="*.tsx" . 2>/dev/null | \
  grep -v node_modules | grep "import\|require" || echo "  (none)"
echo ""
echo "Steps:"
echo "  1. git mv $SRC $DEST"
echo "  2. Update all imports"
echo "  3. Run tests"
