#!/usr/bin/env bash
set -euo pipefail

echo "[PIPELINE] 50_human-validation"
if [[ "${PHOENIX_HUMAN_VALIDATED:-0}" != "1" ]]; then
  echo "[ERROR] human validation missing. Export PHOENIX_HUMAN_VALIDATED=1 to continue."
  exit 1
fi

echo "[OK] human validation"
