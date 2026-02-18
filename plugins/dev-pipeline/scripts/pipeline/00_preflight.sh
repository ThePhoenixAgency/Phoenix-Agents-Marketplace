#!/usr/bin/env bash
set -euo pipefail

echo "[PIPELINE] 00_preflight"

for p in BACKLOG.md scripts docs; do
  if [[ ! -e "$p" ]]; then
    echo "[ERROR] preflight: element requis absent: $p"
    exit 1
  fi
done

if ! command -v git >/dev/null 2>&1; then
  echo "[ERROR] preflight: git requis"
  exit 1
fi

echo "[OK] preflight"
