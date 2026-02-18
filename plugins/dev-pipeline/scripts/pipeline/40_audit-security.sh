#!/usr/bin/env bash
set -euo pipefail

echo "[PIPELINE] 40_audit-security"

FAIL=0

# 1) Secrets patterns in staged or working tree fallback
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  DIFF_CONTENT="$(git diff --cached || true)"
else
  DIFF_CONTENT=""
fi

if [[ -z "$DIFF_CONTENT" ]]; then
  DIFF_CONTENT="$(rg -n --hidden --glob '!**/.git/**' --glob '!node_modules/**' \
    -e 'AKIA[0-9A-Z]{16}' \
    -e 'ghp_[A-Za-z0-9]{36,}' \
    -e 'AIza[0-9A-Za-z_\-]{35}' \
    -e '-----BEGIN (RSA|EC|OPENSSH|DSA) PRIVATE KEY-----' . || true)"
fi

if rg -n "AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{36,}|AIza[0-9A-Za-z_\-]{35}|BEGIN (RSA|EC|OPENSSH|DSA) PRIVATE KEY" <<<"$DIFF_CONTENT" >/dev/null 2>&1; then
  echo "[ERROR] audit-security: pattern secret detecte"
  FAIL=1
fi

# 2) Sensitive docs outside /private
SENSITIVE=$(find . -type f \( -iname '*THREAT*MODEL*' -o -iname '*VULNERABILITY*' -o -iname '*REMEDIATION*REPORT*' -o -iname '*AUDIT*REPORT*' \) \
  ! -path './private/*' ! -path './.git/*' 2>/dev/null || true)
if [[ -n "$SENSITIVE" ]]; then
  echo "[ERROR] audit-security: documents sensibles hors ./private"
  echo "$SENSITIVE"
  FAIL=1
fi

# 3) Unsafe perms for key-like files
while IFS= read -r kf; do
  perm=$(stat -f '%Mp%Lp' "$kf" 2>/dev/null || echo "")
  if [[ -n "$perm" ]] && [[ "$perm" =~ [2367][0-9][0-9]$ ]]; then
    echo "[WARNING] audit-security: permission potentiellement trop ouverte: $kf ($perm)"
  fi
done < <(find . -type f \( -name '*.pem' -o -name '*.key' -o -name '.env' \) ! -path './.git/*' 2>/dev/null)

if [[ "$FAIL" -ne 0 ]]; then
  echo "[ERROR] audit-security: KO"
  exit 1
fi

echo "[OK] audit-security"
