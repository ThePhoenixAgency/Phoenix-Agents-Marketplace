#!/bin/bash
# Command: status (workflow)
# Created: 2026-02-18
set -euo pipefail
echo "=== Project Status ==="
echo ""
echo "Git:"
echo "  Branch: $(git branch --show-current 2>/dev/null || echo 'N/A')"
echo "  Last commit: $(git log -1 --oneline 2>/dev/null || echo 'N/A')"
echo "  Modified files: $(git status --short 2>/dev/null | wc -l | tr -d ' ')"
echo ""
echo "Dependencies:"
if [ -f "package.json" ]; then
  echo "  Runtime: $(jq '.dependencies | length' package.json 2>/dev/null || echo 'N/A')"
  echo "  Dev: $(jq '.devDependencies | length' package.json 2>/dev/null || echo 'N/A')"
fi
echo ""
echo "Tests:"
if [ -f "package.json" ]; then
  npx jest --coverage --silent 2>&1 | tail -5 || echo "  N/A"
fi
