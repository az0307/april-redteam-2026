#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
# backup.sh — archive + encrypt the loot directory
# Produces backups/loot-<timestamp>.tar.gz.gpg (AES-256, symmetric)
# Requires: tar, gpg. Passphrase via $BACKUP_PASSPHRASE or prompt.
# ─────────────────────────────────────────────────────────────
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT" || exit 1

if [[ ! -d loot ]]; then
    echo "[!] No loot/ directory to back up." >&2
    exit 1
fi

command -v gpg >/dev/null 2>&1 || { echo "[!] gpg is required." >&2; exit 1; }

mkdir -p backups
TS="$(date +%Y%m%d-%H%M%S)"
ARCHIVE="backups/loot-${TS}.tar.gz"
ENCRYPTED="${ARCHIVE}.gpg"

echo "[*] Archiving loot/ ..."
tar -czf "$ARCHIVE" loot/

echo "[*] Encrypting (AES-256) ..."
if [[ -n "${BACKUP_PASSPHRASE:-}" ]]; then
    gpg --batch --yes --symmetric --cipher-algo AES256 \
        --passphrase "$BACKUP_PASSPHRASE" -o "$ENCRYPTED" "$ARCHIVE"
else
    gpg --symmetric --cipher-algo AES256 -o "$ENCRYPTED" "$ARCHIVE"
fi

# Remove the plaintext archive once encrypted.
rm -f "$ARCHIVE"

echo "[+] Encrypted backup: $ENCRYPTED"
echo "    Decrypt with: gpg -d -o loot.tar.gz $ENCRYPTED"
