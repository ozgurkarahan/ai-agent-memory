# {Project Name}

> **Template starter** — Replace this README with the actual project description after the `new-engagement` skill (or a manual copy) has scaffolded the engagement.

## What this template provides

A minimal, agent-agnostic starting skeleton for any new project — designed to plug straight into the [ai-agent-memory](https://github.com/ozgurkarahan/ai-agent-memory) wiki pattern. Every file points one or more agents back at the same `AGENT.md` so context flows from a single source of truth.

| Path | Purpose | Read by |
|------|---------|---------|
| `AGENT.md` | **The** project context (overview, env, commands, conventions). Edit this first. | All agents (standard) |
| `CLAUDE.md` | Thin shim → "Read `AGENT.md`" | Claude Code (standalone) |
| `.claude/CLAUDE.md` | Claude Code project-scoped config + project-context block | Claude Code (in-repo) |
| `.claude/commands/status.md` | `/status` slash-command — 30-second project briefing | Claude Code |
| `.github/copilot-instructions.md` | Copilot pointer → `AGENT.md` | GitHub Copilot |
| `.github/instructions/end-session.instructions.md` | "End session" trigger — captures lessons before context is lost | GitHub Copilot CLI |
| `.gitignore` | Sensible defaults (OS, editor, env, Python). Tracks `.claude/CLAUDE.md` and `.claude/commands/`; ignores everything else under `.claude/`. | Git |
| `LICENSE` | MIT (change as needed) | Humans |

## Using this template

### Option 1 — `new-engagement` skill (automated)

If you've adopted the `ai-agent-memory` wiki pattern and have this template cloned at `~/projects/project-template/`, just invoke the [`new-engagement`](https://github.com/ozgurkarahan/ai-agent-memory/blob/master/.github/instructions/new-engagement.instructions.md) skill — the agent copies this scaffold, pre-fills `AGENT.md`, creates format-specific folders, and initialises git.

### Option 2 — Manual copy

```bash
# 1. Pick this template up
cp -R <ai-agent-memory-clone>/project-template ~/projects/my-new-project
cd ~/projects/my-new-project
rm -rf .git

# 2. Edit AGENT.md to describe the project (overview, env, key paths, conventions)
$EDITOR AGENT.md

# 3. Init git
git init && git add -A && git commit -m "Initial scaffold"
```

## After scaffolding — first session

When an agent first opens the scaffolded project:

1. **Read all existing files** to understand current state
2. **Read `AGENT.md`** — that's the project's identity
3. **Enter plan mode** (or equivalent) and propose a detailed plan before changing anything
4. **Wait for user approval** before creating any content files

## Pairing with the wiki

This template assumes a central memory wiki lives at `~/projects/memory/` (or wherever you keep it). Project-specific lessons get graduated back to the wiki via the [`end-session`](https://github.com/ozgurkarahan/ai-agent-memory/blob/master/.github/instructions/end-session.instructions.md) skill at the end of each coding session — that's the loop that keeps the project's memory compounding instead of evaporating.

## License

MIT — see [LICENSE](LICENSE).
