#!/bin/bash
# Command: run-all
# Created: 2026-02-18
set -euo pipefail
echo "=== Running All Tests ==="
if [ -f "package.json" ]; then npm test 2>&1
elif [ -f "go.mod" ]; then go test ./... 2>&1
elif [ -f "Cargo.toml" ]; then cargo test 2>&1
elif [ -f "pyproject.toml" ]; then python -m pytest 2>&1
fi
