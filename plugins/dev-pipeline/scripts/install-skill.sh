#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_DIR="$HOME/.codex/skills/phoenix-orchestrator"

mkdir -p "$SKILL_DIR"
cp -f "$REPO_DIR/docs/SKILL.md" "$SKILL_DIR/SKILL.md"
cp -f "$REPO_DIR/docs/config.schema.json" "$SKILL_DIR/config.schema.json"
cp -f "$REPO_DIR/docs/commands.map.fr-en.yaml" "$SKILL_DIR/commands.map.fr-en.yaml"

cat > "$REPO_DIR/PHOENIX_SKILL_LINK.md" <<'LINK'
# Phoenix Skill Link

Ce repository reference la skill locale:

`~/.codex/skills/phoenix-orchestrator`

Desinstallation propre:

`bash scripts/uninstall-skill.sh`
LINK

echo "[OK] Skill installée dans $SKILL_DIR"
echo "[INFO] Redémarrer Codex pour charger les nouvelles skills."
