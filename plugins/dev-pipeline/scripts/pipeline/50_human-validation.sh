#!/usr/bin/env bash
set -euo pipefail

echo "[PIPELINE] 50_human-validation"
if [[ "${PHOENIX_HUMAN_VALIDATED:-0}" != "1" ]]; then
  echo "[ERROR] validation humaine manquante. Exporter PHOENIX_HUMAN_VALIDATED=1 pour continuer."
  exit 1
fi

echo "[OK] validation humaine"
