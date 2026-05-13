---
applyTo: "**"
---

# Lint Wiki

When the user says "lint", "health check", or "check wiki":

1. Run: `python scripts/lint.py --semantic --log`
2. Present findings by severity:
   - **Critical** — orphan pages, missing frontmatter, suggested new pages (3+ broken refs)
   - **Important** — cross-reference gaps, thin pages
   - **Informational** — unlinked entities, broken links with <3 refs
3. For each critical/important finding, suggest a specific fix
4. If the user wants fixes applied, follow the ingest checklist for all updates
