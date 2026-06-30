# ARCHITECTURE — April 2026 Red Team Stack
# Full system design, data flows, and component relationships

---

## System Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    OPERATOR (Claude Code)                            │
│            claude --dangerously-skip-permissions                     │
│                                                                      │
│   CLAUDE.md loaded → 9 MCP servers available → playbooks indexed    │
└──────────────────────────────┴──────────────────────────────────────┘
                               │  MCP protocol
              ┌────────────────┼────────────────┐
              │                │                │
     ┌────────▼───────┐ ┌──────▼─────┐ ┌─────▼────────┐
     │  HEXSTRIKE AI   │ │  KALI MCP   │ │ PENTEST-THINK  │
     │  v6.0 :8888/89  │ │  :8000/2222 │ │ MCTS+BeamSearch│
     │  150+ tools     │ │  SSH+PTY    │ │ Attack Planning │
     │  12 agents      │ │  14 tools   │ │                │
     └────────┬────────┘ └──────┬─────┘ └─────┬────────┘
              │                 │               │
     ┌────────▼────────┐        │     ┌─────────▼──────────┐
     │   TOOL LAYER    │        │     │   PENTESTGPT        │
     │  nmap nuclei    │        │     │  Task Tree Reasoning │
     │  sqlmap ffuf    │        │     │  86.5% XBOW success │
     │  crackmapexec   │        │     │  Autonomous CTF     │
     │  metasploit     │◄───────┘     └─────────────────────┘
     │  gobuster...    │
     └─────────────────┘

     ┌─────────────────┐ ┌────────────┐ ┌──────────────────┐
     │   VULNGPT v2    │ │ STRIDE-GPT   │ │  PENTESTAGENT    │
     │   :8090         │ │ :8501        │ │  (crew mode)     │
     │   CVE analysis  │ │ STRIDE model │ │  Shadow Graph    │
     │   Shodan intel  │ │ threat model │ │  RAG memory      │
     │   NVD queries   │ │              │ │  Multi-agent     │
     └────────┬────────┘ └──────┬───────┘ └──────┬───────────┘
              │                 │                     │
     ┌────────▼─────────────────▼─────────────────────▼───────┐
     │                  PERSISTENCE LAYER                       │
     │  PostgreSQL :5432 — scan history, findings, credentials  │
     │  Redis :6379      — LRU scan cache (30-day retention)   │
     └────────────────────────────────────────────────────────┘

     ┌────────────────────────────────────────────────────────┐
     │               BACKGROUND INTELLIGENCE                   │
     │                                                        │
     │  AutoGPT (170k stars)                                  │
     │  ├── Passive OSINT (overnight, no noise)               │
     │  ├── CVE feed monitoring (daily)                       │
     │  ├── Target change detection (2h cadence)              │
     │  └── Report assembly from loot/                        │
     └────────────────────────────────────────────────────────┘
```

---

*April 2026 | Architecture designed for: authorized pentesting, CTF, security research*
