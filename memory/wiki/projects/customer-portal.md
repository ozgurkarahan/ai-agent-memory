---
title: Customer Portal
category: projects
tags: [azure, apim, entra-id, react, typescript, node]
source_docs: []
date_created: 2026-03-25
date_updated: 2026-04-15
---

# Customer Portal

## Summary

A React + Node.js customer portal that exposes internal APIs through Azure API Management. Customers authenticate via Azure Entra ID B2C, and the portal consumes backend microservices through APIM policies. Deployed to Azure App Service (frontend) and Azure Container Apps (backend).

## Architecture

```
Customer Browser → React SPA (App Service)
                      ↓
                  Azure APIM ──→ Backend APIs (Container Apps)
                      ↕               ↕
              Entra ID B2C      Azure SQL / Cosmos DB
              (auth tokens)     (customer data)
```

- **Frontend**: React 18 + TypeScript, Azure App Service
- **API Gateway**: Azure API Management (consumption tier)
- **Auth**: [[azure-entra-id]] B2C with MSAL.js
- **Backend**: Node.js microservices on Azure Container Apps
- **Data**: Azure SQL (relational), Cosmos DB (documents)

## Technical Reference

| Component | Detail |
|-----------|--------|
| Frontend | React 18, TypeScript 5.x, Vite |
| API Gateway | Azure API Management (consumption) |
| Auth | Entra ID B2C, MSAL.js 2.x |
| Backend | Node.js 20 LTS, Express |
| Database | Azure SQL, Cosmos DB |
| CI/CD | GitHub Actions → Azure |

### Key Files

- `frontend/src/auth/` — MSAL configuration and token handling
- `frontend/src/api/` — API client with token injection
- `backend/services/` — Express microservices
- `infra/bicep/` — Infrastructure as Code (Bicep templates)
- `apim/policies/` — APIM policy XML files

## Lessons Learned

### 2026-04-06 — APIM header casing breaks policy rewrites

APIM policy `<set-header>` was silently failing on the legacy backend because header names were case-sensitive on that backend but APIM normalizes them.

**Root cause**: The legacy backend expected `X-Customer-ID` (mixed case) but APIM was sending `x-customer-id` (lowercase). The `<set-header>` policy doesn't preserve casing in all scenarios.

**Fix**: Added explicit header normalization in the APIM policy before forwarding to the legacy backend.

**See also**: [[apim-header-casing]] for the full debugging lesson.

### 2026-04-10 — Token expiry caused silent 401s

The React SPA was caching tokens in sessionStorage but not checking `exp` before API calls. After 1 hour, users got silent 401 errors without being redirected to login.

**Root cause**: MSAL.js `acquireTokenSilent` was called once at login, but not before each API call. Expired tokens were sent to APIM, which returned 401.

**Fix**: Wrapped all API calls in a `getValidToken()` helper that calls `acquireTokenSilent` with `forceRefresh: true` when the token is within 5 minutes of expiry.

**See also**: [[azure-entra-id]] for token lifecycle patterns, [[identity-propagation]] for the OBO flow.

### 2026-04-15 — APIM rate limiting hit during demo

During a customer demo, the consumption-tier APIM hit the 5 requests/second rate limit, causing 429 errors visible to the audience.

**Fix**: Upgraded to developer tier for demo environments. Added [[retry-with-backoff]] on the frontend API client for graceful degradation.

**Lesson**: Always test with realistic load before demos. Consumption tier limits are strict.

## Decision Record

### Why APIM over direct backend calls

**Date**: 2026-03-25
**Decision**: Route all frontend API calls through [[azure-api-management]] instead of calling backend services directly.

**Rationale**:
- Centralized auth validation (JWT validation in APIM policy)
- Rate limiting and throttling per customer
- Request/response transformation without backend changes
- API versioning and deprecation management
- Analytics and monitoring dashboard

**Trade-off**: Added latency (~10-20ms) and another failure point. Worth it for security and operational control.

## Related

- [[azure-api-management]] — APIM patterns and policies used here
- [[azure-entra-id]] — B2C auth flow and token handling
- [[identity-propagation]] — token forwarding from SPA → APIM → backend
- [[apim-header-casing]] — header casing debugging lesson
- [[retry-with-backoff]] — resilience pattern used on frontend API client

<!-- DEMO DATA: This content is fictional, created to demonstrate the wiki structure. -->
