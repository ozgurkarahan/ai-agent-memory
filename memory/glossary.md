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
| **Bootstrap**    | Initial setup of a wiki: creating schema, index, glossary, templates, and first project pages.                |
| **End-Session**  | Workflow step at session close — capture lessons, update wiki pages, check git status. See [[schema]].        |
| **Ingest**       | Pipeline for compiling raw content (docs, transcripts, code) into structured wiki pages with frontmatter.     |
| **Memory Wiki**  | A Karpathy-style LLM knowledge base — structured Markdown files that AI agents read for persistent context.   |
| **Schema**       | The governance file ([[schema]]) defining categories, naming rules, quality standards, and article format.     |
| **Wikilink**     | Internal link syntax `[[page-name]]` connecting wiki pages. Resolved against the wiki directory tree.         |
| **Workflow**     | Global rules for AI agent behavior — plan before coding, verify before done. See `agent-config/workflow.md`.  |
