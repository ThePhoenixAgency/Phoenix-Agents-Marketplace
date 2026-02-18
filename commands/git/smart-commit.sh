#!/bin/bash
# Command: smart-commit
# Created: 2026-02-18
# Description: Commit avec message conventionnel auto-genere

set -euo pipefail

# Verifier qu'il y a des changements stages
if ! git diff --cached --quiet 2>/dev/null; then
  echo "[INFO] Staged changes detected"
else
  echo "[ERROR] No staged changes. Run 'git add' first."
  exit 1
fi

# Detecter le type de changement
CHANGED_FILES=$(git diff --cached --name-only)
TYPE="chore"

if echo "$CHANGED_FILES" | grep -qE '\.(test|spec)\.(js|ts|jsx|tsx|py|go|rs|swift)$'; then
  TYPE="test"
elif echo "$CHANGED_FILES" | grep -qE '\.md$'; then
  TYPE="docs"
elif echo "$CHANGED_FILES" | grep -qE '\.(css|scss|less)$'; then
  TYPE="style"
elif echo "$CHANGED_FILES" | grep -qE 'Dockerfile|docker-compose|\.yml$|\.yaml$'; then
  TYPE="chore"
fi

# Generer le scope a partir du dossier le plus modifie
SCOPE=$(echo "$CHANGED_FILES" | head -1 | xargs dirname | tr '/' '-')
if [ "$SCOPE" = "." ]; then
  SCOPE="root"
fi

echo "Type detected: $TYPE"
echo "Scope: $SCOPE"
echo "Files: $(echo "$CHANGED_FILES" | wc -l | xargs) files"
echo ""
echo "Suggested commit message:"
echo "$TYPE($SCOPE): describe your changes here"
echo ""
echo "Co-Authored-By: Gemini"
