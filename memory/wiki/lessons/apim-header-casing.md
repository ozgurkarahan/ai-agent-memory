---
title: APIM Header Casing
category: lessons
tags: [azure, apim, debugging, headers, legacy]
source_docs: []
date_created: 2026-04-06
date_updated: 2026-04-06
---

# APIM Header Casing

## Summary

Azure API Management normalizes HTTP header names to lowercase in certain policy scenarios. This breaks integrations with legacy backends that expect specific header casing (e.g., `X-Customer-ID` vs `x-customer-id`).

## What Happened

In [[customer-portal]], the APIM `<set-header>` policy was adding a custom header `X-Customer-ID` for the legacy backend. The backend requires exact casing — but APIM was sending `x-customer-id` (lowercase).

The symptoms were confusing: the API call succeeded (HTTP 200) but the response was missing customer-specific data. The backend silently ignored the unrecognized lowercase header and returned default/empty data instead of an error.

## Debugging Steps

1. **Checked APIM trace** (`Ocp-Apim-Trace: true` header) — saw the header was present in the outbound request, but didn't notice the casing difference
2. **Checked backend logs** — backend logged "missing X-Customer-ID header" but we were looking for error codes, not log messages
3. **Used `curl` to call the backend directly** — with correct casing, it worked; with lowercase, it returned empty data
4. **Root cause identified**: APIM normalizes headers in the outbound pipeline

## The Fix

Used a `<set-header>` policy with explicit casing in the backend section, and added a backend-specific workaround:

```xml
<backend>
    <forward-request />
</backend>
<outbound>
    <!-- APIM may lowercase headers; the legacy backend needs exact casing -->
    <!-- Workaround: use a custom policy to set the header after forwarding -->
    <set-header name="X-Customer-ID" exists-action="override">
        <value>@(context.Variables.GetValueOrDefault<string>("customer-id"))</value>
    </set-header>
</outbound>
```

Alternative fix for the backend team (long-term): make the backend case-insensitive for header names, per HTTP/2 spec (RFC 7540 §8.1.2: header field names are lowercase).

## Rules

1. **Always test header casing end-to-end** when integrating APIM with legacy backends
2. **Don't assume case-insensitive headers** — HTTP/1.1 headers are technically case-insensitive, but legacy implementations often aren't
3. **Use APIM tracing** (`Ocp-Apim-Trace: true`) to inspect the exact headers sent to the backend
4. **Log missing headers on the backend** as errors, not warnings — silent data omission is harder to debug than a clear failure

## Related

- [[customer-portal]] — project where this was discovered
- [[azure-api-management]] — APIM patterns and policies
- [[api-auth-debugging]] — similar debugging methodology for auth issues

<!-- DEMO DATA: This content is fictional, created to demonstrate the wiki structure. -->
