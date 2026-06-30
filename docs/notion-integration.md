# NOTION INTEGRATION — Red Team Stack
# April 2026 | AutoBoros / Az Command Center
# Sync pentest findings → Notion databases

---

## Overview

Connect the red team stack to Az's existing Notion setup:
- Az Command Center: `2f337887-0577-81a0-9b20-ca46e9754137`
- AutoBoros Command Center: `23c37887-0577-8107-ad14-f824899b91bd`

Sync flow:
```
loot/[MISSION]/findings.md → Notion Task Tracker
loot/[MISSION]/report.md   → Notion Document
Mission notes              → Notion Agent Activity Log
CVE watches                → Notion Dispatch Engine
```

---

## WORKFLOW 1 — Create Engagement in Notion

```
Using Notion MCP, create a new page under Az Command Center
for engagement [MISSION_NAME].
```

---

## WORKFLOW 2 — Sync Finding to Notion Task Tracker

```
Using Notion MCP, add task to Task Tracker database.
```

---

## Notion Page IDs Quick Reference

```
Az Command Center:        2f337887-0577-81a0-9b20-ca46e9754137
AutoBoros Command Center: 23c37887-0577-8107-ad14-f824899b91bd
```

---

*April 2026 | Notion integration — connect red team work to your command center*
