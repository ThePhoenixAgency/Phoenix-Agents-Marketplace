#!/usr/bin/env bash
set -euo pipefail

echo "[PIPELINE] 10_spec_gate"

if ! rg -n "spec|specification|criteria|acceptance|validated" BACKLOG.md >/dev/null 2>&1; then
  echo "[ERROR] spec gate: no validated specification found in BACKLOG.md"
  exit 1
fi

echo "[OK] spec gate"
