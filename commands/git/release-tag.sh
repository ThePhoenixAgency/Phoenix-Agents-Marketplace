#!/bin/bash
# Command: release-tag
# Created: 2026-02-18
set -euo pipefail
CURRENT=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")
echo "=== Release Tag ==="
echo "Current version: $CURRENT"
echo ""
echo "Commits since $CURRENT:"
git log "${CURRENT}..HEAD" --oneline 2>/dev/null || git log --oneline -10
echo ""
MAJOR=$(echo "$CURRENT" | sed 's/v//' | cut -d. -f1)
MINOR=$(echo "$CURRENT" | sed 's/v//' | cut -d. -f2)
PATCH=$(echo "$CURRENT" | sed 's/v//' | cut -d. -f3)
echo "Next versions:"
echo "  Patch: v${MAJOR}.${MINOR}.$((PATCH + 1))"
echo "  Minor: v${MAJOR}.$((MINOR + 1)).0"
echo "  Major: v$((MAJOR + 1)).0.0"
echo ""
echo "Run: git tag -a v<version> -m 'Release v<version>'"
