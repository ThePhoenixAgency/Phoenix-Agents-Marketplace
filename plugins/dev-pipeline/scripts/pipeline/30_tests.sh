#!/usr/bin/env bash
set -euo pipefail

echo "[PIPELINE] 30_tests"

if [[ -x scripts/run-tests.sh ]]; then
  scripts/run-tests.sh
else
  # Fallback: syntax check bash scripts
  while IFS= read -r f; do
    bash -n "$f"
  done < <(find scripts -type f -name "*.sh" | sort)
fi

echo "[OK] tests"
