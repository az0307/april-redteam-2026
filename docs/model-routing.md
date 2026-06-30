# MODEL ROUTING — April 2026 Red Team Stack
# When to use which model — decision tree + cost math

---

## The Core Question: Accuracy vs Cost

```
DECISION TREE

Is this task reasoning-critical?
  → Novel exploit design, complex attack chain, final report?
  YES → Claude Opus ($0.015/1k in)

Is this standard orchestration?
  → Tool output parsing, recon analysis, skill execution?
  YES → Claude Sonnet ($0.003/1k in) [80% of all calls]

Is this bulk data processing?
  → Log files, scan dumps, 50k+ token inputs?
  YES → DeepSeek ($0.00027/1k in) [37x cheaper than GPT-4o]

Is this sensitive or offline?
  → Real PII, patient data, lab without internet?
  YES → Ollama local ($0/1k in) [zero egress, free]
```

---

## Detailed Routing Table

| Task | Model | Why | Est. Cost |
|------|-------|-----|----------|
| Attack path planning (MCTS input) | Opus | Multi-step logic chains | $0.05–0.20 |
| Novel exploit chain design | Opus | Creative reasoning | $0.10–0.50 |
| Report — executive summary | Opus | Nuanced language | $0.10–0.30 |
| Orchestrate MCP tool calls | Sonnet | Deterministic, fast, cheap | $0.01–0.05 |
| Parse nmap / nuclei output | Sonnet | Pattern recognition | $0.01–0.03 |
| CVE analysis (VulnGPT) | Sonnet | Structured lookup | $0.02–0.08 |
| AutoGPT OSINT monitoring | DeepSeek | 24/7 background, cost matters | $0.01–0.05/hr |
| Bulk log analysis (>50k tok) | DeepSeek | Context window + cost | $0.01–0.10 |
| Sensitive data (PII) | Ollama | Zero egress | $0 |

---

*April 2026 | Route smart — full Opus everywhere wastes money*
