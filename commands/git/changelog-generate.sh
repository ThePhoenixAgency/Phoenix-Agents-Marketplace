#!/bin/bash
# Command: changelog-generate
# Created: 2026-02-18
set -euo pipefail
echo "=== Changelog Generator ==="
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
if [ -z "$LAST_TAG" ]; then
  echo "No tags found. Generating from all commits."
  RANGE=""
else
  echo "Since: $LAST_TAG"
  RANGE="${LAST_TAG}..HEAD"
fi
echo ""
echo "## [Unreleased]"
echo ""
echo "### Features"
git log $RANGE --pretty=format:"- %s" --grep="^feat" 2>/dev/null || echo "  (none)"
echo ""
echo "### Fixes"
git log $RANGE --pretty=format:"- %s" --grep="^fix" 2>/dev/null || echo "  (none)"
echo ""
echo "### Security"
git log $RANGE --pretty=format:"- %s" --grep="^security" 2>/dev/null || echo "  (none)"
echo ""
echo "### Other"
git log $RANGE --pretty=format:"- %s" --grep="^chore\|^docs\|^style\|^refactor\|^perf\|^test" 2>/dev/null || echo "  (none)"
