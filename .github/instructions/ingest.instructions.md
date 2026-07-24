---
applyTo: "**"
---

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
