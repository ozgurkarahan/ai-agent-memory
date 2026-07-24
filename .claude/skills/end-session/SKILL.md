---
name: end-session
description: "Wrap up the current coding session: update the project wiki page with lessons and decisions, graduate cross-cutting findings to domain / pattern / lesson pages, check git status, present a status table. Trigger: 'end session', 'wrap up', 'done for today'."
---

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
