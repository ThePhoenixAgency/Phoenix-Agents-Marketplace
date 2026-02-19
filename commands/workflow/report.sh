#!/bin/bash
# Command: report (workflow)
# Created: 2026-02-18
set -euo pipefail
echo "=== Phoenix Compliance Report ==="
echo "Generated: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
echo ""

echo "## 1. Tests"
if [ -f "package.json" ]; then
  npx jest --coverage --silent 2>&1 | grep -E "Tests:|Test Suites:|Stmts|Lines" || echo "  N/A"
fi
echo ""

echo "## 2. Security"
echo "  Secrets in code:"
SECRETS=$(grep -rnE "(password|secret|api.?key)\s*=\s*['\"]" --include="*.js" --include="*.ts" . 2>/dev/null | grep -v node_modules | grep -v '.test.' | wc -l | tr -d ' ' || echo "0")
echo "    Found: $SECRETS"
echo ""

echo "## 3. Documentation"
TOTAL_EXPORTS=$(grep -rl "module\.exports\|export " --include="*.js" . 2>/dev/null | grep -v node_modules | grep -v '.test.' | wc -l | tr -d ' ')
TOTAL_JSDOC=$(grep -rl "/\*\*" --include="*.js" . 2>/dev/null | grep -v node_modules | grep -v '.test.' | wc -l | tr -d ' ')
echo "  Files with exports: $TOTAL_EXPORTS"
echo "  Files with JSDoc: $TOTAL_JSDOC"
echo ""

echo "## 4. Accessibility"
echo "  WCAG audit: Run \`npx pa11y-ci\` manually"
echo ""

echo "## 5. Performance"
echo "  Lighthouse: Run \`npx lhci autorun\` manually"
echo ""

echo "## 6. Code Quality"
echo "  console.log count: $(grep -rn 'console\.log' --include="*.js" --include="*.ts" . 2>/dev/null | grep -v node_modules | grep -v '.test.' | grep -v coverage | wc -l | tr -d ' ' || echo "0")"
echo "  TODO count: $(grep -rn 'TODO:' --include="*.js" --include="*.ts" . 2>/dev/null | grep -v node_modules | wc -l | tr -d ' ' || echo "0")"
