# Contributing

Thanks for your interest in contributing to **ai-agent-memory**! This repo is a teaching reference for the [Karpathy LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) pattern applied to coding-agent memory. Contributions that improve the skills, schema, or worked examples are very welcome.

## Adding or changing a skill

Skills live in **three parallel locations** that must stay in sync — one per supported agent surface, plus a plain-Markdown reference:

| Path | Surface | Frontmatter |
|---|---|---|
| `.github/instructions/{slug}.instructions.md` | GitHub Copilot CLI auto-discovery | `applyTo: "**"` |
| `.claude/skills/{slug}/SKILL.md` | Claude Code project-scoped skill auto-discovery | `name: {slug}` + `description: ...` |
| `memory/workflows/{slug}.md` | Agent-agnostic plain-Markdown reference (canonical source for documentation; also loaded via the maintainer's `AGENT.md` pointer pattern) | `applyTo: "**"` (current convention) |

When you change one, update the other two in the same commit. The bodies should be identical across the three surfaces — only the per-surface frontmatter block differs.

**Why three surfaces?** Each agent has its own skill-discovery mechanism:

- GitHub Copilot CLI loads any file matching `.github/instructions/*.instructions.md` whose `applyTo` glob matches the current workspace
- Claude Code loads any `SKILL.md` under `.claude/skills/{slug}/` and routes invocations based on the `description:` field, so write the description carefully — it's what the agent's skill router sees
- The plain-Markdown copy under `memory/workflows/` is the human-readable canonical source for documentation, and is what skills like `ingest` reference internally when discussing other skills

A skill that ships in only one of the three locations is invisible to two of the three agent ecosystems this repo targets.

### Skill style

- **Trigger up front.** First line of the body says when the skill activates: *"When the user says 'X', 'Y', or invokes /X, do…"*
- **Numbered procedure**, not prose. Skills are runbooks, not essays.
- **Generic.** No real client names, no colleagues, no file paths from your personal machine, no internal-only references. Use Microsoft-style fictional placeholders: Acme, Contoso, Fabrikam, Northwind, Globex for clients; Colleague A..I for people; `~/projects/...` for paths; `github.com/{your-username}/...` for repo refs.
- **Agent-neutral** where possible. If a skill is specific to one agent's session format or capability, document the equivalent for the other supported agents (see `review-sessions` for a worked example covering both GitHub Copilot CLI and Claude Code).
- **No runnable scripts.** Skills that simply wrap a script the consumer hasn't seen are misleading documentation. If your skill needs a script, ship the script in the same PR and treat its publication as a separate concern (license, scrub, README, etc.). If the same outcome can be expressed as a 2-line native CLI invocation, prefer that.

## Adding a changelog entry

Every user-visible change requires an entry in `CHANGELOG.md` under `## [Unreleased]`. Use the [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) sections:

- **Added** — new skills, new schema rows, new templates, new workflows
- **Changed** — material behaviour changes to an existing skill or schema rule
- **Deprecated** — skills / conventions still present but discouraged
- **Removed** — skills / conventions no longer in the repo
- **Fixed** — corrections to wrong / misleading documentation
- **Security** — anything related to credential leakage, scrubbing, threat surface

Reference issues / PRs by number where helpful: `Added X (#42)`.

Trivial changes (typos, link fixes, internal refactors that don't affect users) don't need a changelog entry.

## Releases

Versioning follows [CalVer](https://calver.org/): `YYYY.0M.MICRO` — for example `2026.05.0`, `2026.05.1`, `2026.06.0`.

Releases ship when meaningful skill / schema changes accumulate, typically once per month.

### Cutting a release (maintainer process)

1. Roll the `[Unreleased]` section into a new `[YYYY.0M.MICRO]` section dated to the release day
2. Update the comparison links at the bottom of `CHANGELOG.md`
3. Open a PR titled `Release vYYYY.0M.MICRO`, merge once green
4. Tag the resulting merge commit on `master`:
   ```bash
   git tag -a vYYYY.0M.MICRO -m "Release YYYY.0M.MICRO"
   git push origin vYYYY.0M.MICRO
   ```
5. Create a GitHub Release pointing at the tag, with the body copied from the new `CHANGELOG.md` section. Quickest path:
   ```bash
   gh release create vYYYY.0M.MICRO --title "vYYYY.0M.MICRO" --notes-from-tag
   ```
   …or use `--notes-file` with a file containing the section body.

### Version-component bumping rules

- **`YYYY`** — the year of the release (4 digits).
- **`0M`** — the month, zero-padded (`01`..`12`).
- **`MICRO`** — incremented within the same month if a follow-up release is needed; otherwise stays at `0`. Reset to `0` when the month rolls over.

## Pull requests

- Branch from `master`. Branch name: short and descriptive (e.g. `add-skills-2026-05`, `fix-ingest-phase-6`).
- One logical change per PR. If your PR ends up doing two things, split it.
- Include a `Co-authored-by:` trailer if you used a coding agent to draft the change. Example:
  ```
  Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>
  ```

## Scope

**In scope:** skills, schema, workflows, templates, agent-config, README, CHANGELOG, demo content, security / scrubbing guidance.

**Out of scope without prior discussion:** large rewrites of the README narrative, switching the wiki tool from plain Markdown to another format, adding heavy CI / automation, vendor-specific integrations beyond agent-neutral skills.

Open an issue first if you're unsure whether a change is in scope.
