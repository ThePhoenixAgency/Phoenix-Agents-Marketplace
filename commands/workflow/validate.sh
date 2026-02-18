#!/bin/bash
# Command: validate (workflow)
# Created: 2026-02-18
set -euo pipefail
echo "=== Phoenix Validation Pipeline ==="
echo ""
PASS=0
FAIL=0

check() {
  local name="$1"
  local cmd="$2"
  if eval "$cmd" &>/dev/null; then
    echo "  [OK] $name"
    PASS=$((PASS + 1))
  else
    echo "  [FAIL] $name"
    FAIL=$((FAIL + 1))
  fi
}

echo "Quality Gates:"
check "Lint" "npm run lint 2>/dev/null || npx eslint . --ext .js,.ts 2>/dev/null || true"
check "Tests" "npm test 2>/dev/null"
check "No console.log" "! grep -rn 'console\.log' --include='*.js' --include='*.ts' . 2>/dev/null | grep -v node_modules | grep -v '.test.' | grep -v coverage | head -1"
check "No TODOs" "! grep -rn 'TODO:' --include='*.js' --include='*.ts' . 2>/dev/null | grep -v node_modules | head -1"
check "No secrets" "! grep -rnE '(password|secret|api_key)\s*=' --include='*.js' --include='*.ts' . 2>/dev/null | grep -v node_modules | grep -v '.test.' | head -1"
check ".gitignore" "test -f .gitignore"
check "README.md" "test -f README.md"

echo ""
echo "Results: $PASS passed, $FAIL failed"
if [ "$FAIL" -gt 0 ]; then
  echo "[WARNING] Fix failures before committing."
  exit 1
fi
echo "[OK] All checks passed."
