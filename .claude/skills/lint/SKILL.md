---
name: lint
description: "Run wiki health checks (structural + semantic) and report findings by severity: critical (orphans, missing frontmatter), important (cross-reference gaps, thin pages), informational. Trigger: 'lint', 'health check', 'check wiki'."
---

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
