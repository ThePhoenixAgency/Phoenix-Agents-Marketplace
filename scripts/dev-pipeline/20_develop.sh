#!/usr/bin/env bash
set -euo pipefail

echo "[PIPELINE] 20_develop"
# Orchestration step: implementation is done before this pipeline.
# This gate only validates the existence of a source directory.
if [[ ! -d src ]]; then
  echo "[ERROR] develop gate: src directory missing"
  exit 1
fi

echo "[OK] develop gate"
