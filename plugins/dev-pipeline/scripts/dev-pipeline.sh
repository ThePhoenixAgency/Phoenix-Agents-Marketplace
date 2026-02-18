#!/usr/bin/env bash
set -euo pipefail

# Pipeline officiel issu de ~/.codex + AGENTS.override:
# preflight -> spec -> developpement -> tests -> audit-security
# -> validation humaine actions critiques -> deploiement -> verification post-deploiement

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

scripts/pipeline/00_preflight.sh
scripts/pipeline/10_spec_gate.sh
scripts/pipeline/20_develop.sh
scripts/pipeline/30_tests.sh
scripts/pipeline/40_audit-security.sh
scripts/pipeline/50_human-validation.sh
scripts/pipeline/60_deploy.sh
scripts/pipeline/70_post-deploy-verify.sh

echo "[OK] pipeline complet"
