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
