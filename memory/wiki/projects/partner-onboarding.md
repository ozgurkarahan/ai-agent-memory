---
title: Partner Onboarding
category: projects
tags: [azure, azure-functions, logic-apps, entra-id, automation]
source_docs: []
date_created: 2026-04-08
date_updated: 2026-04-18
---

# Partner Onboarding

## Summary

An automated partner onboarding workflow that provisions Azure resources, creates Entra ID app registrations, and configures API Management subscriptions for new partners. Built with Azure Functions (Python) and Logic Apps for orchestration, with a simple admin dashboard in React.

## Architecture

```
Admin Dashboard (React) → Azure Functions (Python)
                              ↓
                         Logic Apps Orchestration
                              ├─→ Create Entra ID App Registration
                              ├─→ Provision APIM Subscription + Product
                              ├─→ Create Azure Resource Group + RBAC
                              ├─→ Send Welcome Email (SendGrid)
                              └─→ Update Partner DB (Cosmos DB)
```

- **API**: Azure Functions v4 (Python 3.11), HTTP triggers
- **Orchestration**: Logic Apps (Standard) for multi-step provisioning
- **Identity**: [[azure-entra-id]] — creates app registrations via Microsoft Graph API
- **API Gateway**: [[azure-api-management]] — provisions partner subscriptions
- **Notifications**: SendGrid for welcome emails

## Technical Reference

| Component | Detail |
|-----------|--------|
| Runtime | Azure Functions v4, Python 3.11 |
| Orchestration | Logic Apps (Standard) |
| Identity | Microsoft Graph SDK for Python |
| API Gateway | APIM Management REST API |
| Database | Cosmos DB (partner records) |
| Email | SendGrid API |

### Key Files

- `functions/onboard/` — HTTP trigger for partner onboarding
- `functions/graph_client.py` — Microsoft Graph API wrapper
- `functions/apim_client.py` — APIM management operations
- `logic-apps/onboard-flow/` — Logic App workflow definition
- `infra/bicep/` — Bicep templates for infrastructure

## Lessons Learned

### 2026-04-12 — Graph API permissions confusion

Creating app registrations via Microsoft Graph required `Application.ReadWrite.All` permission, but the initial setup only had `Application.Read.All`. The error message was cryptic: `Authorization_RequestDenied` with no detail about which permission was missing.

**Root cause**: Insufficient Graph API permissions on the managed identity. The Azure Function's managed identity needed admin-consented application permissions, not delegated.

**Fix**: Added `Application.ReadWrite.All` as an application permission (not delegated) and ran admin consent via `az ad app permission admin-consent`.

**Lesson**: Always check the difference between delegated and application permissions for Graph API. Managed identities can only use application permissions.

### 2026-04-18 — Logic App retry storm on APIM provisioning

The Logic App retried a failed APIM subscription creation 10 times with no backoff, creating 10 duplicate subscriptions for the same partner.

**Root cause**: Default Logic App retry policy is "fixed interval, 4 retries" but the APIM management API returned 500 on a transient error, and each retry succeeded (creating a new subscription each time) because the API wasn't idempotent.

**Fix**: Added a check-before-create step in the Logic App. Also added [[retry-with-backoff]] configuration in the Logic App retry policy and made the subscription name deterministic (partner ID-based) so duplicates are rejected.

**Lesson**: Retry is only safe for idempotent operations. For create operations, always check-then-create or use deterministic identifiers.

## Related

- [[azure-entra-id]] — app registration and managed identity patterns
- [[azure-api-management]] — subscription provisioning
- [[identity-propagation]] — managed identity token flow
- [[retry-with-backoff]] — retry patterns (applied to Logic Apps here)
- [[customer-portal]] — sibling project, shares APIM and Entra ID patterns

<!-- DEMO DATA: This content is fictional, created to demonstrate the wiki structure. -->
