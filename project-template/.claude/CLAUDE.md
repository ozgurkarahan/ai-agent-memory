# Claude Code — Project Configuration

> Project-scoped instructions for Claude Code. Lives at `.claude/CLAUDE.md`.
> Loaded automatically by Claude Code when you open this project.

## Project Context

Read `AGENT.md` at the project root for the canonical project identity (overview, environment, key paths, commands, conventions, what-not-to-do).

This file complements `AGENT.md` — `AGENT.md` is the single source of truth, this file just adds Claude-Code-specific guidance.

## Claude Code conventions for this project

- **Plan first** — for any task touching 3+ files or making architectural decisions, propose the plan before implementing
- **Verify before "done"** — never mark a task complete without proving the change works (build, test, smoke check)
- **Learn from mistakes** — at the end of a session, run the `end-session` workflow to graduate lessons back to the central memory wiki
- **Diagnose, don't retry blindly** — on failure, identify root cause before iterating

## Slash commands available in this project

- `/status` — 30-second briefing on this project (tech stack, recent commits, deployment, current state). Defined in `.claude/commands/status.md`.

## Reference

| Document | Contents |
|----------|----------|
| `AGENT.md` | Project identity + workflow rules + reference paths |
| Memory wiki path declared in `AGENT.md` | Shared wiki, lessons, patterns, and glossary |
