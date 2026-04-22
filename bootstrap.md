# AI Agent Memory — Bootstrap Prompt

> **Give this file to your AI coding agent** (GitHub Copilot, Claude Code, Codex, Cursor, Windsurf, etc.) in a new project folder.
>
> The agent will create a **persistent memory wiki** that compounds knowledge across coding sessions. No more re-explaining your stack, debugging the same issues twice, or losing hard-won lessons.
>
> Based on the [Karpathy LLM Wiki pattern](https://x.com/karpathy/status/1882839370598990104): raw sources → compiled wiki → structured schema.

---

## Instructions

You are setting up a **persistent memory system** for an AI coding agent. Follow each step below. Create every file with the exact content provided. Do not skip steps.

---

### Step 1: Create the directory structure

Create the following directory tree inside a `memory/` folder (at the root of the current project, or at a path the user specifies):

```
memory/
├── schema.md
├── index.md
├── log.md
├── glossary.md
├── agent-config/
│   ├── workflow.md
│   └── platform.md
├── workflows/
│   ├── ingest.md
│   ├── end-session.md
│   └── query.md
├── wiki/
│   ├── projects/
│   ├── domains/
│   ├── patterns/
│   └── lessons/
├── raw/
└── templates/
    ├── project.md
    └── lesson.md
```

Create all directories (including empty ones like `raw/`, `wiki/projects/`, etc.).

---

### Step 2: Create `memory/schema.md`

```markdown
---
title: Wiki Schema
category: meta
date_created: {{today}}
date_updated: {{today}}
---

# Wiki Schema

This document governs how the wiki is structured. The LLM reads this to understand conventions, categories, and workflows.

## Category Taxonomy

| Category | Folder | Description | Example Pages |
|----------|--------|-------------|---------------|
| Projects | `wiki/projects/` | Per-project knowledge: architecture, lessons, technical reference | `my-api`, `mobile-app` |
| Domains | `wiki/domains/` | Technical domain deep-dives | `authentication`, `kubernetes`, `react` |
| Patterns | `wiki/patterns/` | Reusable architecture & design patterns | `retry-with-backoff`, `event-sourcing` |
| Lessons | `wiki/lessons/` | Consolidated debugging history & gotchas | `encoding-gotchas`, `deployment-failures` |
| Agent Config | `agent-config/` | Cross-project AI agent configuration | `workflow`, `platform` |

## Article Format

Every wiki page has YAML frontmatter + markdown body:

~~~markdown
---
title: Page Title
category: projects|domains|patterns|lessons
tags: [tag1, tag2, tag3]
source_docs: []
date_created: YYYY-MM-DD
date_updated: YYYY-MM-DD
---

# Page Title

## Summary
One-paragraph overview.

## Content
Main content with [[wikilinks]] to related pages.

## Related
- [[related-page-1]]
- [[related-page-2]]

## Sources
- Source documents, URLs, or references
~~~

## Naming Conventions

- **File names**: lowercase, hyphenated (`my-project.md`, not `My Project.md`)
- **Folders**: lowercase, hyphenated
- **Category in frontmatter**, not in path (allows migration without renaming)
- **Derive filename from content**, not from LLM-generated titles (deterministic)

## Wikilink Syntax

- `[[page-name]]` — link to another wiki page
- `[[page-name|Display Text]]` — link with custom display text
- `[[page-name#Section]]` — link to a specific section
- Pages are resolved by filename (shortest unique match)

## Index Files

- **`index.md`** (root) — master content catalog, grouped by category, with counts
- The LLM updates indexes on every ingest

## Log Format

`log.md` is append-only. Each entry:

```
- **YYYY-MM-DDTHH:MM** | ACTION | "Title" | details
```

Actions: `INGEST`, `QUERY`, `UPDATE`, `CREATE`

## When to Create a New Page vs Update Existing

- **New page**: new entity, new project, new concept not covered anywhere
- **Update existing**: new information about an existing entity, correction, additional detail
- **Consolidate**: if 3+ pages cover overlapping topics, merge into one

## Quality Rules

- Every page must have frontmatter with at least: title, category, date_created
- Every page should have at least one `[[wikilink]]` to another page (no orphans)
- Source documents must be cited when information comes from external sources
- **No speculation**: pages must be source-backed
```

---

### Step 3: Create `memory/index.md`

```markdown
---
title: Wiki Index
category: meta
date_created: {{today}}
date_updated: {{today}}
---

# Wiki Index

*Central knowledge base — articles compiled from projects, domain knowledge, and cross-project synthesis.*

**Quick navigation:** [[glossary]] · [[schema]] · [[log]]

## Projects (0 articles)

## Domains (0 articles)

## Patterns (0 articles)

## Lessons (0 articles)
```

---

### Step 4: Create `memory/log.md`

```markdown
---
title: Wiki Activity Log
category: meta
tags: [log, activity]
date_created: {{today}}
date_updated: {{today}}
---

# Wiki Activity Log

Append-only record of all wiki operations.

- **{{now}}** | CREATE | "Wiki initialized" | Bootstrap setup complete
```

---

### Step 5: Create `memory/glossary.md`

```markdown
---
title: Glossary
category: meta
date_created: {{today}}
date_updated: {{today}}
---

# Glossary

Quick-reference definitions for terms used throughout this wiki, organized alphabetically.

## C

- **Compounding Memory** — Memory that improves over time via merge/dedupe/refactor rather than blind append. Core idea of the Karpathy wiki pattern. See [[schema]].

## I

- **Ingest** — The process of converting raw source material into structured wiki knowledge. See `workflows/ingest.md`.

## K

- **Karpathy Wiki Pattern** — Three-layer knowledge architecture: raw sources (immutable) → compiled wiki (structured) → schema (governance). Named after Andrej Karpathy's proposal for LLM-maintained knowledge bases.

## W

- **Wikilink** — Internal link syntax `[[page-name]]` used to connect wiki pages and build a knowledge graph.
```

---

### Step 6: Create `memory/agent-config/workflow.md`

```markdown
---
title: Workflow Rules
category: agent-config
tags: [workflow, rules, conventions]
date_created: {{today}}
date_updated: {{today}}
---

# Workflow Rules

These rules apply to all projects and all AI coding assistant sessions.

> Each project has an `AGENT.md` in its root with project-specific instructions.
> Lessons learned and technical reference live in the central memory wiki at `memory/`.

## Rules

### 1. Plan Before Coding
- **For any task with 3+ expected steps, outline the approach before writing code.**
- Define what "done" looks like — including acceptance criteria and verification steps.
- List the files you expect to change and why.
- Get approval before implementing.

### 2. Verify Before Done
- Never mark a task complete without proving it works.
- Run tests, check logs, demonstrate correctness.
- Diff behavior between before and after when relevant.

### 3. Learn From Mistakes
- After ANY correction from the user: update the project's wiki page at `memory/wiki/projects/{project-name}.md` — append to "## Lessons Learned".
- Write rules that prevent the same mistake from recurring.
- Review the project's wiki page at session start.

### 4. No Blind Retries
- **Never retry a command that failed with a non-transient error.** Diagnose the root cause instead.
- Non-transient: validation errors, 401, 403, permission denied.
- Transient (ok to retry once): network timeout, 429, 503, connection reset.
- After 2 failures on the same command: stop, explain the issue, ask the user.

### 5. Keep It Simple
- Don't add features, refactor code, or make improvements beyond what was asked.
- For non-trivial changes: pause and ask "is there a more elegant way?"
- If a fix feels hacky: step back and implement the clean solution.

## Session Routine

**Start of session:**
- Read the project's wiki page at `memory/wiki/projects/{project-name}.md` — especially "## Lessons Learned".
- Review any active work notes or prior session context.

**End of session:**
- Capture any new lessons in the project's wiki page ("## Lessons Learned").
- Note what was done and what's next.
- Follow the end-session workflow in `memory/workflows/end-session.md`.

**Wiki compounding (when significant work was done):**
- If a reusable pattern was discovered, create or update a page in `memory/wiki/patterns/`.
- If a domain gotcha was learned, update the relevant `memory/wiki/domains/*.md` page.
- Update `memory/log.md` with: `- **{timestamp}** | UPDATE | "{what changed}" | project: {name}`

## Project Structure Convention

Every project should have:

```
project-root/
├── AGENT.md                       # Main AI instructions (project overview + rules)
├── CLAUDE.md                      # Pointer to AGENT.md (Claude Code compatibility)
├── .github/
│   └── copilot-instructions.md    # Pointer to AGENT.md (GitHub Copilot compatibility)
└── README.md                      # Human-readable project overview
```

Lessons learned and technical reference are centralized in `memory/wiki/projects/{project-name}.md` — not duplicated in the repo.
```

---

### Step 7: Create `memory/agent-config/platform.md`

Ask the user what platform they're on (OS, language runtimes, cloud provider). If the user doesn't specify, create sensible defaults:

```markdown
---
title: Platform & Preferences
category: agent-config
tags: [platform, environment]
date_created: {{today}}
date_updated: {{today}}
---

# Platform & Preferences

## Environment

- OS: (ask user, or detect from current environment)
- Primary language(s): (ask user)
- Cloud provider: (ask user, or "none" if local-only)

## Platform Gotchas

<!-- Add platform-specific gotchas as you discover them -->
<!-- Example: "Always use encoding='utf-8' for subprocess on Windows" -->

## Cross-Project Knowledge

Shared domain knowledge files are stored in `agent-config/knowledge/` — consult when working in the relevant domain.
```

---

### Step 8: Create workflow files

#### Create `memory/workflows/ingest.md`

```markdown
---
title: Ingest Workflow
category: workflows
date_created: {{today}}
date_updated: {{today}}
---

# Ingest Source — LLM-Compiled Wiki Ingestion

When the user says **"ingest"** followed by content, follow these 7 phases:

## Phase 1: Gather Context

1. **Read `memory/schema.md`** — understand wiki structure, categories, naming rules
2. **Read `memory/index.md`** — get the full list of existing articles with paths (needed for backlink resolution)
3. **Read `memory/glossary.md`** — check existing terms
4. **Read the source content** — the file, topic, or conversation findings to ingest

## Phase 2: LLM Compilation

Compile the source into structured wiki knowledge. Ask yourself:

### 2a. What type of knowledge is this?
- **Project knowledge** → `wiki/projects/{slug}.md` (create or update)
- **Domain/technology knowledge** → `wiki/domains/{slug}.md` (create or update)
- **Reusable pattern** → `wiki/patterns/{slug}.md` (create or update)
- **Debugging lesson / gotcha** → `wiki/lessons/{slug}.md` (create or update)
- **Platform/env knowledge** → `agent-config/platform.md` (update)

### 2b. Create or update?
- Search `index.md` for existing pages about this topic
- If a page exists → **UPDATE** it (don't create duplicates)
- If no page exists → **CREATE** a new one

### 2c. Compile the article
For **new pages**, generate YAML frontmatter + Markdown body following `schema.md`:

~~~markdown
---
title: "Descriptive Title"
category: domains|projects|patterns|lessons
tags: [tag1, tag2, tag3]
source_docs: ["original-source.ext"]
date_created: YYYY-MM-DD
date_updated: YYYY-MM-DD
---

# Title

## Summary
One-paragraph overview.

## Content
Main content with [[wikilinks]] to related pages.
Use ONLY wikilinks that exist in index.md — check before linking.

## Related
- [[existing-page-1]]
- [[existing-page-2]]

## Sources
- Source reference
~~~

For **updates**, surgically edit the existing page — don't rewrite unrelated content.

### 2d. Resolve backlinks against index.md
**CRITICAL:** Every `[[wikilink]]` MUST point to a page that exists in `index.md`.
- Read index.md to find the correct slug
- If the target page doesn't exist, either create it or don't link
- Never create orphan `[[links]]` to non-existent pages

## Phase 3: Update the Wiki Graph

After compiling the article, update these files:

1. **Backlinks TO the new page** — find 2-5 existing pages that should reference this topic, add `[[wikilinks]]` to them
2. **Domain pages** — if this relates to an existing domain, update its relevant section
3. **Glossary** — add new terms to `glossary.md` with one-line definitions
4. **Root `index.md`** — add the entry under the correct category, update article count
5. **`log.md`** — append entry: `- **YYYY-MM-DDTHH:MM** | INGEST | "Title" | source: ... | category: ...`

## Phase 4: Save Raw Source

**Every ingest MUST produce an immutable raw snapshot** (Karpathy Layer 1 = immutable):

- **File source** → copy to `raw/`
- **Conversation / web search** → write the verbatim response to `raw/{slug}-YYYY-MM-DD.md`
- **User-provided text** → save as-is to `raw/{slug}-YYYY-MM-DD.md`

The `source_docs:` frontmatter field on every new wiki page MUST point to a real file under `raw/`.

## Phase 5: Self-Audit Gate

Before reporting, verify all of these pass:

```
[ ] 1. Raw source exists under raw/ AND is referenced in source_docs: frontmatter
[ ] 2. New page has ≥1 incoming [[wikilink]] from an existing page
[ ] 3. index.md article count matches actual file count in the category
[ ] 4. Glossary has any new terms (acronyms, product names) introduced by the source
[ ] 5. log.md has a new INGEST entry with ISO timestamp, title, source, category
```

If any item fails, fix it before proceeding.

## Phase 6: Consolidation (for bulk ingests of 3+ sources)

When ingesting multiple related sources:

1. **List every source** you intend to ingest
2. **Create a consolidation matrix** mapping each source to its target page
3. **Same entity across N sources → ONE page**, not N pages
4. **One consolidated log.md entry** for the batch, not N separate entries

## Phase 7: Report

Report a table:

| Action | File | Change |
|--------|------|--------|
| CREATE/UPDATE | wiki/domains/foo.md | New page: ... |
| UPDATE | index.md | Added foo to Domains |
| UPDATE | glossary.md | Added term: ... |
| APPEND | log.md | INGEST entry |

**Target: 8-15 files touched per ingest.**

## Anti-Patterns

- ❌ Don't create `[[wikilinks]]` to pages that don't exist in index.md
- ❌ Don't duplicate content already in another page — link to it instead
- ❌ Don't skip updating index.md and log.md
- ❌ Don't append raw text to knowledge files — compile it into structured sections
- ❌ Don't point `source_docs:` at a free-text string — always a real file under `raw/`
```

#### Create `memory/workflows/end-session.md`

```markdown
---
title: End Session Workflow
category: workflows
date_created: {{today}}
date_updated: {{today}}
---

# End Session

When the user says **"end session"**, **"wrap up"**, or **"done for today"**, follow these 5 steps:

## Step 1: Update Project Docs

- Check if the current project's wiki page at `memory/wiki/projects/{project-name}.md` needs updates from today's work.
- Append new lessons to "## Lessons Learned".
- Update technical reference if architecture or key paths changed.

## Step 2: Compound to Wiki

If significant lessons or patterns were discovered during this session:

- **Update the project page** at `memory/wiki/projects/{project-name}.md`
- **Update domain pages** at `memory/wiki/domains/*.md` if domain-specific knowledge was gained
- **Create or update pattern/lesson pages** in `memory/wiki/patterns/` or `memory/wiki/lessons/` if a reusable insight emerged
- **Add new glossary terms** to `memory/glossary.md`
- **Append to `memory/log.md`**: `- **{timestamp}** | UPDATE | "{what changed}" | project: {name}`

## Step 3: Ingest Session Learnings

If meaningful knowledge was generated during the session (gotchas, debugging breakthroughs, architecture decisions):

- Follow the ingest workflow (`memory/workflows/ingest.md`) with the session's key learnings as source content.
- If nothing meaningful was learned (e.g., session was a quick fix), skip and note it.

## Step 4: Git Check

- Run `git status` and warn about uncommitted changes.
- Remind the user to commit if there are pending changes.

## Step 5: Summary

Present a summary table:

| Area | Status | Action |
|------|--------|--------|
| Project docs | Up to date / Updated | ... |
| Wiki (project page) | Up to date / Updated | ... |
| Wiki (domains/patterns) | Up to date / Created | ... |
| Glossary | Up to date / Updated | ... |
| Git | Clean / Has changes | ... |
```

#### Create `memory/workflows/query.md`

```markdown
---
title: Query Workflow
category: workflows
date_created: {{today}}
date_updated: {{today}}
---

# Query Wiki

When the user asks a question about the knowledge base or says **"query"**, follow these 4 steps:

## Step 1: Search the Index

- Read `memory/index.md` — scan the content catalog for relevant pages
- Identify which wiki pages are likely to contain the answer

## Step 2: Read Relevant Pages

- Read the identified pages **in full** — don't skip or summarize prematurely
- Cross-reference between pages to build a complete picture

## Step 3: Synthesize Answer

- Compose a clear answer with `[[wikilink]]` citations to source pages
- If multiple pages contribute, synthesize rather than listing — add your reasoning

## Step 4: Log the Query

- Append to `memory/log.md`: `- **{timestamp}** | QUERY | "{question}"`

Present the answer to the user with citations.
```

---

### Step 9: Create template files

#### Create `memory/templates/project.md`

```markdown
---
title: "{{title}}"
category: projects
tags: []
source_docs: []
date_created: {{date}}
date_updated: {{date}}
---

# {{title}}

## Overview
<!-- What this project does, its purpose -->

## Architecture
<!-- Key components, tech stack, data flow -->

## Key Paths
<!-- Important files and directories -->

## Lessons Learned
<!-- Debugging history, gotchas, things that work -->

## Technical Reference
<!-- Implementation details, API endpoints, configuration -->

## Related
<!-- Links to related projects, domains, patterns -->
```

#### Create `memory/templates/lesson.md`

```markdown
---
title: "{{title}}"
category: lessons
tags: []
source_docs: []
projects: []
date_created: {{date}}
date_updated: {{date}}
---

# {{title}}

## Context
<!-- When and where this lesson was learned -->

## Problem
<!-- What went wrong or what was confusing -->

## Root Cause
<!-- Why it happened -->

## Fix
<!-- How it was resolved -->

## Rule
<!-- The rule to prevent this from recurring -->

## Related
<!-- Links to related lessons, projects, domains -->
```

---

### Step 10: Create project instruction files

Create these files **in the current project root** (not inside `memory/`):

#### Create `AGENT.md`

```markdown
# Project Instructions

## Memory System

This project uses a persistent AI memory wiki. All cross-project knowledge lives at `memory/`.

### Key Files
- `memory/agent-config/workflow.md` — Workflow rules (read at session start)
- `memory/agent-config/platform.md` — Platform preferences
- `memory/schema.md` — Wiki governance and conventions
- `memory/index.md` — Content catalog (read first for queries)
- `memory/glossary.md` — Canonical terms

### Workflows
- **Ingest**: Say "ingest" + content → follows `memory/workflows/ingest.md`
- **End session**: Say "end session" → follows `memory/workflows/end-session.md`
- **Query**: Ask a question → follows `memory/workflows/query.md`

### Rules
Read `memory/agent-config/workflow.md` for the full set of rules. Key rules:

1. **Plan Before Coding** — For tasks with 3+ steps, outline first
2. **Verify Before Done** — Prove it works before marking complete
3. **Learn From Mistakes** — Update wiki after corrections
4. **No Blind Retries** — Diagnose root cause on failure
5. **Keep It Simple** — Don't add beyond what was asked
```

#### Create `CLAUDE.md`

```markdown
# Claude Code Instructions

Read `AGENT.md` for all project instructions, workflow rules, and references.
```

#### Create `.github/copilot-instructions.md`

```markdown
# Copilot Instructions

Read `AGENT.md` for all project instructions, workflow rules, and references.
```

---

## Verification Checklist

After creating all files, verify each item:

- [ ] `memory/schema.md` exists and has the category taxonomy table
- [ ] `memory/index.md` exists with category sections (may have 0 articles)
- [ ] `memory/log.md` exists with the format header and initialization entry
- [ ] `memory/glossary.md` exists with starter terms
- [ ] `memory/agent-config/workflow.md` has 5 rules defined
- [ ] `memory/agent-config/platform.md` exists (may have defaults)
- [ ] `memory/workflows/ingest.md` has the 7-phase pipeline
- [ ] `memory/workflows/end-session.md` has the 5-step routine
- [ ] `memory/workflows/query.md` has the 4-step procedure
- [ ] `memory/templates/project.md` exists with frontmatter template
- [ ] `memory/templates/lesson.md` exists with frontmatter template
- [ ] `memory/wiki/projects/` directory exists
- [ ] `memory/wiki/domains/` directory exists
- [ ] `memory/wiki/patterns/` directory exists
- [ ] `memory/wiki/lessons/` directory exists
- [ ] `memory/raw/` directory exists
- [ ] `AGENT.md` exists and references `memory/agent-config/workflow.md`
- [ ] `CLAUDE.md` exists and points to `AGENT.md`
- [ ] `.github/copilot-instructions.md` exists and points to `AGENT.md`

Report the checklist results to the user.

---

## Next Steps

Setup is complete. Here's how to use your memory system:

1. **Try your first ingest:** Tell your agent `ingest` followed by any topic you've learned today — a debugging breakthrough, a new tool, an architecture decision. The agent will compile it into a wiki page.

2. **At the end of your session:** Tell your agent `end session` to capture lessons learned, update project docs, and compound knowledge.

3. **Query your knowledge:** Ask your agent any question — it will search the wiki and synthesize an answer with citations.

4. **It compounds over time.** Each session adds to the wiki. After a few weeks, your agent will have a rich knowledge base of your projects, patterns, and hard-won lessons — and it never forgets.
