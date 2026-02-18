#!/usr/bin/env bash
set -euo pipefail

echo "[PIPELINE] 20_develop"
# Etape d'orchestration: l'implementation est faite avant ce pipeline.
# Ce gate valide juste l'existence d'un espace source.
if [[ ! -d src ]]; then
  echo "[ERROR] develop gate: dossier src absent"
  exit 1
fi

echo "[OK] develop gate"
