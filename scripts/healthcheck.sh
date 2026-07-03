#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
# healthcheck.sh — check all red team stack services
# Exit non-zero if any critical service is unreachable.
# ─────────────────────────────────────────────────────────────
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT" || exit 1

# Load ports from .env if present (fall back to defaults).
HEXSTRIKE_API_URL="http://localhost:8888"
KALI_MCP_PORT="8000"
GRAFANA_PORT="3000"
PROMETHEUS_PORT="9090"
VULNGPT_PORT="8090"
STRIDE_GPT_PORT="8501"
if [[ -f .env ]]; then
    # shellcheck disable=SC1091
    set -a; . ./.env; set +a
fi

fail=0

check_http() {
    local name="$1" url="$2" critical="${3:-no}"
    if curl -sf -o /dev/null --max-time 5 "$url"; then
        printf '  [+] %-16s %s\n' "$name" "OK"
    else
        printf '  [-] %-16s %s\n' "$name" "unreachable ($url)"
        [[ "$critical" == "critical" ]] && fail=1
    fi
}

echo "[*] Red Team Stack — health check"

if command -v docker >/dev/null 2>&1; then
    echo "[*] Docker containers:"
    docker compose ps 2>/dev/null || echo "  (compose not running)"
fi

echo "[*] Service endpoints:"
check_http "HexStrike"   "${HEXSTRIKE_API_URL}/health"        critical
check_http "Kali MCP"    "http://localhost:${KALI_MCP_PORT}/" no
check_http "Grafana"     "http://localhost:${GRAFANA_PORT}/api/health" no
check_http "Prometheus"  "http://localhost:${PROMETHEUS_PORT}/-/healthy" no
check_http "VulnGPT"     "http://localhost:${VULNGPT_PORT}/"  no
check_http "STRIDE-GPT"  "http://localhost:${STRIDE_GPT_PORT}/" no

if [[ "$fail" -ne 0 ]]; then
    echo "[!] One or more critical services are down." >&2
    exit 1
fi
echo "[+] Health check complete."
