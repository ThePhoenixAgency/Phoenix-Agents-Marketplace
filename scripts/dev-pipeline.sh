#!/usr/bin/env bash
set -euo pipefail

# Pipeline officiel issu de ~/.codex + AGENTS.override:
# preflight -> spec -> developpement -> tests -> audit-security
# -> validation humaine actions critiques -> deploiement -> verification post-deploiement

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

scripts/dev-pipeline/00_preflight.sh
scripts/dev-pipeline/10_spec_gate.sh
scripts/dev-pipeline/20_develop.sh
scripts/dev-pipeline/30_tests.sh
scripts/dev-pipeline/40_audit-security.sh
scripts/dev-pipeline/50_human-validation.sh
scripts/dev-pipeline/60_deploy.sh
scripts/dev-pipeline/70_post-deploy-verify.sh

echo "[OK] pipeline complet"
