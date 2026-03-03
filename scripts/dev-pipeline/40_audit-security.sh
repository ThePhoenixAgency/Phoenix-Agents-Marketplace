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
    -e '-----BEGIN (RSA|EC|OPENSSH|DSA) PRIVATE KEY-----' . || true)"
fi

  echo "[ERROR] audit-security: secret pattern detected"
  FAIL=1
fi

# 2) Sensitive docs outside /private
SENSITIVE=$(find . -type f \( -iname '*THREAT*MODEL*' -o -iname '*VULNERABILITY*' -o -iname '*REMEDIATION*REPORT*' -o -iname '*AUDIT*REPORT*' \) \
  ! -path './private/*' ! -path './.git/*' 2>/dev/null || true)
if [[ -n "$SENSITIVE" ]]; then
  echo "[ERROR] audit-security: sensitive documents outside ./private"
  echo "$SENSITIVE"
  FAIL=1
fi

# 3) Unsafe perms for key-like files
while IFS= read -r kf; do
  perm=$(stat -f '%Mp%Lp' "$kf" 2>/dev/null || echo "")
  if [[ -n "$perm" ]] && [[ "$perm" =~ [2367][0-9][0-9]$ ]]; then
    echo "[WARNING] audit-security: potentially too open permissions: $kf ($perm)"
  fi
done < <(find . -type f \( -name '*.pem' -o -name '*.key' -o -name '.env' \) ! -path './.git/*' 2>/dev/null)

if [[ "$FAIL" -ne 0 ]]; then
  echo "[ERROR] audit-security: KO"
  exit 1
fi

echo "[OK] audit-security"
