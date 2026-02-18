#!/bin/bash
# Command: secrets-scan
# Created: 2026-02-18
# Description: Scanner les secrets potentiels dans le code

set -euo pipefail

echo "=== Secrets Scan ==="
echo ""

# Patterns de secrets courants
PATTERNS=(
  "password\s*=\s*['\"]"
  "api_key\s*=\s*['\"]"
  "API_KEY\s*=\s*['\"]"
  "secret\s*=\s*['\"]"
  "token\s*=\s*['\"]"
  "private_key"
  "BEGIN RSA PRIVATE KEY"
  "BEGIN OPENSSH PRIVATE KEY"
  "aws_access_key_id"
  "aws_secret_access_key"
)

FOUND=0
for pattern in "${PATTERNS[@]}"; do
  RESULTS=$(grep -rn --include="*.{js,ts,py,go,rs,swift,json,yaml,yml,env,cfg,conf}" "$pattern" . 2>/dev/null | grep -v node_modules | grep -v .git || true)
  if [ -n "$RESULTS" ]; then
    echo "[WARNING] Pattern: $pattern"
    echo "$RESULTS" | head -5
    echo ""
    FOUND=$((FOUND + 1))
  fi
done

if [ $FOUND -eq 0 ]; then
  echo "[OK] No secrets detected."
else
  echo "[WARNING] $FOUND patterns detected. Review above."
fi
