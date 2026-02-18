#!/bin/bash
# Command: logs-tail
# Created: 2026-02-18
set -euo pipefail
SERVICE=${1:-"app"}
LINES=${2:-50}
echo "=== Logs: $SERVICE (last $LINES lines) ==="
if docker ps --format '{{.Names}}' | grep -q "$SERVICE"; then
  docker logs --tail "$LINES" -f "$SERVICE" 2>&1
elif command -v journalctl &>/dev/null; then
  journalctl -u "$SERVICE" -n "$LINES" -f 2>&1
else
  echo "[INFO] No Docker container or systemd service named '$SERVICE' found."
  echo "Available Docker containers:"
  docker ps --format "  {{.Names}} ({{.Status}})" 2>/dev/null || echo "  (Docker not running)"
fi
