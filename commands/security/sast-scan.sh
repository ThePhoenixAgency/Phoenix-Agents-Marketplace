#!/bin/bash
# Command: sast-scan (Static Application Security Testing)
# Created: 2026-02-18
set -euo pipefail
echo "=== SAST Scan ==="
echo ""
echo "[CHECK] SQL Injection patterns..."
SQLI=$(grep -rn "query.*\$\|query.*+\|execute.*+" --include="*.js" --include="*.ts" . 2>/dev/null | grep -v node_modules | grep -v '.test.' || true)
if [ -n "$SQLI" ]; then
  echo "  [WARNING] Potential SQL injection:"
  echo "$SQLI" | head -5
else
  echo "  [OK] No obvious SQL injection patterns"
fi
echo ""
echo "[CHECK] eval() usage..."
EVAL=$(grep -rn "eval(" --include="*.js" --include="*.ts" . 2>/dev/null | grep -v node_modules || true)
if [ -n "$EVAL" ]; then
  echo "  [WARNING] eval() detected:"
  echo "$EVAL" | head -5
else
  echo "  [OK] No eval() usage"
fi
echo ""
echo "[CHECK] Hardcoded secrets..."
SECRETS=$(grep -rn "password.*=.*['\"]" --include="*.js" --include="*.ts" . 2>/dev/null | grep -v node_modules | grep -v '.test.' || true)
if [ -n "$SECRETS" ]; then
  echo "  [WARNING] Possible hardcoded secrets:"
  echo "$SECRETS" | head -5
else
  echo "  [OK] No obvious hardcoded secrets"
fi
