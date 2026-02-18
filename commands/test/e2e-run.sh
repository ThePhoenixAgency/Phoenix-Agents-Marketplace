#!/bin/bash
# Command: e2e-run
# Created: 2026-02-18
set -euo pipefail
echo "=== E2E Tests ==="
if [ -f "playwright.config.ts" ] || [ -f "playwright.config.js" ]; then
  npx playwright test 2>&1
elif [ -f "cypress.config.ts" ] || [ -f "cypress.config.js" ]; then
  npx cypress run 2>&1
else
  echo "[INFO] No E2E framework detected (Playwright/Cypress)"
  echo "Setup: npx playwright init"
fi
