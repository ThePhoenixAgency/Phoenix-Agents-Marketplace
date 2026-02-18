#!/bin/bash
# Command: branch-cleanup
# Created: 2026-02-18
# Description: Nettoyer les branches locales mergees

set -euo pipefail

echo "[INFO] Branches locales mergees dans main :"
git branch --merged main | grep -v '^\*' | grep -v 'main' | grep -v 'develop' || echo "  (aucune)"
echo ""
echo "[INFO] Pour supprimer : git branch --merged main | grep -v 'main' | xargs -r git branch -d"
