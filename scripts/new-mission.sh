#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
# new-mission.sh — scaffold a new engagement under loot/<NAME>/
# Usage: ./scripts/new-mission.sh <NAME> <TARGET> <TYPE>
#   NAME    engagement slug (e.g. acme-webapp)
#   TARGET  primary target (domain / IP / CIDR)
#   TYPE    web | network | ad | ctf | osint | cloud | mobile
# ─────────────────────────────────────────────────────────────
set -euo pipefail

NAME="${1:-}"
TARGET="${2:-}"
TYPE="${3:-web}"

if [[ -z "$NAME" || -z "$TARGET" ]]; then
    echo "Usage: $0 <NAME> <TARGET> <TYPE>" >&2
    echo "Example: $0 acme-webapp app.acme.com web" >&2
    exit 1
fi

# Resolve repo root regardless of where the script is invoked from.
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MISSION_DIR="$ROOT/loot/$NAME"
TEMPLATE_DIR="$ROOT/loot/mission-template"

if [[ -d "$MISSION_DIR" ]]; then
    echo "[!] Mission already exists: $MISSION_DIR" >&2
    exit 1
fi

echo "[*] Creating mission: $NAME ($TYPE) → $TARGET"
mkdir -p "$MISSION_DIR"/{screenshots,scans,exploits,osint}

TODAY="$(date +%Y-%m-%d)"

# Seed mission.md from the template if present, otherwise a minimal header.
if [[ -f "$TEMPLATE_DIR/mission.md" ]]; then
    sed -e "s/sample-webapp/$NAME/g" \
        -e "/^# Status: TEMPLATE/d" \
        -e "/^# Run: make new-mission/d" \
        "$TEMPLATE_DIR/mission.md" > "$MISSION_DIR/mission.md"
else
    cat > "$MISSION_DIR/mission.md" <<EOF
# MISSION: $NAME
# Created: $TODAY

## Authorization
**Target:** $TARGET
**Type:** $TYPE
**Authorization ref:** FILL-IN (signed SOW / written approval required before testing)

## Scope
- In scope: $TARGET
- Out of scope: FILL-IN
EOF
fi

cat > "$MISSION_DIR/findings.md" <<EOF
# FINDINGS LOG — $NAME
# Created: $TODAY | Target: $TARGET | Type: $TYPE

## CRITICAL

## HIGH

## MEDIUM

## LOW

## INFO
EOF

echo "$TARGET" > "$MISSION_DIR/scope.txt"

echo "[+] Mission ready: loot/$NAME/"
echo "    Reminder: confirm written authorization before any active testing."
