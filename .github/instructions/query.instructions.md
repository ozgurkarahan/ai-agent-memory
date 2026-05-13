---
applyTo: "**"
---

# Query Wiki

When the user asks a question about the knowledge base or says "query":

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
