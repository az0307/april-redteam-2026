#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
# rotate-tokens.sh — regenerate secrets in .env
# Rotates API tokens and DB/service passwords in place, keeping a
# timestamped backup of the previous .env.
# ─────────────────────────────────────────────────────────────
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT" || exit 1

if [[ ! -f .env ]]; then
    echo "[!] No .env found. Run 'make install' first." >&2
    exit 1
fi

command -v openssl >/dev/null 2>&1 || { echo "[!] openssl is required." >&2; exit 1; }

# hex tokens vs base64 passwords
HEX_KEYS=(HEXSTRIKE_API_TOKEN KALI_MCP_TOKEN)
B64_KEYS=(KALI_PASSWORD POSTGRES_PASSWORD GRAFANA_PASSWORD)

backup=".env.bak.$(date +%Y%m%d-%H%M%S)"
cp .env "$backup"
echo "[*] Backed up current .env → $backup"

# Replace KEY=... with a freshly generated value. Only rotates keys
# that already exist in the file so we never introduce unknown vars.
rotate_key() {
    local key="$1" value="$2"
    if grep -qE "^${key}=" .env; then
        # Use a non-/ delimiter since base64 can contain '/'.
        sed -i "s|^${key}=.*|${key}=${value}|" .env
        echo "  [+] rotated ${key}"
    fi
}

for key in "${HEX_KEYS[@]}"; do
    rotate_key "$key" "$(openssl rand -hex 32)"
done
for key in "${B64_KEYS[@]}"; do
    rotate_key "$key" "$(openssl rand -base64 24)"
done

echo "[+] Token rotation complete."
echo "    Restart the stack to apply: make restart"
