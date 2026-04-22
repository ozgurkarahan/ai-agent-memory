---
title: Identity Propagation
category: patterns
tags: [azure, identity, auth, obo, tokens]
source_docs: []
date_created: 2026-04-03
date_updated: 2026-04-15
---

# Identity Propagation

## Summary

A pattern for forwarding user identity through multi-tier API architectures. The user authenticates once (at the SPA), and their identity flows through APIM → backend → downstream services without re-authentication at each layer.

## The Pattern

```
User (SPA)                    APIM                    Backend API              Downstream API
    │                          │                          │                          │
    │── Access Token (B2C) ──→ │                          │                          │
    │                          │── Validate JWT ──→       │                          │
    │                          │── Forward token ────→    │                          │
    │                          │   (set-header)           │── OBO exchange ─────→    │
    │                          │                          │   (new token)            │
    │                          │                          │←── Response ─────────    │
    │                          │←── Response ─────────    │                          │
    │←── Response ─────────    │                          │                          │
```

### Step 1: APIM Forwards the Token

APIM validates the JWT and passes it to the backend:

```xml
<inbound>
    <validate-jwt header-name="Authorization" ... />
    <!-- Token is already in Authorization header, just forward it -->
    <set-header name="X-User-Email" exists-action="override">
        <value>@(context.Request.Headers.GetValueOrDefault("Authorization","")
            .AsJwt()?.Claims.GetValueOrDefault("email", "unknown"))</value>
    </set-header>
</inbound>
```

### Step 2: Backend Exchanges via OBO

The backend uses the incoming token to request a new token for the downstream API:

```python
from msal import ConfidentialClientApplication

msal_app = ConfidentialClientApplication(
    client_id=BACKEND_CLIENT_ID,
    client_credential=BACKEND_CLIENT_SECRET,
    authority=f"https://login.microsoftonline.com/{TENANT_ID}",
)

def get_downstream_token(incoming_token: str) -> str:
    result = msal_app.acquire_token_on_behalf_of(
        user_assertion=incoming_token,
        scopes=[f"api://{DOWNSTREAM_APP_ID}/.default"],
    )
    if "error" in result:
        raise AuthError(f"OBO failed: {result['error_description']}")
    return result["access_token"]
```

### Step 3: Call Downstream API

```python
downstream_token = get_downstream_token(request.headers["Authorization"].split(" ")[1])
async with httpx.AsyncClient() as client:
    response = await client.get(
        f"{DOWNSTREAM_URL}/api/data",
        headers={"Authorization": f"Bearer {downstream_token}"},
    )
```

## When to Use

- Multi-tier architectures where downstream APIs need to know the user's identity
- Audit trail requirements — each service logs the actual user, not a service account
- Fine-grained authorization — downstream services enforce per-user permissions

## When NOT to Use

- Service-to-service calls where user identity is irrelevant → use managed identity instead
- Simple gateway patterns where APIM is the only auth boundary
- High-throughput scenarios where OBO token exchange latency is unacceptable (adds ~50-100ms per call)

## Common Mistakes

1. **Caching OBO tokens too aggressively** — OBO tokens have the same lifetime as the incoming token. Cache with a key of `(user_id, downstream_scope)` and respect the `expires_in` field.

2. **Missing API permissions** — The backend app registration needs the downstream API's permissions configured and admin-consented. Same pattern as [[partner-onboarding]]'s Graph API lesson.

3. **Confusing OBO with client credentials** — OBO preserves user context. Client credentials flow creates a token for the app itself, losing user identity.

## Projects Using This

- [[customer-portal]] — SPA → APIM → backend → downstream APIs
- [[partner-onboarding]] — managed identity variant for automation flows

## Related

- [[azure-entra-id]] — token types, auth flows, and managed identity
- [[azure-api-management]] — JWT validation and header forwarding policies
- [[api-auth-debugging]] — debugging auth failures in multi-tier setups

<!-- DEMO DATA: This content is fictional, created to demonstrate the wiki structure. -->
