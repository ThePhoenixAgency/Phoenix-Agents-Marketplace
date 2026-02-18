#!/usr/bin/env bash
set -euo pipefail

echo "[PIPELINE] 70_post-deploy-verify"

if [[ -x scripts/doctor.sh ]]; then
  scripts/doctor.sh
fi

echo "[OK] post-deploy verify"
