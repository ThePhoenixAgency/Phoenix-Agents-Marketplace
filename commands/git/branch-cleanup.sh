#!/bin/bash
# Command: branch-cleanup
# Created: 2026-02-18
# Description: Clean up local branches merged into main

set -euo pipefail

echo "[INFO] Local branches merged into main:"
git branch --merged main | grep -v '^\*' | grep -v 'main' | grep -v 'develop' || echo "  (none)"
echo ""
echo "[INFO] To delete: git branch --merged main | grep -v 'main' | xargs -r git branch -d"
