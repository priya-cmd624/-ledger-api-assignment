# Task 4 – Reconnaissance & Penetration Testing Report

## Executive Summary

A security assessment was performed against the authorized target as described in the assessment instructions.

The engagement consisted of:

- Passive reconnaissance (OSINT)
- Web application security testing
- Verification of common OWASP Top 10 vulnerabilities

Testing was limited to the authorized target only.

---

# Scope

## Passive Reconnaissance

Target:

```
dodopayments.tech
```

Techniques used:

- Certificate Transparency Logs (crt.sh)
- Subfinder
- Assetfinder
- Amass
- HTTPX
- WhatWeb

No active attacks were performed during reconnaissance.

---

## Authorized Penetration Testing

Testing included:

- SSRF
- Broken Access Control / IDOR
- Security Misconfiguration
- Secrets Exposure
- Input Validation
- Error Handling

Testing was performed only against the authorized vulnerable target.

---

# Methodology

Reconnaissance:

- crt.sh
- subfinder
- assetfinder
- amass
- httpx
- whatweb

Application Testing:

- Manual testing
- Burp Suite Community Edition
- HTTP request analysis

---

# Findings

## Finding 1 – Server Side Request Forgery (SSRF)

Severity:
High

CVSS v3.1

```
CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N
```

Evidence:

```
evidence/ssrf-example.json
evidence/ssrf-internal.json
```

Impact

An attacker could force the application to access internal services that should not be publicly reachable.

Recommendation

Validate destination URLs.
Block internal IP ranges.
Implement outbound request filtering.

---

## Finding 2 – Sensitive Data Exposure

Severity

Medium

Evidence

```
transactions-redacted.json
```

Impact

Sensitive transaction information could be exposed if proper data masking is not implemented.

Recommendation

Mask sensitive information before returning responses.

---

## Finding 3 – Internal Server Error

Severity

Low

Evidence

```
import-500.txt
```

Impact

Unexpected server errors may disclose implementation details.

Recommendation

Implement centralized exception handling.
Return generic error responses.

---

# Reconnaissance Summary

Passive enumeration identified publicly accessible hosts and technologies.

Reconnaissance included:

- DNS enumeration
- Certificate Transparency logs
- HTTP technology fingerprinting
- Live host discovery

Evidence is available under:

```
task-4/recon/
```

---

# Recommendations

High Priority

- Prevent SSRF
- Restrict outbound connections
- Validate URLs

Medium Priority

- Redact sensitive information
- Improve access control

Low Priority

- Improve exception handling
- Hide stack traces

---

# Conclusion

The assessment successfully demonstrated passive reconnaissance techniques and authorized penetration testing against the designated target.

All testing was conducted within the permitted scope defined by the assessment.
