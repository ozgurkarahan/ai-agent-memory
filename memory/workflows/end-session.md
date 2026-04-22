# End-Session Workflow

> **Agent-agnostic.** Any AI coding agent can follow these steps at the end of a working session.

When a user says **"end session"**, **"wrap up"**, or **"done for today"**, follow this routine to capture knowledge before context is lost.

---

## Step 1 — Capture Lessons

Review what happened during the session. If any of these occurred, update the project's wiki page:

- **Corrections** — The user corrected your approach or assumption
- **Debugging discoveries** — You found a non-obvious root cause
- **Design decisions** — A meaningful choice was made (and why)
- **Tool/library gotchas** — Something didn't work as expected

**Where to write:** `memory/wiki/projects/{project-name}.md` under `## Lessons Learned`

**Format:**
```markdown
### {Date} — {Short title}

**Context:** What you were trying to do
**Problem:** What went wrong or was surprising
**Root cause:** Why it happened
**Rule:** What to do differently next time
```

---

## Step 2 — Cross-Project Knowledge

If a lesson applies beyond the current project, propagate it:

| If the lesson is about... | Update this page |
|---------------------------|------------------|
| A technology or framework | `wiki/domains/{technology}.md` |
| A reusable pattern | `wiki/patterns/{pattern}.md` |
| A debugging story worth preserving | Create `wiki/lessons/{short-name}.md` |

**Remember:** Follow the ingest workflow's graph-update rules — update `index.md`, `glossary.md`, and add backlinks.

---

## Step 3 — Update Log

Append an entry to `memory/log.md`:

```
- **{date}** | UPDATE | "{what changed}" | project: {project-name}
```

Examples:
```
- **2026-04-22** | UPDATE | "Added Redis connection pooling lesson" | project: weather-api
- **2026-04-22** | CREATE | "New lesson: api-auth-debugging" | project: recipe-chatbot
```

---

## Step 4 — Git Check

Run `git status` in the project directory and warn the user about:

- Uncommitted changes
- Untracked files that should be committed
- Files that might contain secrets (`.env`, API keys)

---

## Step 5 — Summary

Report what was updated:

```
## Session Summary

### Knowledge Updates
- Updated `wiki/projects/weather-api.md` — added lesson on Redis TTL pitfall
- Updated `wiki/domains/fastapi.md` — added async middleware note

### Log
- Appended 2 entries to `log.md`

### Git Status
- 3 uncommitted changes in `demo-project/`
- No secrets detected
```
