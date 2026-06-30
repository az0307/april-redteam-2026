# LOOT DIRECTORY — STRUCTURE & CONVENTIONS
# April 2026 Red Team Stack

This directory contains all engagement artifacts.
It is GIT-IGNORED — never commit this directory.

---

## Standard Structure Per Engagement

```
loot/
├── REPORT_TEMPLATE.md         ← Copy this for each new engagement
├── README.md                  ← This file
└── [ENGAGEMENT_NAME]/
    ├── mission.md             ← Scope, auth, timeline (new-mission.sh)
    ├── findings.md            ← Running findings log
    ├── report.md              ← Final report (from REPORT_TEMPLATE.md)
    ├── hosts.txt              ← Discovered hosts
    │
    ├── osint/                 ← AutoGPT passive intelligence
    │   ├── company_profile.md
    │   ├── employees.csv
    │   ├── github_secrets.md
    │   ├── subdomains_passive.txt
    │   └── cve_watch.md
    │
    ├── recon/                 ← HexStrike active recon outputs
    │   ├── subdomains.txt
    │   ├── live_hosts.txt
    │   ├── live_hosts_full.json
    │   ├── tech_stack.txt
    │   └── directories.txt
    │
    ├── scans/                 ← Raw tool outputs
    │   ├── nmap_services.xml
    │   ├── nmap_fullscan.gnmap
    │   ├── nuclei_output.json
    │   └── vulngpt_report.json
    │
    ├── threat_model/          ← STRIDE-GPT outputs
    │   ├── threat_model_pre.md
    │   ├── threat_model_correlation.md
    │   └── threat_model_final.md
    │
    ├── exploits/              ← Working PoC code
    │   ├── [finding_name].py
    │   └── README.md          ← What each exploit does, target, test date
    │
    ├── screenshots/           ← Evidence screenshots
    │   ├── finding_01_[name].png
    │   └── finding_02_[name].png
    │
    └── evidence/              ← Raw evidence files
        ├── burp_requests.xml
        ├── session_tokens.txt ← ENCRYPT THESE
        └── captured_data/     ← Sensitive — ENCRYPT EVERYTHING HERE
```

---

## Findings Log Format (findings.md)

```markdown
# Findings Log — [MISSION_NAME]
Last updated: [DATE]

## CRITICAL

### [F1] [FINDING TITLE]
- **Date found:** [DATE]
- **Asset:** [URL/IP:PORT]
- **Tool:** [HexStrike / Manual / PentestGPT]
- **Evidence:** screenshots/finding_01.png
- **Status:** [New / Exploited / Documented / Fixed]
- **Notes:** [Brief notes]

## HIGH
[...]

## MEDIUM
[...]
```

---

## Security Rules for Loot

```bash
# 1. Encrypt ALL credential files immediately after capture
gpg --symmetric --cipher-algo AES256 loot/[MISSION]/evidence/creds.txt
rm loot/[MISSION]/evidence/creds.txt

# 2. Verify nothing sensitive is in git
git status                # Should show nothing in loot/
git check-ignore -v loot/ # Should confirm git-ignored

# 3. Secure transfer to client (never email plaintext)
# Option A: Password-protected archive
zip -e -r client_report_$(date +%Y%m%d).zip loot/[MISSION]/report.md loot/[MISSION]/screenshots/

# Option B: Encrypted tar
tar -czf - loot/[MISSION]/ | gpg --symmetric > loot_$(date +%Y%m%d).tar.gz.gpg

# 4. Retention: destroy after contract period ends
shred -u loot/[MISSION]/evidence/*  # Secure delete
rm -rf loot/[MISSION]/
```

---

## Notes.json — PentestAgent Integration

PentestAgent writes to `loot/notes.json` automatically.
This is the Shadow Graph memory store.

```json
{
  "credentials": [
    {"host": "[IP]", "service": "ssh", "username": "admin", "source": "finding_01"}
  ],
  "vulnerabilities": [
    {"host": "[IP]", "vuln": "CVE-2024-XXXX", "confirmed": true, "timestamp": "..."}
  ],
  "findings": [
    {"id": "F1", "title": "...", "severity": "critical", "asset": "..."}
  ],
  "artifacts": [
    {"type": "shell", "host": "[IP]", "method": "webshell", "path": "/uploads/shell.php"}
  ]
}
```

This persists across sessions — PentestAgent remembers what was found
even if Claude Code is restarted.

---

*Keep this directory local. Keep it encrypted. Delete it when done.*
