---
title: Azure API Management
category: domains
tags: [azure, apim, api-gateway, policies]
source_docs: []
date_created: 2026-03-28
date_updated: 2026-04-15
---

# Azure API Management

## Summary

Azure API Management (APIM) is a managed API gateway for publishing, securing, and monitoring APIs. This page captures policies, patterns, and gotchas learned from [[customer-portal]] and [[partner-onboarding]] projects.

## Key Concepts

### Policy Scopes

Policies can be applied at four levels (evaluated in order):

```
Global (all-apis) → Product → API → Operation
```

Each scope has `<inbound>`, `<backend>`, `<outbound>`, and `<on-error>` sections.

### Common Policies

#### JWT Validation

```xml
<inbound>
    <validate-jwt header-name="Authorization" failed-validation-httpcode="401">
        <openid-config url="https://login.microsoftonline.com/{tenant}/v2.0/.well-known/openid-configuration" />
        <required-claims>
            <claim name="aud" match="all">
                <value>{client-id}</value>
            </claim>
        </required-claims>
    </validate-jwt>
</inbound>
```

#### Rate Limiting per Subscription

```xml
<inbound>
    <rate-limit-by-key calls="100" renewal-period="60" 
        counter-key="@(context.Subscription.Id)" />
</inbound>
```

#### Request Transformation

```xml
<inbound>
    <set-header name="X-Forwarded-For" exists-action="override">
        <value>@(context.Request.IpAddress)</value>
    </set-header>
    <set-header name="X-Request-ID" exists-action="skip">
        <value>@(Guid.NewGuid().ToString())</value>
    </set-header>
</inbound>
```

## Common Gotchas

### Header Casing

APIM normalizes header names in certain scenarios, but some legacy backends are case-sensitive. See [[apim-header-casing]] for the full debugging lesson.

**Rule**: Always test header handling end-to-end when integrating with legacy systems. Don't assume case-insensitive behavior.

### Policy Expression Limits

C# expressions in policies (`@(...)`) run in a sandboxed environment:
- No `System.IO` or filesystem access
- No `System.Net` (use `send-request` policy instead)
- 5-second execution timeout
- Limited assembly references

### Consumption Tier Limits

- 5 requests/second sustained throughput
- No VNet integration
- No custom domains on gateway
- Cold start latency (~1-2 seconds after idle)

**Lesson from [[customer-portal]]**: Hit 429 errors during a live demo due to consumption tier limits. Always use developer tier or higher for demos and load testing.

### CORS with APIM

CORS must be configured in APIM policy, **not** in the backend:

```xml
<inbound>
    <cors allow-credentials="true">
        <allowed-origins>
            <origin>https://portal.contoso.com</origin>
        </allowed-origins>
        <allowed-methods preflight-result-max-age="300">
            <method>GET</method>
            <method>POST</method>
        </allowed-methods>
        <allowed-headers>
            <header>Authorization</header>
            <header>Content-Type</header>
        </allowed-headers>
    </cors>
</inbound>
```

**Gotcha**: If CORS is configured in both APIM and the backend, you get duplicate CORS headers, which browsers reject.

## Subscription Management

For multi-tenant scenarios (like [[partner-onboarding]]):

1. Create an APIM **Product** per access tier (free, standard, premium)
2. Create a **Subscription** per partner, assigned to a product
3. Use `subscription-key` header or query param for auth
4. Combine with JWT validation for identity + access control

**Lesson**: Make subscription names deterministic (based on partner ID) to prevent duplicate creation during retries.

## Projects Using This

- [[customer-portal]] — API gateway for customer-facing portal
- [[partner-onboarding]] — automated APIM subscription provisioning

## Related

- [[azure-entra-id]] — JWT token validation in APIM policies
- [[identity-propagation]] — token forwarding through APIM
- [[apim-header-casing]] — header casing gotcha
- [[retry-with-backoff]] — client-side resilience when APIM returns 429

<!-- DEMO DATA: This content is fictional, created to demonstrate the wiki structure. -->
