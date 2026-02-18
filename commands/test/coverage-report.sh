#!/bin/bash
# Command: coverage-report
# Created: 2026-02-18
set -euo pipefail
echo "=== Coverage Report ==="
if [ -f "package.json" ]; then
  npm test -- --coverage 2>&1 || true
elif [ -f "pytest.ini" ] || [ -f "pyproject.toml" ]; then
  python -m pytest --cov=. --cov-report=term-missing 2>&1 || true
elif [ -f "go.mod" ]; then
  go test -coverprofile=coverage.out ./... && go tool cover -func=coverage.out 2>&1 || true
fi
