# Changelog

All notable changes to this repository are documented in this file.

The format is based on [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/).
Versioning follows [Calendar Versioning](https://calver.org/) (`YYYY.0M.MICRO`) — releases ship when meaningful skill or schema changes accumulate, typically once per month. See [CONTRIBUTING.md](CONTRIBUTING.md#releases) for the release process.

## [Unreleased]

## [2026.05.1] — 2026-05-13

Adds Claude Code as a first-class agent surface and polishes the surrounding docs.

### Added

- **`.claude/skills/{slug}/SKILL.md` surface** — Claude Code agents working inside a clone of this repo now auto-discover all 9 skills via Claude Code's project-scoped skill discovery (`.claude/skills/`). Each `SKILL.md` carries the YAML frontmatter Claude Code expects (`name`, `description`) so the skill router can match user requests against the right skill. The repo is now **tri-surface** and treats GitHub Copilot CLI and Claude Code symmetrically:
  - `.github/instructions/{slug}.instructions.md` — Copilot CLI
  - `.claude/skills/{slug}/SKILL.md` — Claude Code
  - `memory/workflows/{slug}.md` — agent-agnostic plain-Markdown reference
- `.gitignore` exception pattern (`.claude/*` + `!.claude/skills/` + `!.claude/skills/**`) so the public skills surface ships with the repo while personal Claude Code state stays ignored.

### Changed

- `CONTRIBUTING.md` — "dual-surface" guidance updated to "tri-surface", with a table summarising each surface's frontmatter requirements and rationale.
- `README.md` — "How It Works" rewritten (was "Three workflows drive the system", now reflects 9 skills); "Agent Compatibility" tables add rows for GitHub Copilot CLI (`.github/instructions/`) and Claude Code project-scoped skills (`.claude/skills/`).

### Fixed

- `plan-week` / `close-week` skills (both `.github/instructions/` and `memory/workflows/` surfaces) — removed leaked references to `~/.claude/skills/{slug}/SKILL.md (mirror) — abridged here:`. With the new `.claude/skills/` surface now shipping in the repo, each surface is self-contained — no dangling pointer needed, and the procedure flows directly from the trigger sentence.

### Notes

- Reference: [PR #3](https://github.com/ozgurkarahan/ai-agent-memory/pull/3).

## [2026.05.0] — 2026-05-13

First versioned release. Brings the new and updated agent skills from the maintainer's private memory wiki back to this public teaching repo, scrubbed of real client / colleague / personal references.

### Added

- **9 agent-agnostic skills**, each shipped in two parallel locations to satisfy both conventions used in this repo:
  - `.github/instructions/{slug}.instructions.md` — for GitHub Copilot CLI (`applyTo: "**"` frontmatter)
  - `memory/workflows/{slug}.md` — canonical plain-markdown procedure (the existing repo convention)

  New skills:
  - `close-week` / `plan-week` — Weekly operating rhythm using `ops/weekly/{ISO}.md` files + `ops/activity.jsonl` event stream
  - `project-status` — 30-second briefing on any child project (tech stack, history, deployment, current state)
  - `review-sessions` — Session-data analysis for workflow efficiency, prompt quality, error patterns. Agent-agnostic: supports **GitHub Copilot CLI** (`~/.copilot/session-state/{id}/events.jsonl`) and **Claude Code** (`~/.claude/projects/{hash}/{id}.jsonl`) via `--agent {copilot,claude,all}`
  - `new-engagement` — Scaffold one or more client engagement projects from `~/projects/project-template/`
  - `lint` — Wiki health check trigger
- **Schema updates** in `memory/schema.md`:
  - 11 new category rows to the taxonomy table: Clients, Skills, Agents, Tools, Meetings, Career, Microsoft, Personal, Queries, Ops, Agent Config
  - **Client-folder rule** for `wiki/projects/` with a slug-strip decision table (when to flatten `client-foo` slugs vs. keep them under `client/foo/` sub-folders)
  - **Source classification frontmatter fields**: `source_type`, `sensitivity`, `system_of_record`, `retention`, `sharing`

### Changed

- `ingest` skill — major refresh: adds Phase 0 (inventory), Phase 2b.5 (consolidation matrix for mass ingest), Phase 6 (7-item self-audit gate), Phase 8 (emit activity event for cross-skill operational tracking)
- `end-session` skill — aligned with the post-`.ai/` world: project knowledge now lives directly on the wiki page rather than in per-project `.ai/` folders
- `query` skill — tightened workflow

### Removed

- `launch-copilot` / `launch-claude` skills — public consumers shouldn't have to download and run wrapper scripts from an internet repo, and the wrappers added no value over the equivalent native CLI invocation (`cd <project>` + `copilot --allow-all-tools` / `claude --dangerously-skip-permissions`). The `new-engagement` skill was updated to use native commands in its examples.
- `sync` skill — targeted a `.ai/` folder convention that was retired in April 2026 (project knowledge now lives directly on the wiki page, see `end-session`); the reference script was not shipped publicly and contained internal client-specific hardcoded mappings. If a generic drift-detection workflow is wanted later, it should ship as a fresh skill paired with a configurable script.

### Notes

- All examples were scrubbed via a one-shot script + manual review: client names → Acme / Contoso / Fabrikam / Northwind / Globex, colleague names → Colleague A..I, personal paths → `~/projects/...`, repo refs → `github.com/{your-username}/...`, internal back-references → `internal-*-lesson` placeholders.
- `review-sessions` defines an agent-agnostic contract but no reference parser ships in this release — implementers should match the schema documented in the skill (Copilot CLI event-stream parser + Claude Code turn parser).
- Reference: [PR #1](https://github.com/ozgurkarahan/ai-agent-memory/pull/1).

[Unreleased]: https://github.com/ozgurkarahan/ai-agent-memory/compare/v2026.05.1...HEAD
[2026.05.1]: https://github.com/ozgurkarahan/ai-agent-memory/compare/v2026.05.0...v2026.05.1
[2026.05.0]: https://github.com/ozgurkarahan/ai-agent-memory/releases/tag/v2026.05.0
