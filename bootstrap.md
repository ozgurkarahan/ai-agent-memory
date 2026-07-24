# AI Agent Memory — Bootstrap Prompt

> **Give this file to your AI coding agent** (GitHub Copilot, Claude Code, Codex, Cursor, Windsurf, etc.) in a new project folder.
>
> The agent will create a **persistent memory wiki** that compounds knowledge across coding sessions, plus a complete set of triggerable workflows (ingest, query, end-session, lint, plan-week, close-week, project-status, review-sessions, new-engagement) wired for **both GitHub Copilot CLI and Claude Code**.
>
> Based on the [Karpathy LLM Wiki pattern](https://x.com/karpathy/status/1882839370598990104): raw sources → compiled wiki → structured schema.

---

## Instructions

You are setting up a **persistent memory system** for an AI coding agent. Follow each step below. Create every file with the exact content provided. Do not skip steps.

This bootstrap installs **9 skills across 2 native agent surfaces**, plus an agent-neutral Markdown copy:

| Copy | Path | Read by |
|---|---|---|
| Native GitHub Copilot CLI instructions | `.github/instructions/{slug}.instructions.md` | GitHub Copilot CLI (auto-loaded via `applyTo: "**"`) |
| Native Claude Code skills | `.claude/skills/{slug}/SKILL.md` | Claude Code (auto-routed by `description:` field) |
| Agent-neutral workflows | `memory/workflows/{slug}.md` | Any agent that follows `AGENT.md`; portable reference copy |

The **body** of each skill is identical across the 3 copies. Only the YAML frontmatter differs.

## Non-negotiable execution contract

This is an **installation task**, not a document to summarize. Work directly in the current folder unless the user supplied another target.

1. Install the executable skill surfaces first. A wiki without `.github/instructions/` and `.claude/skills/` is an incomplete installation.
2. Complete each mandatory gate before continuing. Do not skip a failed gate.
3. Be resume-safe: inspect existing files first, keep files that already match, and create or repair every missing or incomplete file.
4. Do not report success until the Definition of Done in Step 12 passes.
5. If interrupted, the next run starts at the first failed gate rather than recreating the wiki from scratch.

`memory/wiki/skills/` contains knowledge *about* skills. It does **not** make skills executable. The native executable locations are `.github/instructions/` and `.claude/skills/`.

---

### Step 1: Create the directory structure

Create the following directory tree at the root of the current project (or at a path the user specifies):

```
project-root/
├── AGENT.md                                    # Main AI instructions (created in Step 10)
├── CLAUDE.md                                   # Pointer to AGENT.md (Step 10)
├── .github/
│   ├── copilot-instructions.md                 # Pointer to AGENT.md (Step 10)
│   └── instructions/                           # GitHub Copilot CLI surface (Step 2)
│       ├── ingest.instructions.md
│       ├── end-session.instructions.md
│       ├── query.instructions.md
│       ├── lint.instructions.md
│       ├── plan-week.instructions.md
│       ├── close-week.instructions.md
│       ├── project-status.instructions.md
│       ├── review-sessions.instructions.md
│       └── new-engagement.instructions.md
├── .claude/
│   └── skills/                                 # Claude Code surface (Step 2)
│       ├── ingest/SKILL.md
│       ├── end-session/SKILL.md
│       ├── query/SKILL.md
│       ├── lint/SKILL.md
│       ├── plan-week/SKILL.md
│       ├── close-week/SKILL.md
│       ├── project-status/SKILL.md
│       ├── review-sessions/SKILL.md
│       └── new-engagement/SKILL.md
├── memory/
│   ├── schema.md                               # Wiki governance (Step 3)
│   ├── index.md                                # Content catalog (Step 4)
│   ├── log.md                                  # Append-only audit log (Step 5)
│   ├── glossary.md                             # Canonical terms (Step 6)
│   ├── agent-config/
│   │   ├── workflow.md                         # Cross-project rules (Step 7)
│   │   └── platform.md                         # Platform & preferences (Step 8)
│   ├── workflows/                              # Agent-neutral skill bodies (Step 2)
│   │   ├── ingest.md
│   │   ├── end-session.md
│   │   ├── query.md
│   │   ├── lint.md
│   │   ├── plan-week.md
│   │   ├── close-week.md
│   │   ├── project-status.md
│   │   ├── review-sessions.md
│   │   └── new-engagement.md
│   ├── templates/                              # Page templates (Step 9)
│   │   ├── project.md
│   │   └── lesson.md
│   ├── wiki/                                   # The compiled knowledge graph
│   │   ├── projects/
│   │   ├── domains/
│   │   ├── patterns/
│   │   ├── lessons/
│   │   ├── skills/
│   │   ├── agents/
│   │   ├── tools/
│   │   └── _queries/
│   ├── raw/                                    # Immutable source snapshots (Karpathy Layer 1)
│   └── ops/                                    # Operational state for plan-week/close-week
│       ├── weekly/                             # ISO week files (e.g., 2026-W18.md)
│       └── activity.jsonl                      # Append-only event log
└── project-template/                           # Required offline scaffold for new engagements (Step 11)
```

Create all directories (including empty ones like `raw/`, `wiki/projects/`, `memory/ops/weekly/`).

Also create an empty `memory/ops/activity.jsonl` (touch the file so `plan-week`/`close-week` can append to it).

---

### Step 2: Install all 9 skills before creating wiki content

**This is the first mandatory deliverable. Do not continue to Step 3 until its gate passes.**

For each skill below, create **3 files** containing the **same body** but **different frontmatter**:

1. `.github/instructions/{slug}.instructions.md` — frontmatter: `---\napplyTo: "**"\n---`
2. `.claude/skills/{slug}/SKILL.md` — frontmatter: `---\nname: {slug}\ndescription: <see per-skill description below>\n---`
3. `memory/workflows/{slug}.md` — frontmatter: `---\napplyTo: "**"\n---`

Create each set of 3 files immediately before moving to the next skill. The body is byte-identical across all 3 files; only the frontmatter differs.

If a destination file already exists, verify its frontmatter and body. Keep it if correct; otherwise repair it. This makes interrupted installs safe to resume.

---

#### Skill: `ingest`

**Claude Code description** (for `.claude/skills/ingest/SKILL.md` frontmatter):

```yaml
name: ingest
description: "Ingest a source document into the wiki following the Karpathy LLM Wiki pattern. Compile content into structured frontmatter + Markdown pages, resolve [[wikilinks]] against the existing graph, update related pages, run lint, emit activity event. Trigger: 'ingest [source]', 'mass ingest [batch]'."
```

**Body** (save to all 3 paths — `.github/instructions/ingest.instructions.md`, `.claude/skills/ingest/SKILL.md`, `memory/workflows/ingest.md`):

~~~markdown
# Ingest Source — LLM-Compiled Wiki Ingestion (Karpathy Pattern)

Two triggers:

- **"ingest"** — single-source ingest. Follow Phase 1 → Phase 7 as written.
- **"mass ingest"** / **"bulk ingest"** / **"ingest all ... from ..."** — multi-source batch. MUST insert **Phase 0 (Inventory)** and **Phase 2b.5 (Consolidation Planning)** before compiling anything. See [[ingest]] consolidation section for the full pattern and rationale.

## Resolve the memory root

1. If `memory/schema.md` exists in the current workspace, set `WIKI_ROOT` to `memory/`.
2. Else if `schema.md` exists, set `WIKI_ROOT` to the current directory.
3. Else follow the memory-wiki path declared in the current project's `AGENT.md`.
4. If no folder containing both `schema.md` and `index.md` resolves, report the missing path and stop.

All relative paths below are under `WIKI_ROOT`.

## Phase 0: Inventory (mass ingest only)

Before pulling content from files or any connected source tool:

1. **List every source** you intend to ingest (OneNote sections, files, URLs, query topics).
2. **Save the inventory** to the session folder or as a temp list. Do NOT start pulling yet.
3. **If the source system can't be enumerated**, explicitly state the limitation and the coverage estimate before proceeding.
4. **Ask the user to confirm scope** if the inventory is >10 sources — consolidation decisions are cheaper to agree on upfront than to refactor later.

## Phase 1: Gather Context

1. **Read `schema.md`** — understand wiki structure, categories, naming rules
2. **Read `index.md`** — get the full list of existing articles with paths (needed for backlink resolution)
3. **Read `glossary.md`** — check existing terms
4. **Read the source content** — the file, topic, or conversation findings to ingest

## Phase 2: LLM Compilation (this is YOU — use your reasoning)

Compile the source into structured wiki knowledge. Ask yourself:

### 2a. What type of knowledge is this?
- **Project knowledge** → `wiki/projects/{slug}.md` (create or update)
- **Domain/technology knowledge** → `wiki/domains/{slug}.md` (create or update)
- **Reusable pattern** → `wiki/patterns/{slug}.md` (create or update)
- **Debugging lesson / gotcha** → `wiki/lessons/{slug}.md` (create or update)
- **Skill / command / triggerable workflow** → `wiki/skills/{slug}.md` (create or update)
- **Agent / subagent / role-based executor** → `wiki/agents/{slug}.md` (create or update)
- **Tool knowledge** → `wiki/tools/{slug}.md` (create or update; only for products, CLIs, SDKs, APIs, services, utilities)
- **Platform/env knowledge** → `agent-config/platform.md` or `agent-config/knowledge/{domain}.md` (update)
- If a source does not fit the installed taxonomy, ask before extending `schema.md`; do not invent a private or organization-specific category.

### 2b. Create or update?
- Search `index.md` for existing pages about this topic
- If a page exists → **UPDATE** it (don't create duplicates)
- If no page exists → **CREATE** a new one

### 2c. Compile the article
For **new pages**, generate YAML frontmatter + Markdown body following `schema.md`:

```markdown
---
title: "Descriptive Title"
category: projects|domains|patterns|skills|agents|lessons|tools|queries
tags: [tag1, tag2, tag3]
source_docs: ["raw/data/source-slug-YYYY-MM-DD.md"]
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
```

For **updates**, surgically edit the existing page — don't rewrite unrelated content.

### 2b.5 Consolidation Planning (REQUIRED when ≥3 related sources, i.e. mass ingest)

Before writing ANY wiki page, produce a consolidation matrix mapping every inventoried source to its target page. Write this to the session folder (e.g., `plan.md`) or present it inline to the user for approval.

| Source (raw snapshot) | Topic / entity | Target page | Action | Rationale |
|---|---|---|---|---|
| architecture-notes.md | Product Alpha architecture | wiki/projects/product-alpha.md | UPDATE | project page exists |
| retry-postmortem.md | API retry failures | wiki/lessons/api-retry-failures.md | CREATE | reusable debugging lesson |
| queue-benchmarks.md | Async queue design | wiki/patterns/async-queue-design.md | CREATE | cross-project pattern |

**Consolidation rules:**

- **Same entity across N sources → ONE page section.** Never create `acme-foo.md` + `acme-bar.md` when `acme.md` exists.
- **Cross-cutting theme in 3+ sources → promote to its own page** (domain / pattern / lesson). Below 3 sources → inline section on an existing hub.
- **Ephemeral / one-off mention → append to nearest hub**, don't create a page.
- **Sibling cohort (N similar entities) → ONE hub page** with a section per sibling. If the same subsections would be repeated for each item, consolidate them.
- **Target "8-15 files touched"** applies to the whole mass ingest, not per source. A 20-source mass ingest touching 15 files is correctly consolidated; touching 40 is over-fragmented.

After the matrix is approved (or self-reviewed for small batches), execute Phase 2c on each target in the matrix. Multiple sources writing to the same target → merge their content in one edit pass.

### 2d. Resolve backlinks against index.md
**CRITICAL:** Every `[[wikilink]]` MUST point to a page that exists in `index.md`.
- Read index.md to find the correct slug
- If the target page doesn't exist, either create it or don't link
- Never create orphan `[[links]]` to non-existent pages

## Phase 3: Update the Wiki Graph

After compiling the article, update these files:

1. **Backlinks TO the new page** — find 2-5 existing pages that should reference this topic, add `[[wikilinks]]` to them
2. **Domain pages** — if this relates to an existing domain, update its "Projects Using This" or relevant section in `wiki/domains/*.md`
3. **Glossary** — add new terms to `glossary.md` with one-line definitions
4. **Category `_index.md`** — add the new entry to `wiki/{category}/_index.md` if it exists
5. **Root `index.md`** — add the entry under the correct category, update article count
6. **`log.md`** — append entry: `- **YYYY-MM-DDTHH:MM** | INGEST | "Title" | source: ... | category: ...`
   - **Mass ingest:** ONE consolidated log entry with `source:` listing all raw/ snapshots and `files:` listing all created + modified pages — NOT N separate entries.

## Phase 4: Copy Raw Source (ALWAYS — Karpathy Layer 1 = immutable)

**Every ingest MUST produce an immutable raw snapshot**, regardless of source type:

- **File source** → copy it byte-for-byte to `raw/{articles|books|pdfs|data}/` with the agent's filesystem copy tool (or the platform's native copy command). Do not require a helper script.
- **Conversation / connected source tool / web search** → write the verbatim response to `raw/data/{source}-{slug}-YYYY-MM-DD.md`
- **User-provided text** → save as-is to `raw/data/{slug}-YYYY-MM-DD.md`

The `source_docs:` frontmatter field on every new wiki page MUST point to a real file under `raw/`, not a free-text description. Without this, the ingest is not auditable and violates the Karpathy 3-layer architecture (RAW / WIKI / SCHEMA).

## Phase 5: Lint (ALWAYS — required gate)

**Invoke the installed `lint` skill after every ingest.** It inspects the wiki directly with agent-native file/search tools; no helper script is required. This gate is non-negotiable because it catches orphan pages, broken wikilinks, and missing backlinks.

Report lint delta attributable to the ingest:
- **New orphan pages introduced?** → add at least one incoming `[[wikilink]]` from a related page
- **New broken links introduced?** → either create the target page or remove the link
- **New thin pages (<50 words)?** → expand the page with real content

Pre-existing issues unrelated to the current ingest can be left for a dedicated lint pass — but **issues the ingest itself created must be fixed in the same turn**.

## Phase 6: Self-Audit Gate (REQUIRED — run this BEFORE reporting)

Before writing the final report in Phase 7, run this 7-item self-audit. If ANY item fails, fix it in the same turn.

```
[ ] 1. Raw source exists under raw/ AND is referenced in source_docs: frontmatter?
      → search the `raw/` tree for the new page's `source_docs` value
[ ] 2. New page has ≥1 incoming [[wikilink]] from an existing page?
      → search `wiki/` for `[[<new-slug>]]` → must return ≥1 hit outside the new page itself
[ ] 3. index.md count matches actual file count in the category?
      → compare the count in `index.md` with an agent-native recursive inventory of category pages (exclude `_index.md`)
[ ] 4. Category _index.md lists the new page?
[ ] 5. Glossary has any new terms (acronyms, product names) introduced by the source?
[ ] 6. log.md has a new INGEST entry with ISO timestamp, title, source, category, pages?
[ ] 7. Lint was run AND any new issues introduced by this ingest are fixed?
      → delta comparison: issues-before vs issues-after attributable to this ingest = 0
[ ] 8. (mass ingest only) Consolidation matrix exists AND every row was executed?
      → no orphan raw/ snapshot without a target page entry
      → no duplicate topic pages created when a hub could have absorbed the content
```

**If you claim an ingest is complete without running this audit, you have failed the Karpathy pattern.** The pattern's value is compounding memory — that only works if every ingest leaves the graph in a consistent state, enforced mechanically, not by hope.

## Phase 7: Emit Activity Event (REQUIRED)

After lint and self-audit, but before the final report, append **one** line to `ops/activity.jsonl`. This makes the weekly activity table aggregatable on Friday.

Rules:

1. **Identify the `primary_topic`** — the single canonical wiki page this ingest is about. It must be a slug listed in `index.md`.
   - For a new domain page → its own slug (e.g., `event-streaming`).
   - For an updated project page → the project slug (e.g., `product-alpha`).
   - For a debugging lesson → the lesson slug (e.g., `api-retry-failures`).
   - **Do NOT** emit an event per modified file (`index.md`, `glossary.md`, `_index.md`, backlinks…). Those are pipeline exhaust, not work signal.

2. **Identify `secondary_topics`** (0-2 max) — only if the ingest meaningfully co-touches another canonical page. Most ingests have none.

3. **Resolve the active week** — ISO week of `current_datetime` in `Europe/Paris`. Format `2026-W{NN}`.

4. **Verify the active week file exists** — `ops/weekly/{week}.md`. If missing, create this minimal skeleton (replace placeholders):

   ```markdown
   ---
   title: Week {week}
   category: ops
   week: {week}
   status: open
   touches: []
   date_created: YYYY-MM-DD
   date_updated: YYYY-MM-DD
   ---

   # Week {week}

   <!-- BEGIN GENERATED ACTIVITY -->
   <!-- END GENERATED ACTIVITY -->
   ```

5. **Add the slug to the week file's `touches:` frontmatter** (deduped). This is the only edit `ingest` makes to the weekly markdown file — it never edits the activity table directly.

6. **Build one deduplicated changed-file list** containing every file created, updated, or appended during all phases, including the raw snapshot, wiki pages, backlinks, indexes, glossary, `log.md`, the weekly file, and `ops/activity.jsonl`. Do not include files that were only read.

7. **Append to `ops/activity.jsonl`** — one JSON object per line:

```json
{"ts":"2026-07-24T11:48:00+02:00","week":"2026-W30","source":"ingest","topic":"api-retry-failures","secondary":["event-streaming"],"resolved":true,"note":"Retry postmortem","files":9}
```

Required fields: `ts` (ISO 8601 with TZ offset), `week`, `source: "ingest"`, `topic`, `resolved` (based on the slug existing in `index.md`), `note` (≤80 chars), and `files` (the exact number of distinct paths in the changed-file list from Step 6). Optional: `secondary` (0-2 slugs).

## Phase 8: Report

Report the same deduplicated changed-file list used for the event count:

| Action | File | Change |
|--------|------|--------|
| CREATE/UPDATE | wiki/domains/foo.md | New page: ... |
| UPDATE | wiki/projects/bar.md | Added backlink to [[foo]] |
| UPDATE | index.md | Added foo to Domains |
| UPDATE | glossary.md | Added term: ... |
| APPEND | log.md | INGEST entry |

The number of table rows, distinct changed paths, and the event's `files` value must agree. Touch only files needed for source traceability and graph consistency; do not chase an arbitrary file-count target.

Include the self-audit result and lint summary:

| Gate | Result |
|------|--------|
| Self-audit (7 core items) | 7/7 pass |
| Lint (post-ingest) | 0 new issues introduced (N pre-existing unchanged) |

## Anti-Patterns (don't do these)

- ❌ Don't create `[[wikilinks]]` to pages that don't exist in index.md
- ❌ Don't duplicate content already in another page — link to it instead
- ❌ Don't use LLM-generated concept names as slugs — derive from content deterministically
- ❌ Don't skip updating index.md and log.md
- ❌ Don't append raw text to knowledge files — compile it into structured sections
- ❌ Don't point `source_docs:` at a free-text source description — always use a real file under `raw/`
- ❌ Don't skip the lint step — it's a required gate, not optional
- ❌ Don't skip the **self-audit gate** (Phase 6) and jump to reporting — the audit IS the proof the Karpathy pattern was followed
- ❌ Don't mark an ingest "done" until `source_docs:` in the new page points to a real file under `raw/` AND the new page has at least one incoming `[[wikilink]]` from an existing page
- ❌ (mass ingest) Don't start pulling sources before the Phase 0 inventory is written down — leads to forgotten sources and inconsistent coverage
- ❌ (mass ingest) Don't create one wiki page per source — consolidate same-entity / sibling-cohort sources via the Phase 2b.5 matrix
- ❌ (mass ingest) Don't write N log.md entries for one logical batch — one consolidated entry instead
- ❌ (Phase 7) Don't emit an activity event per modified file — only ONE per ingest with `primary_topic`. Pipeline exhaust ≠ work signal.
- ❌ (Phase 7) Don't write to `ops/weekly/{week}.md`'s activity table directly — only `close-week` regenerates it between the sentinels.
~~~

---

#### Skill: `end-session`

**Claude Code description** (for `.claude/skills/end-session/SKILL.md` frontmatter):

```yaml
name: end-session
description: "Wrap up the current coding session: update the project wiki page with lessons and decisions, graduate cross-cutting findings to domain / pattern / lesson pages, check git status, present a status table. Trigger: 'end session', 'wrap up', 'done for today'."
```

**Body** (save to all 3 paths — `.github/instructions/end-session.instructions.md`, `.claude/skills/end-session/SKILL.md`, `memory/workflows/end-session.md`):

```markdown
# End Session

When the user says "end session", "wrap up", or "done for today":

## Resolve the memory root

1. If `memory/schema.md` exists in the current workspace, use `memory/`.
2. Else if `schema.md` exists, use the current directory.
3. Else follow the memory-wiki path declared in the current project's `AGENT.md`.
4. If no folder containing both `schema.md` and `index.md` resolves, report that the wiki update is blocked; still perform the Git check.

All wiki paths below are relative to that memory root.

1. **Project wiki page** — Check if `wiki/projects/{project}.md` needs updates from today's work (lessons, decisions, technical details, status). Propose changes. *(Note: legacy `.ai/lessons-learned.md` / `.ai/project-reference.md` were retired — project knowledge lives directly on the wiki page.)*
2. **Wiki compounding** — If significant lessons or patterns were discovered:
   - Update relevant domain pages under `wiki/domains/`
   - Add new glossary terms to `glossary.md`
   - Create or update pattern/lesson pages if applicable
   - Append to `log.md`
3. **Git check** — Run `git status` and warn about uncommitted changes.
4. **Summary** — Present a table:

| Area | Status | Action |
|------|--------|--------|
| Project docs | Up to date / Updated | ... |
| Wiki (project page) | Up to date / Updated | ... |
| Wiki (domains/patterns) | Up to date / Graduated | ... |
| Glossary | Up to date / Updated | ... |
| Git | Clean / Has changes | ... |
```

---

#### Skill: `query`

**Claude Code description** (for `.claude/skills/query/SKILL.md` frontmatter):

```yaml
name: query
description: "Answer a question by searching the wiki: read index.md, find relevant pages, synthesize an answer with [[wikilink]] citations, file the answer in wiki/_queries/, update log.md. Trigger: 'query [question]' or a direct knowledge-base question."
```

**Body** (save to all 3 paths — `.github/instructions/query.instructions.md`, `.claude/skills/query/SKILL.md`, `memory/workflows/query.md`):

```markdown
# Query Wiki

When the user asks a question about the knowledge base or says "query":

## Resolve the memory root

1. If `memory/schema.md` exists in the current workspace, use `memory/`.
2. Else if `schema.md` exists, use the current directory.
3. Else follow the memory-wiki path declared in `AGENT.md`.
4. If no folder containing both `schema.md` and `index.md` resolves, report the missing path and stop.

All paths below are relative to that memory root.

1. **Read `index.md`** first — scan the content catalog for relevant pages
2. **Read relevant pages in full** — don't skip or summarize prematurely
3. **Synthesize an answer** with `[[wikilink]]` citations to source pages
4. **If the answer is valuable**, file it as a new page in `wiki/_queries/`:
   - YAML frontmatter: title, category: queries, tags, question, date_created
   - The synthesized answer as the body
   - `## Sources` listing the pages referenced
5. **Update `log.md`**: `- **{timestamp}** | QUERY | "{question}" | filed_as: {path}`
6. **Update `wiki/_queries/_index.md`** if a new page was filed

Present the answer with citations.
```

---

#### Skill: `lint`

**Claude Code description** (for `.claude/skills/lint/SKILL.md` frontmatter):

```yaml
name: lint
description: "Run wiki health checks (structural + semantic) and report findings by severity: critical (orphans, missing frontmatter), important (cross-reference gaps, thin pages), informational. Trigger: 'lint', 'health check', 'check wiki'."
```

**Body** (save to all 3 paths — `.github/instructions/lint.instructions.md`, `.claude/skills/lint/SKILL.md`, `memory/workflows/lint.md`):

~~~markdown
# Lint Wiki — Agent-Native Health Check

When the user says "lint", "health check", or "check wiki", inspect the wiki directly with the agent's file listing, search, and read tools. This skill has no helper-script dependency.

## Resolve the memory root

Before reading or writing:

1. If `memory/schema.md` exists in the current workspace, set `WIKI_ROOT` to `memory/`.
2. Else if `schema.md` exists in the current workspace, set `WIKI_ROOT` to the current directory.
3. Else follow the memory-wiki path declared in the current project's `AGENT.md`.
4. If none resolves to a folder containing both `schema.md` and `index.md`, report the missing path and stop. Do not guess.

All paths below are relative to `WIKI_ROOT`.

## Procedure

1. Read `schema.md` and `index.md`.
2. Inventory all Markdown pages recursively under `wiki/`. Treat `_index.md` files as indexes, not content pages.
3. Build a slug map from content-page filenames and extract every `[[wikilink]]` target, ignoring aliases (`|...`) and headings (`#...`).
4. Run the checks below using the agent's native search/read capabilities:

### Critical

- **Missing or malformed frontmatter** — page does not start with a complete `---` block or lacks `title`, `category`, `date_created`, or `date_updated`.
- **Broken wikilink** — target slug does not resolve to a content page.
- **Orphan page** — content page has no incoming wikilink from another page or index.
- **Invalid source reference** — a `source_docs:` entry is non-empty but does not resolve to a file under `raw/`.

### Important

- **Missing catalog entry** — content page is absent from `index.md`.
- **Missing category index entry** — when `wiki/{category}/_index.md` exists, it does not link the page.
- **Thin page** — fewer than 50 prose words outside frontmatter and headings.
- **Cross-reference gap** — two clearly related existing pages mention the same canonical entity but do not link to each other.

### Informational

- Duplicate or ambiguous slugs across category folders.
- Stale pages whose `date_updated` is more than six months old.
- Unlinked glossary terms that appear repeatedly in content.

5. Present findings by severity with counts, affected paths, and a specific fix for every critical or important issue.
6. Do not modify files unless the user asks for fixes. If fixes are requested, apply them and rerun this full procedure.
7. For an ingest gate, compare before/after findings and require **zero new issues introduced by that ingest**. Pre-existing unrelated findings may remain documented.

## Output

```markdown
## Wiki Health

| Severity | Count |
|---|---:|
| Critical | N |
| Important | N |
| Informational | N |

### Findings
| Severity | Path | Finding | Fix |
|---|---|---|---|
```
~~~

---

#### Skill: `plan-week`

**Claude Code description** (for `.claude/skills/plan-week/SKILL.md` frontmatter):

```yaml
name: plan-week
description: "Plan the upcoming ISO week: resolve active week (TZ Europe/Paris), lift carry-over from prior week's 'Seed for W+1' block, aggregate open `- [ ]` todos from project + meeting pages, draft a Monday plan grouped by topic. Trigger: 'plan week', 'Monday plan', '/plan-week'."
```

**Body** (save to all 3 paths — `.github/instructions/plan-week.instructions.md`, `.claude/skills/plan-week/SKILL.md`, `memory/workflows/plan-week.md`):

```markdown
# Plan Week

When the user says "plan week", "Monday plan", or "/plan-week":

## Resolve the memory root

Resolve `WIKI_ROOT` using `memory/schema.md`, then `schema.md`, then the pointer in `AGENT.md`. Stop with the missing path if none contains both `schema.md` and `index.md`. All paths below are relative to `WIKI_ROOT`.

1. Resolve active ISO week (TZ Europe/Paris) → `ops/weekly/2026-W{NN}.md`. If missing, create the minimal weekly skeleton defined by the `ingest` skill.
2. Lift carry-over from prior week's `### Seed for W{NN}` block.
3. Find open `- [ ]` todos recursively under `wiki/`, prioritizing pages updated in the last 14 days.
4. Optionally use any connected work-data source available to the agent for the next 7 days of calendar, flagged mail, or open collaboration threads. Skip this step when no such tool is available.
5. Draft `## 🎯 Monday plan` grouped by `### [[topic]]`. Show diff. User confirms.
6. Update `touches: []` frontmatter with topic slugs touched. Bump `date_updated`.

Anti-patterns:
- ❌ Do not write to `ops/activity.jsonl` — planning ≠ work.
- ❌ Do not auto-resolve todos.
- ❌ Topics must be slugs in `index.md` — else group under `### unmapped`.
```

---

#### Skill: `close-week`

**Claude Code description** (for `.claude/skills/close-week/SKILL.md` frontmatter):

```yaml
name: close-week
description: "Close out the working ISO week: aggregate ops/activity.jsonl events, regenerate the activity table between BEGIN/END sentinels, draft Friday review (wins, misses, lessons to graduate, seed for next week), freeze the week file. Trigger: 'close week', 'Friday review', '/close-week'."
```

**Body** (save to all 3 paths — `.github/instructions/close-week.instructions.md`, `.claude/skills/close-week/SKILL.md`, `memory/workflows/close-week.md`):

~~~markdown
# Close Week

When the user says "close week", "Friday review", or "/close-week":

## Resolve the memory root

Resolve `WIKI_ROOT` using `memory/schema.md`, then `schema.md`, then the pointer in `AGENT.md`. Stop with the missing path if none contains both `schema.md` and `index.md`. All paths below are relative to `WIKI_ROOT`.

1. Resolve active ISO week (TZ Europe/Paris) → `ops/weekly/2026-W{NN}.md`.
2. **Aggregate** `ops/activity.jsonl` events for that week — group by `topic`, count `touches`, list `days`, find `last`. Sort by touches desc.
3. **Regenerate the activity block** between the sentinels (wholesale replace):
   ```
   <!-- BEGIN GENERATED ACTIVITY -->
   ...table...
   <!-- END GENERATED ACTIVITY -->
   ```
   Wikilink rule: `[[topic]]` only if `resolved: true`; else plain text + `*(unresolved)*`.
4. **Optional connected-source pull** for "what shipped" — sent mail, collaboration decisions, meetings, or modified files. Skip when no work-data tool is available.
5. **Draft Friday review** sections: Wins · Misses · Lessons → graduate (propose ingest targets, don't auto-run) · Seed for W+1 (top-3 carry-over per topic).
6. **Freeze**: `status: closed`, bump `date_updated`, append `log.md` entry: `... CLOSE-WEEK | 2026-W{NN} | events: N | topics: [...] | wins: N | lessons-promoted: N`.
7. **(Optional) Seed W+1** — create `ops/weekly/{next}.md` skeleton.

Anti-patterns:
- ❌ Do not edit outside the sentinels on regenerate.
- ❌ Do not auto-`/ingest` lessons — explicit user confirm per item.
- ❌ Do not reopen a closed week. Late events → current open week with a note.
- ❌ `ops/activity.jsonl` is append-only — never delete events at close.
~~~

---

#### Skill: `project-status`

**Claude Code description** (for `.claude/skills/project-status/SKILL.md` frontmatter):

```yaml
name: project-status
description: "Produce a 30-second situational-awareness briefing for any child project: tech stack, folder structure, git history, recent changes, deployment status, current state, link to wiki project page. Trigger: 'project status', 'status briefing', '/project-status'."
```

**Body** (save to all 3 paths — `.github/instructions/project-status.instructions.md`, `.claude/skills/project-status/SKILL.md`, `memory/workflows/project-status.md`):

~~~markdown
# Project Status

When the user says **"project status"**, **"status briefing"**, or invokes `/project-status` from inside any project directory (NOT memory itself), produce a complete situational-awareness briefing so the user can get up to speed on that project in 30 seconds.

> This skill is for any child project. When invoked from the memory system itself, refuse and direct the user to the wiki because the wiki is its status.
>
> **Coexists with the per-project `/status` command** that ships in every scaffolded project under `.claude/commands/status.md`. The per-project version is Claude-Code-specific. THIS memory skill is the agent-agnostic version (works under GitHub Copilot CLI, Claude Code, or any tool that loads `.github/instructions/`). When both are available, prefer the per-project one if you are inside Claude Code (richer integration), otherwise use this skill.

## Instructions

Gather information from ALL the sources below, then produce a single structured briefing. Use parallel tool calls to speed up the research.

### Resolve the memory root

1. If the current project contains `schema.md` or `memory/schema.md`, it is the memory system or its installer; refuse as described above.
2. Otherwise follow the memory-wiki path declared in the child project's `AGENT.md`.
3. If no memory root resolves, continue the codebase briefing but mark the wiki page as unavailable instead of guessing a personal path.

### 1. Codebase analysis

- **Tech stack**: languages, frameworks, key dependencies (check `package.json`, `requirements.txt`, `pyproject.toml`, `*.csproj`, `Cargo.toml`, `go.mod`, `pom.xml`, etc.)
- **Folder structure**: high-level tree (max 2 levels deep), explain what each top-level folder contains
- **Key files**: entry points, config files, main modules
- **Architecture patterns**: monolith/microservices, API style (REST/GraphQL/gRPC), state management, key abstractions
- **Size**: approximate number of source files and lines of code

### 2. Project history — what we've done

- Read `AGENT.md` for project overview and objectives
- Read the project's page at `{WIKI_ROOT}/wiki/projects/{project-slug}.md` for lessons and reference, if it exists
- Summarise git log: total commits, contributors, major milestones
- Run: `git log --oneline --since="2 weeks ago"` for recent activity
- Run: `git log --oneline --all | tail -5` for the earliest commits

### 3. Last modifications

- Run: `git log -5 --format="%h %s (%ar)"` for the last 5 commits with relative dates
- Run: `git diff --stat HEAD~3` to show what files changed recently (if enough commits exist)
- Check `git status` for any uncommitted work in progress
- Check for any open branches: `git branch -a`

### 4. Deployment status

Check for deployment indicators and report what you find:

- **Azure (azd)**: check for `azure.yaml`, `.azure/` folder, `infra/` folder with Bicep files
- **GitHub Actions**: check `.github/workflows/` for CI/CD pipelines
- **Docker**: check for `Dockerfile`, `docker-compose.yml`
- **Other CI/CD**: check for `.gitlab-ci.yml`, `Jenkinsfile`, `.circleci/`, `bitbucket-pipelines.yml`
- **Git tags**: run `git tag --sort=-creatordate | head -5` for release/deploy tags
- **Last deploy**: if azd is used, check `.azure/` for environment state. If GitHub Actions, note the workflow files and what they do.
- If NO deployment config is found, say "No deployment configuration detected"

### 5. Current state

- Current branch and how it relates to main/master
- Any uncommitted changes or stashed work (`git stash list`)
- Open TODO items in code: search for `TODO`, `FIXME`, `HACK` in source files (report count, not each one)

## Output format

Produce a briefing in this exact format:

```
## 🔍 Project Status: {project name}

### Tech Stack
{languages, frameworks, key deps — one line each}

### Architecture
{folder structure overview + patterns — keep it brief}

### History
- **Created:** {first commit date}
- **Total commits:** {count}
- **Recent activity:** {last 2 weeks summary}

### Last 5 Changes
{table: hash | message | when}

### Deployment
{deployment status, last deploy if known, CI/CD setup}

### Current State
- **Branch:** {current branch}
- **Uncommitted work:** {yes/no + summary}
- **Open TODOs:** {count}

### Wiki page
- Link to `{WIKI_ROOT}/wiki/projects/{slug}.md` (or note that it does not exist yet)

### Key Takeaways
{2-3 bullet points: what's the most important thing to know right now}
```

Keep the entire briefing concise and scannable. No fluff. The user wants to read this in 30 seconds and know exactly where things stand.
~~~

---

#### Skill: `review-sessions`

**Claude Code description** (for `.claude/skills/review-sessions/SKILL.md` frontmatter):

```yaml
name: review-sessions
description: "Analyse coding-agent session data (GitHub Copilot CLI events.jsonl and/or Claude Code conversation jsonl) to surface workflow efficiency, prompt-quality patterns, error trends, tool usage, security hygiene, session patterns. Supports `--agent {copilot,claude,all}`. Trigger: 'review sessions', 'session review', '/review-sessions'."
```

**Body** (save to all 3 paths — `.github/instructions/review-sessions.instructions.md`, `.claude/skills/review-sessions/SKILL.md`, `memory/workflows/review-sessions.md`):

~~~markdown
# Review Sessions

When the user says **"review sessions"**, **"session review"**, or invokes `/review-sessions`, analyse coding-agent session data to identify workflow improvements, prompt-quality patterns, error trends, and security hygiene issues.

Works across both supported agents:

| Agent | Where sessions live | Format |
|---|---|---|
| **GitHub Copilot CLI** | `~/.copilot/session-state/{session-id}/events.jsonl` (+ `plan.md`, `checkpoints/`, `command-history-state.json`) | JSONL event stream — typed events (`session.start`, `session.mode_changed`, `turn.user`, `turn.assistant`, `tool.invoked`, …) with `timestamp`, `id`, `parentId` |
| **Claude Code** | `~/.claude/projects/{project-hash}/{session-id}.jsonl` (+ `~/.claude/history.jsonl`) | JSONL conversation turns — `type: user|assistant|tool_use|tool_result` records with timestamps |

## Resolve the memory root

1. If `memory/schema.md` exists in the current workspace, set `WIKI_ROOT` to `memory/`.
2. Else if `schema.md` exists, set `WIKI_ROOT` to the current directory.
3. Else follow the memory-wiki path in `AGENT.md`.
4. If no folder containing both `schema.md` and `index.md` can be resolved, report the missing path and stop.

All `ops/...` paths below are relative to `WIKI_ROOT`.

## Scope modifiers

Interpret these optional modifiers from the user's request:

- `--agent {copilot,claude,all}` — source to review; default `all`
- `--all` — ignore the watermark and review every session
- `--project SLUG` — match the session `cwd` or git root
- `--since YYYY-MM-DD` — include sessions on or after this date
- No modifiers — incremental review using `ops/review-state.json`

## Step 1: Discover and normalize sessions directly

Use the agent's native file listing, search, JSON/JSONL reading, and reasoning capabilities. **Do not require or create a helper extraction script.**

1. Inventory session files for the selected agent source(s).
2. For incremental mode, read `ops/review-state.json` if it exists and exclude namespaced file IDs already present in `watermark.reviewed_files`. A file ID is `copilot:{absolute-path}` or `claude:{absolute-path}`.
3. Apply project and date filters before reading large files.
4. Read each JSONL file in manageable chunks. Parse each line independently; count and report malformed lines instead of silently discarding them.
5. Normalize records into this common in-memory model:
   - `agent`: `copilot` or `claude`
   - `session_id`, `timestamp`
   - `kind`: `user_turn`, `assistant_turn`, `tool_call`, `tool_result`, `error`, or `mode_change`
   - `text`, `tool_name`, `success`, `duration_ms` when available
6. Copilot mapping: use event `type` values such as `turn.user`, `turn.assistant`, `tool.invoked`, tool completion/error events, and `session.mode_changed`.
7. Claude mapping: use `type: user|assistant` records and nested `tool_use` / `tool_result` content; infer plan-mode changes only when explicitly represented.
8. Keep the processed namespaced file IDs for the state update in Step 6.

## Step 2: Handle "nothing new"

If the filtered inventory contains no unreviewed session files, report:
- When the last review was performed
- How many total sessions are available **per agent**
- Suggest running with `--all` (and optionally `--agent copilot` or `--agent claude`) for a full review

Stop here — do not generate an empty report or change the watermark.

## Step 3: Interpret the findings

Analyse the JSON output across all 6 dimensions. For each, provide:
- **Key findings** — cite specific numbers and examples, not just summaries
- **What's working well** — positive patterns to reinforce
- **Areas for improvement** — specific, actionable suggestions
- **Per-agent split** when behaviour materially differs between Copilot CLI and Claude Code (e.g., plan-mode adoption, subagent usage, error rate)

### Dimensions

1. **Workflow efficiency** — session lengths, turn durations, restart frequency, plan-mode adoption (Copilot: `session.mode_changed` events; Claude: plan-mode toggle in turns)
2. **Prompt quality** — average length, vague prompts (cite examples), correction rate, multi-intent prompts
3. **Error patterns** — error rate, retry loops (cite specifics), most common errors, "file not read" errors, tool failures
4. **Tool usage** — most/least used tools, subagent adoption, Write vs Edit ratio, task-management adoption (TodoWrite / SQL todos)
5. **Security hygiene** — any secrets detected (cite masked values), bypass-permissions rate (Copilot: `--allow-all-tools`; Claude: `--dangerously-skip-permissions`)
6. **Session patterns** — peak hours, busiest days, project distribution, knowledge capture rate (how often `end-session` or `ingest` is invoked)

## Step 4: Build the recommendation table

| Priority | Finding | Recommendation | Effort | Applies to |
|----------|---------|----------------|--------|------------|
| HIGH | ... | ... | Low/Medium/High | copilot / claude / both |
| MEDIUM | ... | ... | ... | ... |
| LOW | ... | ... | ... | ... |

Rules:
- HIGH = security issues, frequent errors, significant time waste
- MEDIUM = suboptimal patterns with clear improvements
- LOW = nice-to-have optimizations
- Maximum 10 recommendations
- Use the **Applies to** column to make agent-specific guidance explicit

## Step 5: Save the full report

Create `ops/review-reports/` if needed and save to `ops/review-reports/YYYY-MM-DD.md`.

Format:

```markdown
# Session Review Report — YYYY-MM-DD

## Executive Summary
[Top 3 findings in bullet points — call out per-agent splits when relevant]

## Metrics Overview
| Metric | Copilot CLI | Claude Code | Combined |
|---|---|---|---|
| Sessions reviewed | ... | ... | ... |
| Total turns | ... | ... | ... |
| Avg turn duration | ... | ... | ... |
| Error rate | ... | ... | ... |
| Plan-mode rate | ... | ... | ... |

## Detailed Analysis

### 1. Workflow Efficiency
### 2. Prompt Quality
### 3. Error Patterns
### 4. Tool Usage
### 5. Security Hygiene
### 6. Session Patterns

## Recommendations
[The prioritized table from Step 4]

## Trend Deltas
[If previous snapshots exist, show changes since last review]
```

## Step 6: Update state

Update `ops/review-state.json`:
1. Set `watermark.last_review_date` to today's ISO date
2. Append the namespaced processed file IDs collected in Step 1 to `watermark.reviewed_files`, deduplicated, so re-processing one agent does not invalidate the other
3. Append a trend snapshot to `trend_snapshots`:
   ```json
   {
     "date": "YYYY-MM-DD",
     "by_agent": {
       "copilot": { "sessions_reviewed": N, "error_rate": X.XXX, "plan_mode_rate": X.XXX, "avg_turn_duration_ms": N },
       "claude":  { "sessions_reviewed": N, "error_rate": X.XXX, "plan_mode_rate": X.XXX, "avg_turn_duration_ms": N }
     },
     "combined": { "sessions_reviewed": N, "correction_rate": X.XXX, "subagent_rate": X.XXX, "secrets_detected": N }
   }
   ```

## Step 7: Knowledge graduation

If any finding is cross-cutting (applies beyond one project), update the relevant page under `wiki/lessons/`, `wiki/patterns/`, or `agent-config/knowledge/`.

## Step 8: Show results

Display to the user:
1. **Executive summary** — top 3 findings (with per-agent annotation when relevant)
2. **Recommendation table** — full table including the **Applies to** column
3. **Report path** — where the full report was saved
4. **Trend deltas** — if previous snapshots exist, show key metric changes per agent (arrows: up/down/stable)
~~~

---

#### Skill: `new-engagement`

**Claude Code description** (for `.claude/skills/new-engagement/SKILL.md` frontmatter):

```yaml
name: new-engagement
description: "Scaffold client engagement projects from the installed project template: parse client, topic, format, and destination; create folders; pre-fill AGENT.md; create a wiki page; initialize git. Trigger: 'new engagement', 'scaffold engagement', '/new-engagement'."
```

**Body** (save to all 3 paths — `.github/instructions/new-engagement.instructions.md`, `.claude/skills/new-engagement/SKILL.md`, `memory/workflows/new-engagement.md`):

~~~markdown
# New Engagement

When the user says **"new engagement"**, **"scaffold engagement"**, or invokes a slash command like `/new-engagement`, scaffold one or more client engagement projects from the resolved project template.

## Resolve required roots

Before scaffolding:

1. Resolve `WIKI_ROOT` using `memory/schema.md`, then `schema.md`, then the memory-wiki path declared in `AGENT.md`.
2. Resolve `TEMPLATE_ROOT` by checking for `project-template/` beside `WIKI_ROOT`, then the path declared in `AGENT.md`.
3. If the template is absent but network access is available, the agent may clone `https://github.com/ozgurkarahan/ai-agent-memory.git` into a temporary folder and use its `project-template/` directory.
4. If either root remains unresolved, report the missing root and stop. Do not guess a personal path.
5. Remove any temporary clone after scaffolding.

All wiki paths below are relative to `WIKI_ROOT`.

## Step 1: Parse the request

Extract from the user input:
- **Client name** (e.g., "Acme", "Contoso", "Contoso")
- **Topics** — one or more engagement topics, each with a format
- **Projects root** — use an explicit destination from the request or `AGENT.md`; otherwise ask where to create the client workspace

Expected input format: `<ClientName> — <topic1> (format), <topic2> (format)`

Formats: `presentation`, `workshop`, `demo`, `presentation + demo`, or combinations.

If the input is ambiguous or missing details, ask clarifying questions:
- What is the target audience? (e.g., technical leadership, developers, executives)
- What format? (presentation, workshop, demo, or combination)
- What are the key objectives?
- Any specific technologies or topics to cover?

## Step 2: Scaffold each project

For each topic, do the following.

### 2a. Create project directory

```bash
PROJECT_DIR={PROJECTS_ROOT}/{ClientName}/10-projects/{project-slug}
mkdir -p "$PROJECT_DIR"
```

Convert the topic to a kebab-case slug (e.g., "Agent Framework Engagement" → `agent-framework-engagement`).

The standard client workspace layout is `00-client/` (intel), `10-projects/` (delivery repos), `10-projects/_archive/`, `20-assets/` (raw client material), `90-scratch/`. Engagements always go under `10-projects/`.

### 2b. Copy template files

Copy the **canonical files** from `TEMPLATE_ROOT`. The full canonical scaffold is:

```
{project}/
├── AGENT.md                                          # MAIN — overview, env, commands, workflow, refs
├── CLAUDE.md                                         # Thin shim → "Read AGENT.md"
├── .claude/
│   ├── CLAUDE.md                                     # Claude Code project config + Project Context block
│   └── commands/status.md                            # /status slash-command for 30-sec briefing
├── .github/
│   ├── copilot-instructions.md                       # GitHub Copilot CLI instructions
│   └── instructions/
│       └── end-session.instructions.md               # end-session shim (5 steps)
├── .gitignore                                        # tracks .claude/CLAUDE.md, .vscode/; ignores runtime caches
├── LICENSE                                           # MIT
├── README.md                                         # Human-facing
└── (format-specific folders)                         # slides/, demos/, exercises/, etc.
```

```bash
# Copy with the platform's native filesystem tools, then strip template history
cp -R "$TEMPLATE_ROOT/." "$PROJECT_DIR/"
rm -rf "$PROJECT_DIR/.git"
```

Use the platform-native equivalent on Windows. After copying, verify the scaffold matches the canonical structure above; do not copy unrelated files that may have accumulated beside the template.

### 2c. Create format-specific folders

| Format | Folders to create |
|--------|-------------------|
| Presentation | `slides/`, `demos/`, `docs/` |
| Workshop | `slides/`, `exercises/`, `solutions/`, `instructor/`, `docs/` |
| Demo | `demos/`, `docs/` |
| Presentation + Demo | `slides/`, `demos/`, `docs/` |
| Mixed/Other | Combine as appropriate |

Create the folders with a `.gitkeep` in each:
```bash
mkdir -p "$PROJECT_DIR/{folder}" && touch "$PROJECT_DIR/{folder}/.gitkeep"
```

### 2d. Pre-fill AGENT.md

Replace the templated `AGENT.md` with engagement-specific content:

```markdown
# {Topic Title}

## Overview

{Client} engagement: {topic description}. Format: {format}. Target audience: {audience}.

## Engagement Details

| Field | Value |
|-------|-------|
| Client | {ClientName} |
| Topic | {Topic} |
| Format | {format} |
| Audience | {audience} |
| Status | Not started |

## Deliverables

{Based on format — see deliverables table below}

## Key Paths

| Path | Description |
|------|-------------|
{format-specific paths}

## Memory Wiki

Root: `{resolved WIKI_ROOT}`

## Reference Documents

| Document | Contents |
|----------|----------|
| `{resolved WIKI_ROOT}/wiki/projects/{project-slug}.md` | Canonical project memory page |

## First Session Instructions

When the agent is first launched in this project, follow these steps:

1. **Read all existing files** in the project to understand current state
2. **Research the topic** — find the latest capabilities, announcements, and best practices for {topic}
3. **Enter plan mode** and propose a detailed engagement plan including:
   - Agenda / slide outline with timing
   - Key talking points and messaging
   - Demo scenarios (if applicable)
   - Exercise descriptions (if workshop)
   - Competitive positioning where relevant
4. **Wait for user approval** before creating any content files
5. **After approval**, scaffold the content structure and begin development
```

### Deliverables by format

| Format | Deliverables |
|--------|-------------|
| Presentation | - [ ] Slide outline with talking points<br>- [ ] Speaker notes<br>- [ ] Demo script (if applicable)<br>- [ ] Leave-behind document<br>- [ ] Q&A preparation |
| Workshop | - [ ] Lab guide with prerequisites<br>- [ ] Exercise instructions (progressive difficulty)<br>- [ ] Solution files<br>- [ ] Instructor notes with timing<br>- [ ] Cheat sheet / quick reference<br>- [ ] Prerequisites checklist |
| Demo | - [ ] Demo script with steps<br>- [ ] Setup instructions<br>- [ ] Fallback plan<br>- [ ] Talking points |

### 2e. Create the project memory page

Project-specific context lives in two places:

1. **`AGENT.md`** in the project repo — identity, workflow, conventions (single source of truth)
2. **`wiki/projects/{project-slug}.md`** under `WIKI_ROOT` — durable project memory (lessons, reference, technical details, related links).

Save the user's engagement request verbatim to `raw/data/new-engagement-{project-slug}-{YYYY-MM-DD}.md`. If a project memory page does not yet exist, create it with this minimal skeleton:

```markdown
---
title: {Topic Title}
category: projects
tags: [{client-tag}, {topic-tags}]
source_docs: ["raw/data/new-engagement-{project-slug}-{YYYY-MM-DD}.md"]
date_created: {YYYY-MM-DD}
date_updated: {YYYY-MM-DD}
---
# {Topic Title}

## Summary
## Context
## Project notes
## Open actions
## Related
## Sources
- `raw/data/new-engagement-{project-slug}-{YYYY-MM-DD}.md`
```

Add the page entry to `wiki/projects/_index.md` when that index exists, update the Projects section and article count in `index.md`, and append to `log.md`.

### 2f. Git init

```bash
cd "$PROJECT_DIR" && git init
git add -A
git commit -m "Initial scaffold: {topic} engagement for {Client}

Scaffolded from project-template by the new-engagement skill.

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

## Step 3: Output results

After scaffolding all projects, output:

### Launch commands

For each project, suggest both agent options. Use whichever CLI the user has installed; the commands are equivalent in scope (allow-all-tools / bypass-permissions). `cd` first so the agent picks up the project's `AGENT.md`.

**PowerShell (Windows):**
```powershell
cd {actual-project-path}

# GitHub Copilot CLI
copilot --allow-all-tools

# Claude Code (alternative)
claude --dangerously-skip-permissions
```

**Bash (Linux / macOS / Git Bash):**
```bash
cd {actual-project-path}

# GitHub Copilot CLI
copilot --allow-all-tools

# Claude Code (alternative)
claude --dangerously-skip-permissions
```

### Suggested initial prompts

For each project, suggest a specific first prompt based on the topic and format. Pipe it to the agent with `-p`:
```powershell
cd {actual-project-path}
copilot --allow-all-tools -p "Research the latest agentic AI capabilities, then propose a presentation outline with demo scenarios for technical leadership"
```

### Summary table

| Project | Path | Format | Status |
|---------|------|--------|--------|
| {topic} | `{actual-project-path}` | {format} | Scaffolded |
~~~

---

#### Mandatory Gate A: executable skills are installed

Before creating any wiki content, inspect the filesystem and prove all of the following:


- `.github/instructions/` contains the 9 generated `*.instructions.md` files.
- `.claude/skills/` contains the 9 generated `{slug}/SKILL.md` files.
- `memory/workflows/` contains the 9 generated `{slug}.md` files.
- Every native file has the required frontmatter.
- After stripping frontmatter, each skill's body matches across all 3 copies.

Expected counts: **9 Copilot + 9 Claude + 9 agent-neutral = 27 files**.

If any check fails, stop here and repair the skill installation. **Do not proceed with a wiki-only installation.**

---


### Step 3: Create `memory/schema.md`

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
| Skills | `wiki/skills/` | Triggerable workflows (durable knowledge of the skill itself) | `ingest`, `query` |
| Agents | `wiki/agents/` | Role-based executors / subagents | `code-review`, `research` |
| Tools | `wiki/tools/` | Products, CLIs, SDKs, APIs, services | `gh-cli`, `playwright-mcp` |
| Queries | `wiki/_queries/` | Synthesized answers to past questions | `how-to-deploy-X` |
| Agent Config | `agent-config/` | Cross-project AI agent configuration | `workflow`, `platform` |

## Article Format

Every wiki page has YAML frontmatter + markdown body:

~~~markdown
---
title: Page Title
category: projects|domains|patterns|lessons|skills|agents|tools|queries
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
```

---

### Step 4: Create `memory/index.md`

```markdown
---
title: Wiki Index
category: meta
date_created: {{today}}
date_updated: {{today}}
---

# Wiki Content Catalog

This is the master catalog of all wiki pages, grouped by category.

**Always update this file when adding or removing pages.** The LLM reads this file to find pages by topic.

## Projects (0 articles)

<!-- Per-project knowledge: architecture, lessons, technical reference -->

## Domains (0 articles)

<!-- Technical domain deep-dives -->

## Patterns (0 articles)

<!-- Reusable architecture & design patterns -->

## Lessons (0 articles)

<!-- Consolidated debugging history & gotchas -->

## Skills (0 articles)

<!-- Durable knowledge about triggerable workflows -->

## Agents (0 articles)

<!-- Role-based executors / subagents -->

## Tools (0 articles)

<!-- Products, CLIs, SDKs, APIs, services -->

## Queries (0 articles)

<!-- Synthesized answers to past questions -->

## Agent Config

- [workflow](agent-config/workflow.md) — Cross-project workflow rules
- [platform](agent-config/platform.md) — Platform & environment preferences

## Installed Workflows

- [ingest](workflows/ingest.md) — Ingest a source into the wiki
- [end-session](workflows/end-session.md) — Wrap up a coding session
- [query](workflows/query.md) — Answer a question from the wiki
- [lint](workflows/lint.md) — Run wiki health checks
- [plan-week](workflows/plan-week.md) — Draft the Monday plan
- [close-week](workflows/close-week.md) — Friday review + activity aggregation
- [project-status](workflows/project-status.md) — 30-sec project briefing
- [review-sessions](workflows/review-sessions.md) — Analyse past sessions for improvements
- [new-engagement](workflows/new-engagement.md) — Scaffold a new client engagement
```

---

### Step 5: Create `memory/log.md`

```markdown
---
title: Activity Log
category: meta
date_created: {{today}}
date_updated: {{today}}
---

# Activity Log

Append-only log of all wiki changes. Every ingest, update, or significant edit gets a line.

Format: `- **YYYY-MM-DDTHH:MM** | TYPE | "description" | metadata`

Types: `INGEST`, `UPDATE`, `QUERY`, `CLOSE-WEEK`, `LINT`

## Log

- **{{today}}T00:00** | INIT | "Memory wiki bootstrapped" | bootstrap: ai-agent-memory
```

---

### Step 6: Create `memory/glossary.md`

```markdown
---
title: Glossary
category: meta
date_created: {{today}}
date_updated: {{today}}
---

# Glossary

Canonical terms used across the wiki. One-line definitions. Update when ingesting new acronyms, product names, or domain-specific jargon.

## Terms

<!-- Add entries alphabetically:
- **Term** — one-line definition. See [[related-page]].
-->
```

---

### Step 7: Create `memory/agent-config/workflow.md`

```markdown
---
title: Cross-Project Workflow Rules
category: agent-config
date_created: {{today}}
date_updated: {{today}}
---

# Cross-Project Workflow Rules

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
- Follow the end-session skill (`memory/workflows/end-session.md` or trigger word "end session").

**Wiki compounding (when significant work was done):**
- If a reusable pattern was discovered, create or update a page in `memory/wiki/patterns/`.
- If a domain gotcha was learned, update the relevant `memory/wiki/domains/*.md` page.
- Update `memory/log.md` with: `- **{timestamp}** | UPDATE | "{what changed}" | project: {name}`

## Available Skills

The following skills are installed via tri-surface (both GitHub Copilot CLI and Claude Code can trigger them):

| Skill | Trigger | Purpose |
|---|---|---|
| `ingest` | "ingest X" | Compile a source into the wiki with raw-source and graph checks |
| `end-session` | "end session", "wrap up" | Capture lessons, update project page, git check |
| `query` | "query X", "what do we know about X" | Answer a question with `[[wikilinks]]` |
| `lint` | "lint", "health check" | Run wiki health checks, report findings |
| `plan-week` | "plan week", "Monday plan" | Draft the ISO week's plan |
| `close-week` | "close week", "Friday review" | Aggregate the week's activity, freeze the file |
| `project-status` | "project status" (from inside a child project) | 30-sec situational briefing |
| `review-sessions` | "review sessions" | Analyse past sessions for workflow improvements |
| `new-engagement` | "new engagement <Client> — <topic> (format)" | Scaffold a new client engagement from `project-template/` |

## Project Structure Convention

Every project scaffolded by `new-engagement` (or created manually) has this shape:

```
project-root/
├── AGENT.md                                            # MAIN — overview, env, commands, workflow, refs
├── CLAUDE.md                                           # Thin shim → "Read AGENT.md"
├── README.md                                           # Human-facing
├── LICENSE                                             # Open-source license
├── .gitignore
├── .github/
│   ├── copilot-instructions.md                         # GitHub Copilot CLI shim → AGENT.md
│   └── instructions/
│       └── end-session.instructions.md                 # Per-project end-session shim
├── .claude/
│   ├── CLAUDE.md                                       # Claude Code project config
│   └── commands/
│       └── status.md                                   # /status slash-command (30-sec briefing)
└── (format-specific folders: slides/, demos/, exercises/, docs/...)
```

Lessons learned and technical reference are centralized in `memory/wiki/projects/{project-name}.md` — not duplicated in the repo.
```

---

### Step 8: Create `memory/agent-config/platform.md`

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
<!-- Append discoveries here. Format: ### Lesson title\n- What/Why/How -->

## Open Actions
<!-- Active work items -->

## Related
<!-- [[wikilinks]] to domains, patterns, lessons -->

## Sources
<!-- Reference docs, URLs, raw/ files -->
```

#### Create `memory/templates/lesson.md`

```markdown
---
title: "{{title}}"
category: lessons
tags: []
source_docs: []
date_created: {{date}}
date_updated: {{date}}
---

# {{title}}

## Context
<!-- Where this came up, what we were doing -->

## What Happened
<!-- The failure mode, error message, surprise -->

## Root Cause
<!-- The actual underlying reason -->

## Fix
<!-- What we did, why it works -->

## Prevention
<!-- How to avoid hitting this again -->

## Related
<!-- [[wikilinks]] -->
```

---

### Step 10: Create project root files

#### Create `AGENT.md` at the project root

```markdown
# AGENT.md

This project uses a **persistent memory wiki** at `memory/`. Read these files to understand the workflow:

- `memory/agent-config/workflow.md` — Cross-project rules (plan before coding, verify before done, etc.)
- `memory/agent-config/platform.md` — Platform & environment preferences
- `memory/schema.md` — Wiki governance and article format
- `memory/index.md` — Content catalog (read first when answering a query)
- `memory/glossary.md` — Canonical terms

## Triggerable Skills

The following workflows can be invoked by name (both GitHub Copilot CLI and Claude Code will route them):

| Trigger | Skill |
|---|---|
| "ingest <X>" | Compile X into the wiki |
| "query <Q>" | Answer Q from the wiki |
| "end session" | Capture lessons, update docs, git check |
| "lint" | Run wiki health checks |
| "plan week" | Draft this week's Monday plan |
| "close week" | Friday review + activity aggregation |
| "project status" | 30-sec briefing of the current project |
| "review sessions" | Analyse past sessions for improvements |
| "new engagement <Client> — <topic> (<format>)" | Scaffold a new engagement from `project-template/` |

## Project-Specific Notes

<!-- Add project-specific instructions here. Tech stack, key commands, etc. -->
```

#### Create `CLAUDE.md` at the project root

```markdown
# Claude Code Instructions

Read `AGENT.md` for all project instructions, workflow rules, and references.
```

#### Create `.github/copilot-instructions.md` at the project root

```markdown
# GitHub Copilot Instructions

Read `AGENT.md` for all project instructions, workflow rules, and references.

All triggerable skills live under `.github/instructions/` and are auto-loaded via `applyTo: "**"`.
```

---

### Step 11: Create the required `project-template/` scaffold

The `new-engagement` skill uses `project-template/` as its offline source when scaffolding a client engagement. Create all 9 files below at `project-template/<path>`; do not skip this step.

---

#### Create `project-template/LICENSE`

```text
MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

#### Create `project-template/README.md`

~~~markdown
# {Project Name}

> **Template starter** — Replace this README with the actual project description after the `new-engagement` skill (or a manual copy) has scaffolded the engagement.

## What this template provides

A minimal, agent-agnostic starting skeleton for any new project — designed to plug straight into the [ai-agent-memory](https://github.com/ozgurkarahan/ai-agent-memory) wiki pattern. Every file points one or more agents back at the same `AGENT.md` so context flows from a single source of truth.

| Path | Purpose | Read by |
|------|---------|---------|
| `AGENT.md` | **The** project context (overview, env, commands, conventions). Edit this first. | All agents (standard) |
| `CLAUDE.md` | Thin shim → "Read `AGENT.md`" | Claude Code (standalone) |
| `.claude/CLAUDE.md` | Claude Code project-scoped config + project-context block | Claude Code (in-repo) |
| `.claude/commands/status.md` | `/status` slash-command — 30-second project briefing | Claude Code |
| `.github/copilot-instructions.md` | Copilot pointer → `AGENT.md` | GitHub Copilot |
| `.github/instructions/end-session.instructions.md` | "End session" trigger — captures lessons before context is lost | GitHub Copilot CLI |
| `.gitignore` | Sensible defaults (OS, editor, env, Python). Tracks `.claude/CLAUDE.md` and `.claude/commands/`; ignores everything else under `.claude/`. | Git |
| `LICENSE` | MIT (change as needed) | Humans |

## Using this template

### Option 1 — `new-engagement` skill (automated)

If you've adopted the `ai-agent-memory` wiki pattern, invoke the [`new-engagement`](https://github.com/ozgurkarahan/ai-agent-memory/blob/master/.github/instructions/new-engagement.instructions.md) skill. It resolves the installed template, copies this scaffold, pre-fills `AGENT.md`, creates format-specific folders, and initialises git.

### Option 2 — Manual copy

```bash
# 1. Pick this template up
cp -R <ai-agent-memory-clone>/project-template <destination>
cd <destination>
rm -rf .git

# 2. Edit AGENT.md to describe the project (overview, env, key paths, conventions)
$EDITOR AGENT.md

# 3. Init git
git init && git add -A && git commit -m "Initial scaffold"
```

## After scaffolding — first session

When an agent first opens the scaffolded project:

1. **Read all existing files** to understand current state
2. **Read `AGENT.md`** — that's the project's identity
3. **Enter plan mode** (or equivalent) and propose a detailed plan before changing anything
4. **Wait for user approval** before creating any content files

## Pairing with the wiki

Declare the installed memory-wiki root in `AGENT.md`. Project-specific lessons are graduated back to that wiki via the [`end-session`](https://github.com/ozgurkarahan/ai-agent-memory/blob/master/.github/instructions/end-session.instructions.md) skill at the end of each coding session — that's the loop that keeps project memory compounding instead of evaporating.

## License

MIT — see [LICENSE](LICENSE).
~~~

---

#### Create `project-template/.gitignore`

```gitignore
# OS
.DS_Store
Thumbs.db

# Editors
.vscode/
.idea/
*.swp

# Claude Code (track project config + slash commands, ignore personal state)
.claude/*
!.claude/CLAUDE.md
!.claude/commands/
!.claude/commands/**

# Environment
.env
.env.*

# Python
__pycache__/
venv/
```

---

#### Create `project-template/AGENT.md`

```markdown
# {PROJECT_NAME}

## Overview

{One-paragraph description of what this project does and why it exists.}

## Architecture

{Key components, data flow, tech stack.}

## Quick Reference

### Setup
{Commands to set up the project.}

### Common Commands
{Build, test, deploy commands.}

## Key Paths

| Path | Description |
|------|-------------|
| {path} | {description} |

## Workflow Rules

The shared memory wiki root is `{MEMORY_WIKI_PATH}`. Replace this placeholder with the actual path when scaffolding the project, then read `{MEMORY_WIKI_PATH}/agent-config/workflow.md` for global rules.

1. **Plan Before Coding** — For any task with 3+ steps, outline first.
2. **Verify Before Done** — Never mark complete without proving it works.
3. **Learn From Mistakes** — Update the project wiki page after corrections.
4. **No Blind Retries** — Diagnose root cause on failure.
5. **Keep It Simple** — Don't over-engineer.

## Platform & Environment

{OS, runtime, key dependencies.}

## What NOT To Do

- Do not create files unless necessary — prefer editing.
- Do not over-engineer simple solutions.
- Do not commit secrets or `.env` files.
- Do not skip verification steps.
```

---

#### Create `project-template/CLAUDE.md`

```markdown
# Claude Code Instructions

Read `AGENT.md` for all project instructions, workflow rules, and references.
```

---

#### Create `project-template/.github/copilot-instructions.md`

```markdown
# Copilot Instructions

Read these files for full context:

- `AGENT.md` — Project instructions, workflow rules, architecture, key paths

## Copilot-Specific Tips

- Use `@workspace` to give Copilot full project context
- Pin important files in chat for persistent context
- Use Copilot Edits (Ctrl+Shift+I) for multi-file changes
- Run the project's available tests and checks before reporting completion
```

---

#### Create `project-template/.github/instructions/end-session.instructions.md`

```markdown
---
applyTo: "**"
---

# End Session — Project Shim

When the user says **"end session"**, **"wrap up"**, or **"done for today"**, wrap up the current coding session by capturing lessons and graduating them to the central memory wiki.

This file is a **per-project shim**. Read `AGENT.md` and resolve the memory wiki root it declares. The canonical procedure is:

- `{memory-root}/workflows/end-session.md`

If `AGENT.md` does not declare a valid folder containing `schema.md` and `index.md`, report that wiki compounding is blocked and continue only with the Git check. Do not guess a home-directory path.

## Summary of steps (abridged)

1. **Project wiki page** — Check if `{memory-root}/wiki/projects/{project}.md` needs updates from today's work — lessons, decisions, technical details, status. Propose the changes.
2. **Wiki compounding** — If significant lessons or patterns were discovered:
   - Update relevant domain pages under `{memory-root}/wiki/domains/`
   - Add new glossary terms to `{memory-root}/glossary.md`
   - Create or update pattern / lesson pages if applicable
   - Append an entry to `{memory-root}/log.md`
3. **Git check** — Run `git status` and warn about uncommitted changes.
4. **Summary** — Present a table:

| Area | Status | Action |
|------|--------|--------|
| Project docs | Up to date / Updated | ... |
| Wiki (project page) | Up to date / Updated | ... |
| Wiki (domains / patterns) | Up to date / Graduated | ... |
| Glossary | Up to date / Updated | ... |
| Git | Clean / Has changes | ... |

For the full procedure (with all edge cases), see the canonical file in the central memory wiki.
```

---

#### Create `project-template/.claude/CLAUDE.md`

```markdown
# Claude Code — Project Configuration

> Project-scoped instructions for Claude Code. Lives at `.claude/CLAUDE.md`.
> Loaded automatically by Claude Code when you open this project.

## Project Context

Read `AGENT.md` at the project root for the canonical project identity (overview, environment, key paths, commands, conventions, what-not-to-do).

This file complements `AGENT.md` — `AGENT.md` is the single source of truth, this file just adds Claude-Code-specific guidance.

## Claude Code conventions for this project

- **Plan first** — for any task touching 3+ files or making architectural decisions, propose the plan before implementing
- **Verify before "done"** — never mark a task complete without proving the change works (build, test, smoke check)
- **Learn from mistakes** — at the end of a session, run the `end-session` workflow to graduate lessons back to the central memory wiki
- **Diagnose, don't retry blindly** — on failure, identify root cause before iterating

## Slash commands available in this project

- `/status` — 30-second briefing on this project (tech stack, recent commits, deployment, current state). Defined in `.claude/commands/status.md`.

## Reference

| Document | Contents |
|----------|----------|
| `AGENT.md` | Project identity + workflow rules + reference paths |
| Memory wiki path declared in `AGENT.md` | Shared wiki, lessons, patterns, and glossary |
```

---

#### Create `project-template/.claude/commands/status.md`

~~~markdown
# /status — Project Briefing

When the user types `/status`, produce a 30-second situational-awareness briefing on **this project** so they can get up to speed instantly.

Gather information from all the sources below in parallel, then produce a single structured briefing.

## 1. Codebase analysis

- **Tech stack**: languages, frameworks, key dependencies (check `package.json`, `requirements.txt`, `pyproject.toml`, `*.csproj`, `Cargo.toml`, `go.mod`, `pom.xml`, etc.)
- **Folder structure**: high-level tree (max 2 levels deep)
- **Entry points / key files**: config files, main modules
- **Architecture patterns**: monolith / microservices, API style (REST / GraphQL / gRPC), state management
- **Size**: approximate source files + LOC

## 2. Project history

- Read `AGENT.md` for the project overview and objectives
- `git log --oneline --since="2 weeks ago"` — recent activity
- `git log -5 --format="%h %s (%ar)"` — last 5 commits with relative dates
- `git log --oneline --all | tail -5` — earliest commits (for context)

## 3. Last modifications

- `git diff --stat HEAD~3` (if enough commits exist) — what files changed recently
- `git status` — uncommitted work in progress
- `git branch -a` — open branches
- `git stash list` — stashed work

## 4. Deployment status

Check for deployment indicators:

- **Azure (azd)**: `azure.yaml`, `.azure/`, `infra/*.bicep`
- **GitHub Actions**: `.github/workflows/`
- **Docker**: `Dockerfile`, `docker-compose.yml`
- **Other CI/CD**: `.gitlab-ci.yml`, `Jenkinsfile`, `.circleci/`, `bitbucket-pipelines.yml`
- **Git tags**: `git tag --sort=-creatordate | head -5`

If no deployment config is found, say "No deployment configuration detected".

## 5. Current state

- Current branch and its relation to main / master
- Uncommitted changes / stashed work
- Open `TODO`, `FIXME`, `HACK` count in source files

## Output format

```
## 🔍 Project Status: {project name}

### Tech Stack
{languages, frameworks, key deps — one line each}

### Architecture
{folder overview + patterns — brief}

### History
- **Created:** {first commit date}
- **Total commits:** {count}
- **Recent activity:** {last 2 weeks summary}

### Last 5 Changes
{table: hash | message | when}

### Deployment
{deployment config + last deploy info if known}

### Current State
- **Branch:** {current branch}
- **Uncommitted work:** {yes/no + summary}
- **Open TODOs:** {count}

### Key Takeaways
{2-3 bullets — what's the most important thing to know right now}
```

Keep the briefing scannable. No fluff. The reader should know exactly where things stand in under 30 seconds.
~~~

---


### Step 12: Verification

## Definition of Done

The setup is complete only when every required item below passes. Inspect the files; do not mark boxes based on intended work.

```
[ ] SKILL GATE: 9 Copilot instruction files exist under .github/instructions/
[ ] SKILL GATE: 9 Claude SKILL.md files exist under .claude/skills/
[ ] SKILL GATE: 9 agent-neutral workflow files exist under memory/workflows/
[ ] SKILL GATE: all 9 skill bodies match across the 3 copies after frontmatter is removed
[ ] DEPENDENCY GATE: no installed skill or template requires a helper script that this bootstrap does not create
[ ] PORTABILITY GATE: no installed skill or template contains a maintainer-specific home-directory path
[ ] memory/schema.md exists with YAML frontmatter
[ ] memory/index.md exists with category sections
[ ] memory/log.md exists with INIT entry
[ ] memory/glossary.md exists
[ ] memory/agent-config/workflow.md exists
[ ] memory/agent-config/platform.md exists
[ ] memory/templates/project.md exists with frontmatter template
[ ] memory/templates/lesson.md exists with frontmatter template
[ ] memory/wiki/{projects,domains,patterns,lessons,skills,agents,tools,_queries}/ directories exist
[ ] memory/raw/ directory exists
[ ] memory/ops/weekly/ directory exists and memory/ops/activity.jsonl exists (empty)
[ ] project-template/ scaffold exists with all 9 canonical files
[ ] AGENT.md exists at project root and references memory/agent-config/workflow.md + lists all 9 skills
[ ] CLAUDE.md exists at project root and points to AGENT.md
[ ] .github/copilot-instructions.md exists at project root and points to AGENT.md
```

### Required completion report

Report one of these outcomes:

- `SETUP COMPLETE — 9/9 skills installed for Copilot CLI and Claude Code; 27/27 skill files present; wiki ready.`
- `SETUP INCOMPLETE — <failed checks and missing paths>.` Then continue repairing the failed checks; do not stop at this report unless blocked by permissions or missing tool access.

Do not call a directory under `memory/wiki/skills/` an installed skill surface. It is wiki content only.

Newly created skills may require a **new agent session** before GitHub Copilot CLI or Claude Code discovers them. File verification happens now; discovery is smoke-tested after restarting the agent in this folder.

---

## Next Steps

Setup is complete. Here's how to use your memory system:

1. **Try your first ingest:** Tell your agent `ingest` followed by any topic you've learned today — a debugging breakthrough, a new tool, an architecture decision. The agent will preserve the raw source, compile durable knowledge, update the graph, and run its audit gates.

2. **At the end of your session:** Tell your agent `end session` to capture lessons learned, update project docs, and compound knowledge.

3. **Query your knowledge:** Ask your agent `query <question>` — it will search the wiki and synthesize an answer with `[[wikilink]]` citations.

4. **Weekly rhythm:** On Monday, `plan week`. On Friday, `close week`. The activity log (`memory/ops/activity.jsonl`) accumulates ingest events, and `close-week` aggregates them into the week's file.

5. **Health checks:** Run `lint` periodically to surface orphan pages, broken wikilinks, and thin pages.

6. **Project briefings:** From inside any child project, run `project status` for a 30-second situational summary.

7. **New engagements:** When starting a new client engagement, say `new engagement <Client> — <topic> (<format>)` and the agent will scaffold the project from `project-template/`.

8. **Session review:** Run `review sessions` to analyse GitHub Copilot CLI and Claude Code JSONL data for workflow improvements.

It compounds over time. Each session adds to the wiki. After a few weeks, your agent will have a rich knowledge base of your projects, patterns, and hard-won lessons — and it never forgets.
