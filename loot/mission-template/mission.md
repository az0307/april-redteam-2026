# MISSION: sample-webapp
# Status: TEMPLATE — copy this structure for new engagements
# Run: make new-mission NAME=client TARGET=target.com TYPE=web

---

## Authorization

**Client:** Acme Corp Pty Ltd
**Contact:** Jane Smith (CISO) — jane@acme.com — +61 4XX XXX XXX
**Emergency stop:** John Ops (IT Manager) — john@acme.com — +61 4XX XXX XXX
**Authorization ref:** PO-2026-0042 / Signed SOW dated 2026-04-01
**Get-out-of-jail letter:** auth_letter.pdf (carry at all times if on-site)

---

## Scope

### In Scope

| Asset | Type | Notes |
|-------|------|-------|
| app.acme.com | Web app | Main SaaS product |
| api.acme.com | API | REST + GraphQL |
| *.acme.com | Subdomains | All subdomains |
| 203.0.113.0/28 | IP range | Confirmed Acme range |

### Out of Scope

| Asset | Reason |
|-------|--------|
| acme.atlassian.net | Third-party, no authorization |
| acme.slack.com | Third-party, no authorization |
| partners.acme.com | Not covered in SOW |

### Rules of Engagement

- Testing window: Mon–Fri 0800–1800 AEST (business hours)
- Rate limiting: max 100 requests/second to any single host
- Destructive testing: NOT permitted (no drop/delete/format)
- Data exfiltration: PoC only — do not retain actual PII
- Social engineering: OUT OF SCOPE for this engagement
- Emergency stop: call John Ops immediately, suspend all testing

---

## Timeline

| Phase | Date | Status |
|-------|------|--------|
| Kickoff call | 2026-04-15 | Complete |
| OSINT + recon | 2026-04-16–17 | In progress |
| Vulnerability scan | 2026-04-18 | Planned |
| Manual testing | 2026-04-19–22 | Planned |
| Exploitation | 2026-04-23 | Planned |
| Report draft | 2026-04-25 | Planned |
| Report delivery | 2026-04-28 | Planned |

---

## Stack Config for This Mission

```json
{
  "scope": ["app.acme.com", "api.acme.com", "*.acme.com", "203.0.113.0/28"],
  "out_of_scope": ["acme.atlassian.net", "acme.slack.com"],
  "rate_limit": "100/s",
  "destructive": false,
  "social_eng": false,
  "type": "web"
}
```

---

## Key Findings (Updated Continuously)

| ID | Title | Severity | Asset | Status |
|----|-------|----------|-------|--------|
| F1 | [Example: SQL injection on /search] | Critical | api.acme.com | New |
| F2 | [Example: Subdomain takeover dev.acme.com] | High | dev.acme.com | New |

---

## Notes

_Running notes — updated throughout engagement._

**2026-04-16:** Passive OSINT complete. Found 47 subdomains via crt.sh.
Tech stack confirmed: React frontend, Node.js backend, AWS hosting.

**2026-04-17:** Active recon started. 12 live subdomains, 3 interesting.
dev.acme.com returns different errors — possible debug mode.
api.acme.com has Swagger UI exposed at /api-docs (no auth).
