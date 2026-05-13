---
name: ingest
description: Ingest a source document into the wiki following the Karpathy LLM Wiki pattern. Compile content into structured frontmatter + Markdown pages, resolve [[wikilinks]] against the existing graph, update related pages, run lint, emit activity event. Trigger: "ingest [source]", "mass ingest [batch]".
---

# Ingest Source — LLM-Compiled Wiki Ingestion (Karpathy Pattern)

Two triggers:

- **"ingest"** — single-source ingest. Follow Phase 1 → Phase 7 as written.
- **"mass ingest"** / **"bulk ingest"** / **"ingest all ... from ..."** — multi-source batch. MUST insert **Phase 0 (Inventory)** and **Phase 2b.5 (Consolidation Planning)** before compiling anything. See [[ingest]] consolidation section for the full pattern and rationale.

## Phase 0: Inventory (mass ingest only)

Before any M365-query-tool / raw pulls:

1. **List every source** you intend to ingest (OneNote sections, files, URLs, query topics).
2. **Save the inventory** to the session folder or as a temp list. Do NOT start pulling yet.
3. **If the source system can't be enumerated** (e.g., M365-query-tool on OneNote hierarchy), explicitly state the limitation and the coverage estimate (e.g., "~70-80% via targeted topic queries") before proceeding.
4. **Ask the user to confirm scope** if the inventory is >10 sources — consolidation decisions are cheaper to agree on upfront than to refactor later.

## Phase 1: Gather Context

1. **Read `~/projects/memory/schema.md`** — understand wiki structure, categories, naming rules
2. **Read `~/projects/memory/index.md`** — get the full list of existing articles with paths (needed for backlink resolution)
3. **Read `~/projects/memory/glossary.md`** — check existing terms
4. **Read the source content** — the file, topic, or conversation findings to ingest

## Phase 2: LLM Compilation (this is YOU — use your reasoning)

Compile the source into structured wiki knowledge. Ask yourself:

### 2a. What type of knowledge is this?
- **Project knowledge** → `wiki/projects/{client-folder}/{slug}.md` for top-level clients (`acme`, `fabrikam`, `contoso`, `northwind`); else `wiki/projects/{slug}.md` (create or update). See [[schema]] "Client-folder rule".
- **Domain/technology knowledge** → `wiki/domains/{slug}.md` (create or update)
- **Reusable pattern** → `wiki/patterns/{slug}.md` (create or update)
- **Debugging lesson / gotcha** → `wiki/lessons/{slug}.md` (create or update)
- **Skill / command / triggerable workflow** → `wiki/skills/{slug}.md` (create or update)
- **Agent / subagent / role-based executor** → `wiki/agents/{slug}.md` (create or update)
- **Tool knowledge** → `wiki/tools/{slug}.md` (create or update; only for products, CLIs, SDKs, APIs, services, utilities)
- **Microsoft colleague / MS-internal entity** → `wiki/microsoft/colleagues/{slug}.md` (MS employees only — customer/partner contacts stay tabular on the relevant `wiki/clients/{slug}.md` hub)
- **Personal career artefact (BR log, goals)** → `wiki/career/{slug}.md`
- **Platform/env knowledge** → `agent-config/platform.md` or `agent-config/knowledge/{domain}.md` (update)

### 2b. Create or update?
- Search `index.md` for existing pages about this topic
- If a page exists → **UPDATE** it (don't create duplicates)
- If no page exists → **CREATE** a new one

### 2c. Compile the article
For **new pages**, generate YAML frontmatter + Markdown body following `schema.md`:

```markdown
---
title: "Descriptive Title"
category: clients|projects|domains|patterns|skills|agents|lessons|tools|meetings|career|microsoft|personal|queries|ops
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
```

For **updates**, surgically edit the existing page — don't rewrite unrelated content.

### 2b.5 Consolidation Planning (REQUIRED when ≥3 related sources, i.e. mass ingest)

Before writing ANY wiki page, produce a consolidation matrix mapping every inventoried source to its target page. Write this to the session folder (e.g., `plan.md`) or present it inline to the user for approval.

| Source (raw snapshot) | Topic / entity | Target page | Action | Rationale |
|---|---|---|---|---|
| m365-query-onenote-acme-...md | Acme contracts + GH→GitLab | wiki/clients/acme.md | UPDATE (append OneNote section) | hub exists, same entity |
| m365-query-onenote-globex-...md | Globex BR | wiki/projects/northwind/segment-customers.md | CREATE (new hub) | no page, 8+ similar non-direct customers share it |
| m365-query-onenote-br-...md | personal BR log | wiki/career/br-personal.md | CREATE | rolling personal log, distinct from team hub |

**Consolidation rules:**

- **Same entity across N sources → ONE page section.** Never create `acme-foo.md` + `acme-bar.md` when `acme.md` exists.
- **Cross-cutting theme in 3+ sources → promote to its own page** (domain / pattern / lesson). Below 3 sources → inline section on an existing hub.
- **Ephemeral / one-off mention → append to nearest hub**, don't create a page.
- **Sibling cohort (N similar entities) → ONE hub page** with a section per sibling. Rule of thumb: if you'd write the same 3 subsections for each, make it a hub (e.g., `northwind-segment-customers.md` covers 9 non-direct customers).
- **Personal rolling log → dedicated page** (e.g., `br-personal.md`), NOT a section on the team page.
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

- **File source** → copy to `raw/{articles|books|pdfs|data}/` using `python scripts/ingest.py raw <file>`
- **Conversation / M365-query-tool / web search** → write the verbatim response to `raw/data/{source}-{slug}-YYYY-MM-DD.md`
- **User-provided text** → save as-is to `raw/data/{slug}-YYYY-MM-DD.md`

The `source_docs:` frontmatter field on every new wiki page MUST point to a real file under `raw/`, not a free-text description. Without this, the ingest is not auditable and violates the Karpathy 3-layer architecture (RAW / WIKI / SCHEMA).

## Phase 5: Lint (ALWAYS — required gate)

**Run the lint after every ingest.** This is non-negotiable — it catches orphan pages, broken wikilinks, and missing backlinks that are trivial to fix immediately but expensive to untangle later.

```powershell
cd ~/projects/memory
$env:PYTHONIOENCODING='utf-8'   # Windows: prevent cp1252 crash on box-drawing chars
python scripts/lint.py --semantic --log
```

Report lint delta attributable to the ingest:
- **New orphan pages introduced?** → add at least one incoming `[[wikilink]]` from a related page
- **New broken links introduced?** → either create the target page or remove the link
- **New thin pages (<50 words)?** → expand the page with real content

Pre-existing issues unrelated to the current ingest can be left for a dedicated lint pass — but **issues the ingest itself created must be fixed in the same turn**.

## Phase 6: Self-Audit Gate (REQUIRED — run this BEFORE reporting)

Before writing the final report in Phase 7, run this 7-item self-audit. If ANY item fails, fix it in the same turn.

```
[ ] 1. Raw source exists under raw/ AND is referenced in source_docs: frontmatter?
      → grep for the new page's source_docs value in raw/ tree
[ ] 2. New page has ≥1 incoming [[wikilink]] from an existing page?
      → grep -r "[[<new-slug>]]" wiki/  → must return ≥1 hit outside the new page itself
[ ] 3. index.md count matches actual file count in the category?
      → compare "## Projects (N articles)" vs `find wiki/projects -name '*.md' -not -name '_index.md' | wc -l` (recursive — client subfolders included)
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

## Phase 7: Report

Report a table:

| Action | File | Change |
|--------|------|--------|
| CREATE/UPDATE | wiki/domains/foo.md | New page: ... |
| UPDATE | wiki/projects/bar.md | Added backlink to [[foo]] |
| UPDATE | index.md | Added foo to Domains |
| UPDATE | glossary.md | Added term: ... |
| APPEND | log.md | INGEST entry |

**Target: 8-15 files touched per ingest.**

Include the self-audit result AND the lint summary in the report:

| Gate | Result |
|------|--------|
| Self-audit (7 items) | 7/7 pass |
| Lint (semantic, post-ingest) | 0 new issues introduced (41 pre-existing unchanged) |

## Phase 8: Emit Activity Event (REQUIRED)

After the report, append **one** line to `~/projects/memory/ops/activity.jsonl` to record this ingest in the operational log. This is what makes the weekly file's activity table aggregate correctly on Friday close-week.

Rules:

1. **Identify the `primary_topic`** — the single canonical wiki page this ingest is about. It must be a slug listed in `index.md`.
   - For a new domain page → its own slug (e.g., `azure-ai-search-sharepoint`).
   - For an update to a project page → the project page slug (e.g., `contoso-archetypes-foundry`).
   - For a meeting recap update → the meeting page slug (e.g., `br-personal`), NOT every related project page.
   - **Do NOT** emit an event per modified file (`index.md`, `glossary.md`, `_index.md`, backlinks…). Those are pipeline exhaust, not work signal.

2. **Identify `secondary_topics`** (0-2 max) — only if the ingest meaningfully co-touches another canonical page. Most ingests have none.

3. **Resolve the active week** — ISO week of `current_datetime` in `Europe/Paris`. Format `2026-W{NN}`.

4. **Append to `ops/activity.jsonl`** — one JSON object per line:

```json
{"ts":"2026-04-25T21:51:00+02:00","week":"2026-W18","source":"ingest","topic":"contoso-archetypes-foundry","secondary":["azure-ai-search-sharepoint"],"resolved":true,"note":"24-Apr meeting recap","files":6}
```

Required fields: `ts` (ISO 8601 with TZ offset), `week`, `source: "ingest"`, `topic`, `resolved` (true/false based on slug existing in `index.md`), `note` (≤80 chars), `files` (count of files CREATEd/UPDATEd in this ingest).
Optional: `secondary` (array of slugs).

5. **Verify the active week file exists** — `ops/weekly/{week}.md`. If missing, create it from the template (frontmatter only — `plan-week` will fill the Monday plan later, or the user will).

6. **Add the slug to the week file's `touches:` frontmatter** (deduped). This is the only edit `ingest` makes to the weekly markdown file — it never edits the activity table directly (that's `close-week`'s job, between the sentinels).

## Anti-Patterns (don't do these)

- ❌ Don't create `[[wikilinks]]` to pages that don't exist in index.md
- ❌ Don't duplicate content already in another page — link to it instead
- ❌ Don't use LLM-generated concept names as slugs — derive from content deterministically
- ❌ Don't skip updating index.md and log.md
- ❌ Don't append raw text to knowledge files — compile it into structured sections
- ❌ Don't point `source_docs:` at a free-text string ("M365-query-tool query") — always a real file under `raw/`
- ❌ Don't skip the lint step — it's a required gate, not optional
- ❌ Don't skip the **self-audit gate** (Phase 6) and jump to reporting — the audit IS the proof the Karpathy pattern was followed
- ❌ Don't mark an ingest "done" until `source_docs:` in the new page points to a real file under `raw/` AND the new page has at least one incoming `[[wikilink]]` from an existing page
- ❌ (mass ingest) Don't start pulling sources before the Phase 0 inventory is written down — leads to forgotten sources and inconsistent coverage
- ❌ (mass ingest) Don't create one wiki page per source — consolidate same-entity / sibling-cohort sources via the Phase 2b.5 matrix
- ❌ (mass ingest) Don't write N log.md entries for one logical batch — one consolidated entry instead
- ❌ (Phase 8) Don't emit an activity event per modified file — only ONE per ingest with `primary_topic`. Pipeline exhaust ≠ work signal.
- ❌ (Phase 8) Don't write to `ops/weekly/{week}.md`'s activity table directly — only `close-week` regenerates it between the sentinels.
