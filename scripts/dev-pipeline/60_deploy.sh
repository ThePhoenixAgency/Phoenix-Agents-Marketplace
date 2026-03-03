#!/usr/bin/env bash
set -euo pipefail

echo "[PIPELINE] 60_deploy"
# Extension point: implement project-specific deployment logic.
# Examples: rsync to VPS, docker push, firebase deploy, etc.
echo "[OK] deploy stage (no deployment configured - extension point)"
