#!/bin/bash
# Command: inline-variable
# Created: 2026-02-18
set -euo pipefail
echo "=== Inline Variable Helper ==="
echo ""
echo "Steps:"
echo "1. Find the variable declaration"
echo "2. Replace all usages with the expression"
echo "3. Remove the declaration"
echo "4. Run tests"
echo ""
echo "When to inline:"
echo "  - Variable used only once"
echo "  - Variable name doesn't add clarity"
echo "  - Expression is simple and readable"
