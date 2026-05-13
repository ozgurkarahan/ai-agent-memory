---
applyTo: "**"
---

# End Session — Project Shim

When the user says **"end session"**, **"wrap up"**, or **"done for today"**, wrap up the current coding session by capturing lessons and graduating them to the central memory wiki.

This file is a **per-project shim**. The canonical procedure lives in the central memory wiki:

- `~/projects/memory/.github/instructions/end-session.instructions.md` (Copilot CLI surface)
- `~/projects/memory/.claude/skills/end-session/SKILL.md` (Claude Code surface)
- `~/projects/memory/memory/workflows/end-session.md` (human-readable reference)

## Summary of steps (abridged)

1. **Project wiki page** — Check if `~/projects/memory/wiki/projects/{project}.md` (or `wiki/projects/{client}/{project}.md` for client engagements) needs updates from today's work — lessons, decisions, technical details, status. Propose the changes.
2. **Wiki compounding** — If significant lessons or patterns were discovered:
   - Update relevant domain pages at `~/projects/memory/wiki/domains/*.md`
   - Add new glossary terms to `~/projects/memory/glossary.md`
   - Create or update pattern / lesson pages if applicable
   - Append an entry to `~/projects/memory/log.md`
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
