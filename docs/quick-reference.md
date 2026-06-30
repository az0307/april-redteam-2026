# QUICK REFERENCE — April 2026 Red Team Stack
# Field cheat sheet — everything in one place

---

## STACK STARTUP

```bash
make start          # Start all 9 Docker services
make health         # Verify all services responding
claude --dangerously-skip-permissions  # Launch Claude Code
```

---

## NEW MISSION

```bash
make new-mission NAME=client TARGET=target.com TYPE=web
# Types: web | network | ad | mobile | cloud | wireless | ctf | bugbounty | osint
```

---

## MCP SHORTCUTS

| Key | Server | Best For |
|-----|--------|--------|
| `hs` | HexStrike full | Any — 150+ tools |
| `web` | HexStrike web | Web apps, bug bounty |
| `net` | HexStrike network | Port scan, AD enum |
| `kali` | Kali SSH+PTY | Manual, MSF, shells |
| `think` | PentestThinkingMCP | Attack path MCTS |
| `pgpt` | PentestGPT | CTF autopilot |
| `vuln` | VulnGPT | CVE analysis |
| `threat` | STRIDE-GPT | Threat modeling |
| `crew` | PentestAgent | Multi-agent, memory |

---

## HASHCAT QUICK COMMANDS

```bash
# WPA2 — rockyou
hashcat -m 22000 hash.hc22000 rockyou.txt -w 1 -d 1 --force

# NTLM — instant
hashcat -m 1000 hashes.txt rockyou.txt -d 1 --force

# NetNTLMv2
hashcat -m 5600 hashes.txt rockyou.txt -r best64.rule -d 1 --force

# Kerberoast
hashcat -m 13100 hashes.txt rockyou.txt -r best64.rule -d 1 --force
```

---

## NMAP ESSENTIAL FLAGS

```bash
nmap -sV -sC --open [TARGET] -oA scans/nmap_svc
nmap -p- --min-rate 5000 [TARGET] -oA scans/nmap_full
nmap -sU --top-ports 100 [TARGET] -oA scans/nmap_udp
```

---

*April 2026 | Authorized testing only | 0x4m4/april-redteam-2026*
