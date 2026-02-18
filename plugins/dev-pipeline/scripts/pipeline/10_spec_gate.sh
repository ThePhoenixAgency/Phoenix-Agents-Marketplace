#!/usr/bin/env bash
set -euo pipefail

echo "[PIPELINE] 10_spec_gate"

if ! rg -n "spec|specification|criteres|acceptation|Plan ce soir" BACKLOG.md >/dev/null 2>&1; then
  echo "[ERROR] spec gate: aucun indicateur de spec validee trouve dans BACKLOG.md"
  exit 1
fi

echo "[OK] spec gate"
