#!/bin/bash
# Command: mutation-test
# Created: 2026-02-18
set -euo pipefail
echo "=== Mutation Testing ==="
if [ -f "package.json" ]; then
  if npx stryker --version &>/dev/null; then
    npx stryker run 2>&1
  else
    echo "[INFO] Stryker not installed."
    echo "Setup: npm install --save-dev @stryker-mutator/core @stryker-mutator/jest-runner"
    echo "Then: npx stryker init"
  fi
else
  echo "[INFO] Mutation testing: install Stryker (JS), mutmut (Python), or go-mutesting (Go)"
fi
