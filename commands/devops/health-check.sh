#!/bin/bash
# Command: health-check
# Created: 2026-02-18
set -euo pipefail
URL=${1:-"http://localhost:3000/health"}
echo "=== Health Check: $URL ==="
echo ""
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$URL" 2>/dev/null || echo "000")
if [ "$RESPONSE" = "200" ]; then
  echo "[OK] Service is healthy (HTTP $RESPONSE)"
elif [ "$RESPONSE" = "000" ]; then
  echo "[ERROR] Service unreachable"
else
  echo "[WARNING] Unexpected response: HTTP $RESPONSE"
fi
echo ""
echo "Response time:"
curl -s -o /dev/null -w "  Connect: %{time_connect}s\n  TTFB: %{time_starttransfer}s\n  Total: %{time_total}s\n" "$URL" 2>/dev/null || echo "  (unavailable)"
