#!/bin/bash
# Command: docker-build
# Created: 2026-02-18
set -euo pipefail
TAG=${1:-latest}
echo "=== Docker Build ==="
if [ ! -f "Dockerfile" ]; then
  echo "[ERROR] No Dockerfile found."
  echo "Create one with: docker init"
  exit 1
fi
echo "Building image with tag: $TAG"
docker build -t "$(basename $(pwd)):$TAG" . 2>&1
echo ""
echo "[OK] Image built: $(basename $(pwd)):$TAG"
echo "Run: docker run -p 3000:3000 $(basename $(pwd)):$TAG"
