#!/bin/bash
# Command: test-watch
# Created: 2026-02-18
set -euo pipefail
echo "=== Test Watch Mode ==="
if [ -f "package.json" ]; then
  npx jest --watch 2>&1
elif [ -f "pyproject.toml" ]; then
  python -m pytest-watch 2>&1
elif [ -f "go.mod" ]; then
  echo "[INFO] Go: use 'go test ./... -v' with entr or fswatch"
fi
