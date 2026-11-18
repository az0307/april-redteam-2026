#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
# install.sh — base install for the April 2026 Red Team Stack
# Usage: ./scripts/install.sh [--full|--kali]
#   --full  clone core repos + prepare docker stack (default)
#   --kali  native Kali install path (apt install hexstrike-ai)
# ─────────────────────────────────────────────────────────────
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT" || exit 1

MODE="--full"
[[ $# -gt 0 ]] && MODE="$1"

# Core repositories installed alongside this stack (git-ignored).
CORE_REPOS=(
    "https://github.com/0x4m4/hexstrike-ai.git|hexstrike-ai"
)

require() {
    command -v "$1" >/dev/null 2>&1 || {
        echo "[!] Missing required tool: $1" >&2
        return 1
    }
}

prepare_env() {
    if [[ ! -f .env ]]; then
        cp .env.example .env
        echo "[+] Created .env from .env.example — fill in secrets before 'make start'"
    else
        echo "[*] .env already present — leaving untouched"
    fi
}

clone_repos() {
    for entry in "${CORE_REPOS[@]}"; do
        local url="${entry%%|*}" dir="${entry##*|}"
        if [[ -d "$dir/.git" ]]; then
            echo "[*] $dir already cloned — skipping"
        else
            echo "[*] Cloning $dir..."
            git clone --depth 1 "$url" "$dir" || echo "[!] Could not clone $dir (continuing)"
        fi
    done
}

case "$MODE" in
    --full)
        echo "[*] Full install: docker stack + core repos"
        require git || exit 1
        require docker || echo "[!] docker not found — install Docker to run the stack"
        prepare_env
        clone_repos
        echo "[+] Base install complete. Next: edit .env, then 'make start'."
        ;;
    --kali)
        echo "[*] Native Kali install path"
        if require apt-get 2>/dev/null; then
            echo "[*] Run: sudo apt-get update && sudo apt-get install -y hexstrike-ai"
        else
            echo "[!] apt-get not available — this path targets Kali/Debian only" >&2
        fi
        prepare_env
        ;;
    *)
        echo "Usage: $0 [--full|--kali]" >&2
        exit 1
        ;;
esac
