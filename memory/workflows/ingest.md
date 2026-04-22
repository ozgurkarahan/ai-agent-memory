# Ingest Workflow

> **Agent-agnostic.** Any AI coding agent (Copilot, Claude Code, Cursor, Aider, etc.) can follow these steps. Nothing here is specific to a single tool.

When a user says **"ingest"** followed by content (a document, conversation, article, or lesson), follow this pipeline to compile it into the wiki.

**Target: 8–15 files touched per ingest.** If you only touched 2–3 files, you missed graph updates.

---

## Phase 1 — Gather Context

Read these files **in parallel** to build a mental model of the wiki's current state:

| File | Purpose |
|------|---------|
| `memory/schema.md` | Category taxonomy, frontmatter rules, naming conventions |
| `memory/index.md` | Full catalog of existing pages — check for duplicates |
| `memory/glossary.md` | Canonical terms — check for existing definitions |
| *Source content* | The material the user wants ingested |

**Goal:** Understand what already exists so you don't create duplicates or orphans.

---

## Phase 2 — Classify

Determine the knowledge type and target location:

| Category | When to use | Target directory |
|----------|-------------|------------------|
| `projects` | Knowledge about a specific codebase or engagement | `wiki/projects/` |
| `domains` | Technology or platform knowledge (e.g., FastAPI, Redis) | `wiki/domains/` |
| `patterns` | Reusable solutions or design patterns | `wiki/patterns/` |
| `lessons` | Debugging stories with root cause and rules | `wiki/lessons/` |

**Decision:** Does a page already exist for this topic?
- **Yes** → You will **update** it in Phase 3
- **No** → You will **create** it in Phase 3

---

## Phase 3 — Compile

Create or update the wiki page with proper structure:

### Frontmatter (required)

```yaml
---
title: "Page Title"
category: projects | domains | patterns | lessons
tags: [tag-a, tag-b]
source_docs: ["path/to/source"]
date_created: YYYY-MM-DD
date_updated: YYYY-MM-DD
---
```

### Body

- Use `[[wikilinks]]` to connect to related pages
- **Every `[[wikilink]]` must resolve** to a page listed in `index.md`
- If a link target doesn't exist, either create the page or remove the link
- Follow the category-specific template from `memory/templates/`

### Quality Checks

- [ ] Frontmatter has all required fields
- [ ] `date_updated` is set to today
- [ ] All `[[wikilinks]]` resolve to existing pages
- [ ] Content is focused — one concept per page

---

## Phase 4 — Update the Wiki Graph

This is where most people under-invest. A wiki page without connections is an orphan.

**Required updates:**

| File | Update |
|------|--------|
| `memory/index.md` | Add new page to the appropriate category table |
| `memory/glossary.md` | Add any new terms introduced by this content |
| `memory/log.md` | Append ingest entry (see format below) |
| Related wiki pages | Add `[[backlinks]]` from existing pages to the new one |
| Category `_index.md` | Update if the category has an index file |

**Backlink rule:** If Page A links to Page B, check whether Page B should also link back to Page A. Cross-references strengthen the graph.

**Log entry format:**
```
- **{date}** | INGEST | "{page title}" | category: {category} | source: {source description}
```

---

## Phase 5 — Copy Raw Source

If the ingested content came from a file (PDF, transcript, document):

1. Copy the original file to `memory/raw/`
2. Use a descriptive filename: `raw/{date}-{short-description}.{ext}`
3. Reference it in the wiki page's `source_docs` frontmatter field

This preserves the original material for future re-processing.

---

## Phase 6 — Self-Audit

Before reporting completion, verify:

| Check | How |
|-------|-----|
| All `[[wikilinks]]` resolve | Scan the new page for `[[...]]` and confirm each target exists in `index.md` |
| Frontmatter complete | `title`, `category`, `date_created`, `date_updated` all present |
| 8–15 files touched | Count the files you modified — if fewer than 8, you likely missed graph updates |
| No orphans created | The new page is linked from at least one other page or from `index.md` |
| Glossary updated | Any new terms are defined in `glossary.md` |

---

## Phase 7 — Report

Present a summary table to the user:

```
| Action  | File                              | Change                        |
|---------|-----------------------------------|-------------------------------|
| CREATE  | wiki/patterns/circuit-breaker.md  | New pattern page              |
| UPDATE  | index.md                          | Added to Patterns table       |
| UPDATE  | glossary.md                       | Added "circuit breaker" term  |
| UPDATE  | wiki/domains/fastapi.md           | Added backlink                |
| UPDATE  | log.md                            | Appended ingest entry         |
| ...     | ...                               | ...                           |
```

**Total files touched: N** (target: 8–15)
