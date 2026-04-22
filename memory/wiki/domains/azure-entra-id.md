---
title: Azure Entra ID
category: domains
tags: [azure, identity, auth, oauth, tokens]
source_docs: []
date_created: 2026-04-02
date_updated: 2026-04-18
---

# Azure Entra ID

## Summary

Azure Entra ID (formerly Azure Active Directory) is Microsoft's cloud identity platform. This page covers auth flows, token handling, and managed identity patterns used across projects.

## Auth Flows

### SPA with B2C (Authorization Code + PKCE)

Used in [[customer-portal]]:

```
Browser → B2C Login Page → Auth Code → Token Endpoint → Access Token + Refresh Token
```

MSAL.js configuration:
```typescript
const msalConfig = {
  auth: {
    clientId: "{app-client-id}",
    authority: "https://{tenant}.b2clogin.com/{tenant}.onmicrosoft.com/{policy}",
    redirectUri: "https://portal.contoso.com",
    knownAuthorities: ["{tenant}.b2clogin.com"],
  },
  cache: {
    cacheLocation: "sessionStorage",  // Not localStorage — security
    storeAuthStateInCookie: false,
  },
};
```

**Gotcha**: Always use `sessionStorage`, not `localStorage`. Tokens in localStorage persist across tabs and survive browser close, increasing XSS risk.

### Managed Identity (System-Assigned)

Used in [[partner-onboarding]] for Azure Functions calling Graph API:

```python
from azure.identity import DefaultAzureCredential
from msgraph import GraphServiceClient

credential = DefaultAzureCredential()
graph_client = GraphServiceClient(credential)
```

**Key rule**: Managed identities use **application permissions** (not delegated). You must:
1. Add the app permission in the Entra ID portal
2. Run admin consent: `az ad app permission admin-consent --id {app-id}`
3. Wait 1-5 minutes for propagation

### On-Behalf-Of (OBO) Flow

Used in [[identity-propagation]] pattern — the backend exchanges the user's token for a new token to call downstream APIs:

```
SPA token → APIM (validates) → Backend (exchanges via OBO) → Downstream API
```

See [[identity-propagation]] for implementation details.

## Token Lifecycle

### Token Types

| Token | Lifetime | Usage |
|-------|----------|-------|
| Access Token | 60-90 min (default) | API authorization |
| Refresh Token | 24 hours (SPA), 90 days (confidential) | Renewing access tokens |
| ID Token | 60 min | User identity claims |

### Common Token Mistakes

1. **Not refreshing before expiry** — Call `acquireTokenSilent` before every API call, not just once at login. Discovered in [[customer-portal]].

2. **Wrong audience (`aud`) claim** — The access token's `aud` must match the API's app registration client ID, not the SPA's. Mismatched `aud` causes 401 at APIM JWT validation.

3. **Confusing v1.0 and v2.0 endpoints** — B2C uses v2.0 exclusively. Mixing endpoints causes `invalid_grant` errors.

## Graph API Permissions Cheat Sheet

| Operation | Permission | Type |
|-----------|-----------|------|
| Read user profile | `User.Read` | Delegated |
| Create app registration | `Application.ReadWrite.All` | Application |
| Manage groups | `Group.ReadWrite.All` | Application |
| Send email | `Mail.Send` | Delegated or Application |

**Lesson from [[partner-onboarding]]**: `Authorization_RequestDenied` errors are almost always a permission type mismatch (delegated vs application). Check this first.

## Projects Using This

- [[customer-portal]] — B2C authentication for customer-facing portal
- [[partner-onboarding]] — managed identity for Graph API and resource provisioning

## Related

- [[azure-api-management]] — JWT validation policies using Entra ID tokens
- [[identity-propagation]] — OBO flow for multi-tier architectures
- [[api-auth-debugging]] — general auth debugging patterns

<!-- DEMO DATA: This content is fictional, created to demonstrate the wiki structure. -->
