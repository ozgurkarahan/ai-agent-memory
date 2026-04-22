---
title: Global Workflow Rules
category: meta
date_created: 2026-04-22
date_updated: 2026-04-22
---

# Global Workflow Rules

Rules that apply to every project and session. Read once at session start.

## Core Rules

### 1. Plan Before Coding
For any task with 3+ steps, outline the approach first. Get approval before implementing. No cowboy coding.

### 2. Verify Before Done
Never mark a task complete without proving it works — run tests, check output, verify behavior. "It should work" is not verification.

### 3. Learn From Mistakes
After any correction or unexpected failure, capture the lesson in the project's lessons-learned file. Review lessons at session start to avoid repeating mistakes.

### 4. No Blind Retries
When something fails, diagnose the root cause before retrying. Don't retry non-transient errors. Read the error message.

### 5. Keep It Simple
Don't add features, refactor code, or make improvements beyond what was asked. Solve the stated problem, nothing more.

### 6. Demand Elegance
Within the scope of the task, prefer clean solutions. If a fix is ugly, find a better way. Simplicity and elegance are not opposites.

## Session Routine

### Start of Session
1. Read the project's `AGENT.md` for orientation
2. Read the project's wiki page at `wiki/projects/{project}.md` for accumulated knowledge
3. Review `lessons-learned.md` to avoid past mistakes
4. Check git status for uncommitted work from previous sessions

### End of Session
1. Capture any new lessons in the project's lessons-learned file
2. Update the project's wiki page if significant knowledge was gained
3. Append to `log.md` with a summary of what was ingested or changed
4. Run `git status` and warn about uncommitted changes

## Retrieval Rules

When an agent needs knowledge from the wiki:

1. **Start with `index.md`** — scan the catalog to find relevant pages
2. **Open only relevant pages** — don't read the entire wiki
3. **Prefer summaries** — read the Summary section first; go deeper only if needed
4. **Follow wikilinks** — if a page references another, follow the link for context

## Write Rules

1. Agents **append** to `log.md` — never rewrite or truncate
2. Agents **do not** rewrite `schema.md` or `index.md` unless explicitly asked
3. New pages must be added to `index.md` and linked from at least one other page
4. Use templates from `templates/` when creating new wiki pages

## Project Structure Convention

Every project should have these agent-facing files at the repo root:

| File                        | Purpose                                      |
|-----------------------------|----------------------------------------------|
| `AGENT.md`                  | Project overview for AI agents               |
| `CLAUDE.md`                 | Claude Code-specific instructions            |
| `copilot-instructions.md`   | GitHub Copilot-specific instructions         |
| `.ai/lessons-learned.md`    | Project-specific debugging history           |
| `.ai/project-reference.md`  | Technical details and implementation caveats  |
