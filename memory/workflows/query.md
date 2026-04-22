# Query Workflow

> **Agent-agnostic.** Any AI coding agent can follow these steps to answer questions using the wiki.

When a user asks a question that might be answered by the wiki — project context, past decisions, known patterns, previous debugging lessons — follow this workflow.

---

## Step 1 — Read the Index

Start with `memory/index.md`. Scan the category tables to identify relevant pages:

- **Projects** — for project-specific context, decisions, lessons
- **Domains** — for technology knowledge, framework gotchas
- **Patterns** — for reusable solutions and implementation details
- **Lessons** — for debugging stories and root-cause analysis

**Tip:** Read `memory/glossary.md` too — the user's question might use a term that maps to a specific wiki concept.

---

## Step 2 — Read Relevant Pages

Read the identified pages **in full** (not chunks or summaries). Wiki pages are kept deliberately concise (~300 lines max), so full reads are efficient.

Follow `[[wikilinks]]` to related pages if the initial pages reference relevant context.

---

## Step 3 — Synthesize Answer

Compose your answer with:

- **Direct citations** using `[[wikilinks]]` — e.g., "According to [[retry-with-backoff]], the base delay should be..."
- **Concrete details** from the wiki — don't paraphrase when exact values, code snippets, or rules are available
- **Cross-references** — if the answer touches multiple pages, connect them

**Format example:**
```
Based on [[weather-api]], the Redis cache TTL is 5 minutes. The caching layer
uses the pattern described in [[retry-with-backoff]] for provider failover.
See [[fastapi]] for the async middleware configuration.
```

---

## Step 4 — Note Knowledge Gaps

If the question reveals information that *should* be in the wiki but isn't:

1. Tell the user: "This isn't captured in the wiki yet."
2. Offer to ingest it: "Would you like me to add this to the wiki? Say 'ingest' followed by the information."
3. If the user agrees, switch to the [Ingest Workflow](ingest.md).

**Common gaps:**
- A decision was made but never documented
- A debugging lesson was learned but not written down
- A pattern is used across projects but has no dedicated page
