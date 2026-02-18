#!/bin/bash
# Command: diagram
# Created: 2026-02-18
set -euo pipefail
echo "=== Architecture Diagram ==="
echo ""
echo "Project structure:"
if command -v tree &>/dev/null; then
  tree -L 3 -I 'node_modules|.git|coverage|dist' --dirsfirst 2>/dev/null
else
  find . -maxdepth 3 -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/coverage/*' | head -50
fi
