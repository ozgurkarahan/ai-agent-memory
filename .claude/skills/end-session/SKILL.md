---
name: end-session
description: "Wrap up the current coding session: update the project wiki page with lessons and decisions, graduate cross-cutting findings to domain / pattern / lesson pages, check git status, present a status table. Trigger: 'end session', 'wrap up', 'done for today'."
---

# End Session

When the user says "end session", "wrap up", or "done for today":

1. **Project wiki page** — Check if `~/projects/memory/wiki/projects/{project}.md` needs updates from today's work (lessons, decisions, technical details, status). Propose changes. *(Note: legacy `.ai/lessons-learned.md` / `.ai/project-reference.md` were retired 2026-04-22 — all project knowledge now lives directly on the wiki page.)*
2. **Wiki compounding** — If significant lessons or patterns were discovered:
   - Update relevant domain pages at `~/projects/memory/wiki/domains/*.md`
   - Add new glossary terms to `~/projects/memory/glossary.md`
   - Create or update pattern/lesson pages if applicable
   - Append to `~/projects/memory/log.md`
3. **Git check** — Run `git status` and warn about uncommitted changes.
4. **Summary** — Present a table:

| Area | Status | Action |
|------|--------|--------|
| Project docs | Up to date / Updated | ... |
| Wiki (project page) | Up to date / Updated | ... |
| Wiki (domains/patterns) | Up to date / Graduated | ... |
| Glossary | Up to date / Updated | ... |
| Git | Clean / Has changes | ... |
