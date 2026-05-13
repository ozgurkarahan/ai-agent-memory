---
applyTo: "**"
---

# Launch Claude

When the user says **"launch claude"**, **"open claude in {project}"**, or runs the script directly, open a fresh Claude Code session in the specified project directory.

> Claude Code is treated as the alternative in these examples; GitHub Copilot CLI is the default — see `launch-copilot.instructions.md`.

## Wrapper scripts (two variants — PowerShell is preferred on Windows)

**PowerShell (preferred on Windows):**
```powershell
~/projects/memory/scripts/launch-claude.ps1 <project-path> ["initial prompt"]
```

**Bash (Git Bash / Linux / macOS):**
```bash
bash ~/projects/memory/scripts/launch-claude.sh <project-path> ["initial prompt"]
```

Both variants:
1. Resolve a relative `<project-path>` against `~/projects/` (PS1 also expands `~`)
2. Validate the directory exists and contains an `AGENT.md`
3. Run `claude --dangerously-skip-permissions` in that directory
4. Optionally pass an initial prompt via `-p`
5. Refuse to launch in `~/projects/memory/` itself

> **Why two variants:** see `launch-copilot.instructions.md`.

## When to use

- The user explicitly asks for Claude Code (subagents, persistent memory, plan mode toggle)
- A task requires Claude-specific features (e.g., `/clear`, custom slash commands defined in `.claude/commands/`)
- The user wants to compare Claude vs Copilot output for the same prompt

## When NOT to use

- Default day-to-day work — use `launch-copilot.sh` instead
- Inside `~/projects/memory/` itself — that's the orchestrator hub, not a child project. Stay in the current session.

## Examples

**PowerShell (Windows, primary):**
```powershell
# Open Claude in a child project
~/projects/memory/scripts/launch-claude.ps1 ~\projects\Acme\10-projects\agent-framework-engagement

# Relative path (resolves under ~/projects/)
~/projects/memory/scripts/launch-claude.ps1 Contoso\10-projects\agentic-platform-workshop

# With an initial prompt
~/projects/memory/scripts/launch-claude.ps1 ~\projects\Contoso\10-projects\agentic-platform-workshop "Review prep docs and propose the agenda"
```

**Bash (Git Bash / Linux / macOS):**
```bash
# Open Claude in a child project
bash ~/projects/memory/scripts/launch-claude.sh ~/projects/Acme/10-projects/agent-framework-engagement

# Relative path (resolves under ~/projects/)
bash ~/projects/memory/scripts/launch-claude.sh Contoso/10-projects/agentic-platform-workshop

# With an initial prompt
bash ~/projects/memory/scripts/launch-claude.sh ~/projects/Contoso/10-projects/agentic-platform-workshop "Review prep docs and propose the agenda"
```

**Bypass — just run claude directly:**
```powershell
cd '~/projects/Acme/10-projects/agent-framework-engagement'; claude --dangerously-skip-permissions
```

## Permission scope

`--dangerously-skip-permissions` applies to the **child project's** session — not to memory. Memory itself is never opened with that flag from this wrapper. Document any change to this contract in `wiki/lessons/internal-migration-lesson.md`.
