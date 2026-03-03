#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_DIR="$HOME/.codex/skills/dev-pipeline"

rm -rf "$SKILL_DIR"
rm -f "$REPO_DIR/PHOENIX_SKILL_LINK.md"

echo "[OK] Skill removed: $SKILL_DIR"
echo "[OK] Reference removed: $REPO_DIR/PHOENIX_SKILL_LINK.md"
