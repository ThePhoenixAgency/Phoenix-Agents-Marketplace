#!/bin/bash
# Command: jsdoc
# Created: 2026-02-18
set -euo pipefail
echo "=== JSDoc Generator ==="
if command -v npx &>/dev/null; then
  if [ -f "jsdoc.json" ]; then
    npx jsdoc -c jsdoc.json 2>&1
  else
    npx jsdoc -r ./scripts -d ./docs/api 2>&1 || echo "[INFO] Install: npm i -D jsdoc"
  fi
else
  echo "[ERROR] npx not found"
fi
