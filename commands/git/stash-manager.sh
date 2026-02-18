#!/bin/bash
# Command: stash-manager
# Created: 2026-02-18
set -euo pipefail
echo "=== Stash Manager ==="
STASHES=$(git stash list 2>/dev/null || echo "")
if [ -z "$STASHES" ]; then
  echo "[INFO] No stashes found."
else
  echo "Current stashes:"
  echo "$STASHES"
  echo ""
  echo "Commands:"
  echo "  git stash pop     -> Apply and remove latest"
  echo "  git stash apply   -> Apply but keep"
  echo "  git stash drop    -> Delete latest"
  echo "  git stash show -p -> Show diff of latest"
fi
