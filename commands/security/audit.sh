#!/bin/bash
# Command: audit
# Created: 2026-02-18
# Description: Scan de securite complet des dependances

set -euo pipefail

echo "=== Security Audit ==="
echo ""

# Node.js
if [ -f "package.json" ]; then
  echo "[CHECK] npm audit..."
  npm audit --audit-level=high 2>&1 || true
  echo ""
fi

# Python
if [ -f "requirements.txt" ]; then
  echo "[CHECK] pip-audit..."
  pip-audit -r requirements.txt 2>&1 || true
  echo ""
fi

# Go
if [ -f "go.mod" ]; then
  echo "[CHECK] govulncheck..."
  govulncheck ./... 2>&1 || true
  echo ""
fi

# Rust
if [ -f "Cargo.toml" ]; then
  echo "[CHECK] cargo audit..."
  cargo audit 2>&1 || true
  echo ""
fi

echo "=== Audit Complete ==="
