#!/usr/bin/env bash
set -euo pipefail

echo "[DOCTOR] Phoenix"

df -h / | sed -n '1,2p'

echo "[OK] doctor run"
