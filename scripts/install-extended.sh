#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
# install-extended.sh — optional extended AI tooling
# Clones PentestGPT, VulnGPT, STRIDE-GPT, AutoGPT alongside the
# core stack. All targets are git-ignored and installed on demand.
# ─────────────────────────────────────────────────────────────
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT" || exit 1

EXTENDED_REPOS=(
    "https://github.com/GreyDGL/PentestGPT.git|pentestgpt"
    "https://github.com/mrwadams/stride-gpt.git|stride-gpt"
    "https://github.com/Significant-Gravitas/AutoGPT.git|autogpt"
)

if ! command -v git >/dev/null 2>&1; then
    echo "[!] git is required for the extended install" >&2
    exit 1
fi

echo "[*] Installing extended AI tooling..."
for entry in "${EXTENDED_REPOS[@]}"; do
    url="${entry%%|*}"
    dir="${entry##*|}"
    if [[ -d "$dir/.git" ]]; then
        echo "[*] $dir already present — skipping"
        continue
    fi
    echo "[*] Cloning $dir..."
    git clone --depth 1 "$url" "$dir" || echo "[!] Could not clone $dir (continuing)"
done

echo "[+] Extended tooling install complete."
