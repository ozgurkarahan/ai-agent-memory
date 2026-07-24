---
name: query
description: "Answer a question by searching the wiki: read index.md, find relevant pages, synthesize an answer with [[wikilink]] citations, file the answer in wiki/_queries/, update log.md. Trigger: 'query [question]' or a direct knowledge-base question."
---

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
