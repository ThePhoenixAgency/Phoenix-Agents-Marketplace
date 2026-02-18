#!/bin/bash
# Command: rollback
# Created: 2026-02-18
set -euo pipefail
echo "=== Rollback ==="
echo ""
echo "Recent deployments (tags):"
git tag --sort=-creatordate | head -5
echo ""
echo "To rollback:"
echo "  1. Identify the target version"
echo "  2. git checkout v<version>"
echo "  3. Build and deploy"
echo "  4. Verify health"
echo ""
echo "[WARNING] Document the reason in an incident report."
