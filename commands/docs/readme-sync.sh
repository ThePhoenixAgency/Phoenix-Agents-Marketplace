#!/bin/bash
# Command: readme-sync
# Created: 2026-02-18
set -euo pipefail
echo "=== README Sync Check ==="
echo ""
if [ ! -f "README.md" ]; then
  echo "[ERROR] No README.md found."
  exit 1
fi
echo "[CHECK] README sections..."
for section in "Installation" "Usage" "Contributing" "License"; do
  if grep -qi "$section" README.md; then
    echo "  [OK] $section"
  else
    echo "  [MISSING] $section"
  fi
done
echo ""
echo "[CHECK] Package name matches..."
if [ -f "package.json" ]; then
  PKG_NAME=$(jq -r '.name' package.json 2>/dev/null || echo "")
  if grep -q "$PKG_NAME" README.md 2>/dev/null; then
    echo "  [OK] Package name '$PKG_NAME' found in README"
  else
    echo "  [WARNING] Package name '$PKG_NAME' not mentioned in README"
  fi
fi
