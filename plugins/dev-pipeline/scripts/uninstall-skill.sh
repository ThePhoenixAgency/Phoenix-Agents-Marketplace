#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_DIR="$HOME/.codex/skills/phoenix-orchestrator"

rm -rf "$SKILL_DIR"
rm -f "$REPO_DIR/PHOENIX_SKILL_LINK.md"

echo "[OK] Skill supprimée: $SKILL_DIR"
echo "[OK] Référence supprimée: $REPO_DIR/PHOENIX_SKILL_LINK.md"
