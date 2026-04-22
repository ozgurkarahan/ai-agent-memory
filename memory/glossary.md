---
title: Glossary
category: meta
date_created: 2026-04-22
date_updated: 2026-04-22
---

# Glossary

> ⚠️ **Demo Data** — Terms below describe the wiki system itself using fictional examples.

| Term             | Definition                                                                                                    |
|------------------|---------------------------------------------------------------------------------------------------------------|
| **AGENT.md**     | Project-root file that orients an AI agent — contains architecture overview, key paths, and conventions.       |
| **APIM**         | Azure API Management — managed API gateway for publishing, securing, and monitoring APIs. See [[azure-api-management]]. |
| **Bootstrap**    | Initial setup of a wiki: creating schema, index, glossary, templates, and first project pages.                |
| **End-Session**  | Workflow step at session close — capture lessons, update wiki pages, check git status. See [[schema]].        |
| **Entra ID**     | Microsoft's cloud identity platform (formerly Azure AD). Used for auth, tokens, managed identity. See [[azure-entra-id]]. |
| **Ingest**       | Pipeline for compiling raw content (docs, transcripts, code) into structured wiki pages with frontmatter.     |
| **Memory Wiki**  | A Karpathy-style LLM knowledge base — structured Markdown files that AI agents read for persistent context.   |
| **OBO**          | On-Behalf-Of flow — exchanging a user's token for a downstream API token, preserving user identity. See [[identity-propagation]]. |
| **Schema**       | The governance file ([[schema]]) defining categories, naming rules, quality standards, and article format.     |
| **Wikilink**     | Internal link syntax `[[page-name]]` connecting wiki pages. Resolved against the wiki directory tree.         |
| **Workflow**     | Global rules for AI agent behavior — plan before coding, verify before done. See `agent-config/workflow.md`.  |
