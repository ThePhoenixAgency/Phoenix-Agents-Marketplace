#!/bin/bash
# Command: pr-create
# Created: 2026-02-18
set -euo pipefail
BRANCH=$(git branch --show-current)
BASE=${1:-main}
echo "=== Creating PR ==="
echo "Branch: $BRANCH -> $BASE"
if [ "$BRANCH" = "$BASE" ]; then
  echo "[ERROR] Cannot create PR from $BASE to $BASE"
  exit 1
fi
COMMITS=$(git log "$BASE".."$BRANCH" --oneline 2>/dev/null || echo "")
if [ -z "$COMMITS" ]; then
  echo "[ERROR] No commits ahead of $BASE"
  exit 1
fi
echo "Commits:"
echo "$COMMITS"
echo ""
echo "Run: gh pr create --base $BASE --head $BRANCH --title '<type>(<scope>): <subject>'"
