#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_DIR="$HOME/.codex/skills/dev-pipeline"

mkdir -p "$SKILL_DIR"
cp -f "$REPO_DIR/skills/dev-pipeline/SKILL.md" "$SKILL_DIR/SKILL.md"

cat > "$REPO_DIR/PHOENIX_SKILL_LINK.md" <<'LINK'
# Phoenix Skill Link

This repository references the local skill:

`~/.codex/skills/dev-pipeline`

Clean uninstall:

`bash scripts/uninstall-skill.sh`
LINK

echo "[OK] Skill dev-pipeline installed in $SKILL_DIR"
echo "[INFO] Restart Codex to load the new skills."
