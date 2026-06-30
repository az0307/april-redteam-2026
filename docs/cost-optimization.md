# COST OPTIMIZATION — April 2026 Red Team Stack
# How to run professional engagements for under $20

---

## Strategy 1 — Three-Tier Model Routing

```
TIER 1: Claude Opus       ~$0.015/1k   Premium reasoning only
TIER 2: Claude Sonnet     ~$0.003/1k   General orchestration (80% of calls)
TIER 3: DeepSeek          ~$0.00027/1k Bulk processing (37x cheaper than GPT-4o)
TIER 0: Ollama (local)    $0           Sensitive data, offline use
```

**Rule of thumb:**
- Anything reading tool output → Sonnet
- Anything reasoning from scratch → check if Sonnet is good enough first
- Long context (>50k tokens) → DeepSeek
- Client PII → Ollama

---

## Strategy 2 — Redis LRU Caching

HexStrike caches all tool invocations in Redis (24h TTL by default).

```bash
# Check cache hit rate:
docker exec rt-redis redis-cli info stats | grep 'keyspace_hits\|keyspace_misses'

# Typical cache hit rate after first scan: 60-80%
# This cuts repeat scan cost to near-zero
```

---

## Strategy 3 — AutoGPT with DeepSeek Backend

```bash
# .env — configure AutoGPT for cost efficiency:
AUTOGPT_FAST_LLM=deepseek-chat
AUTOGPT_SMART_LLM=deepseek-chat

# Monthly cost comparison (continuous monitoring, 1 target):
# GPT-4o:       ~$180/month
# Claude Sonnet: ~$45/month
# DeepSeek:      ~$5/month
```

---

## Per-Engagement Cost Breakdown

### Easy CTF (HackTheBox)
```
Total: ~$0.24
PentestGPT bench avg: ~$1.11
```

### Web App Pentest (1 day)
```
Total: ~$3.49
```

### Bug Bounty (8h)
```
Total: ~$3.40
```

---

*April 2026 | Smart routing = same quality, 5-10x lower cost*
