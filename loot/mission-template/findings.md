# FINDINGS LOG — sample-webapp
# Update this file as findings are confirmed
# Format: add newest findings at the top of each severity section

---

## CRITICAL

### [F1] SQL Injection — /api/search Endpoint

- **Date found:** 2026-04-19
- **Asset:** https://api.acme.com/api/search
- **Tool:** HexStrike web profile (sqlmap via nuclei trigger)
- **Evidence:** screenshots/f1_sqli_auth_bypass.png
- **CVSS:** 9.8 (AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H)
- **CVE:** N/A (custom application)
- **CWE:** CWE-89 — SQL Injection
- **Status:** Confirmed / Exploited (retrieved 3 test rows, stopped)
- **Notes:** Parameter `q` is directly interpolated. MySQL backend. Error-based + UNION-based both work. Time-based blind also tested. Auth bypass possible with `' OR '1'='1`.

---

## HIGH

### [F2] Unauthenticated Swagger UI Exposes All API Endpoints

- **Date found:** 2026-04-17
- **Asset:** https://api.acme.com/api-docs
- **Tool:** Manual (found during OSINT review of subdomains)
- **Evidence:** screenshots/f2_swagger_exposed.png
- **CVSS:** 7.5 (AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N)
- **CVE:** N/A
- **CWE:** CWE-200 — Exposure of Sensitive Information
- **Status:** Confirmed
- **Notes:** Full Swagger UI accessible without authentication. Exposes 147 API endpoints including /admin/ paths. Allows API enumeration, parameter discovery, and reveals internal API structure. Several admin endpoints return 403 but their existence is now known.

---

## MEDIUM

### [F3] Missing Security Headers on All Responses

- **Date found:** 2026-04-18
- **Asset:** https://app.acme.com (all pages)
- **Tool:** HexStrike (nuclei missing-headers templates)
- **Evidence:** screenshots/f3_headers.png
- **CVSS:** 5.3 (AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N)
- **Status:** Confirmed
- **Notes:** Missing: X-Frame-Options (clickjacking), Content-Security-Policy (XSS defense), X-Content-Type-Options, Referrer-Policy. HSTS present but max-age is only 300 seconds (should be 31536000+).

---

## LOW

_No low findings yet._

---

## INFORMATIONAL

### [I1] Verbose Error Messages in API Responses

- **Date found:** 2026-04-18
- **Asset:** https://api.acme.com/api/users/9999
- **Evidence:** N/A (observed in traffic)
- **Status:** Documented
- **Notes:** 404 errors include stack trace and framework version (Express 4.18.2). Reduces attacker effort for fingerprinting. Not directly exploitable but aids attack planning.

---

*Update this file continuously — do not batch at end of engagement.*
*Each finding must have: date, asset, tool, evidence reference, status.*
