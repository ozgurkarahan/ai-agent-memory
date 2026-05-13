---
applyTo: "**"
---

# Launch Copilot

When the user says **"launch copilot"**, **"open copilot in {project}"**, or runs the script directly, open a fresh GitHub Copilot CLI session in the specified project directory.

> Copilot CLI is the default agent in these examples. For Claude Code as the alternative, see `launch-claude.instructions.md`.

## Wrapper scripts (two variants — PowerShell is preferred on Windows)

**PowerShell (preferred on Windows):**
```powershell
~/projects/memory/scripts/launch-copilot.ps1 <project-path> ["initial prompt"]
```

**Bash (Git Bash / Linux / macOS):**
```bash
bash ~/projects/memory/scripts/launch-copilot.sh <project-path> ["initial prompt"]
```

Both variants:
1. Resolve a relative `<project-path>` against `~/projects/` (PS1 also expands `~`)
2. Validate the directory exists and contains an `AGENT.md`
3. Run `copilot --allow-all-tools` in that directory
4. Optionally pass an initial prompt via `-p`
5. Refuse to launch in `~/projects/memory/` itself

> **Why two variants:** the original `launch-project.sh` was Linux-first. On Windows from PowerShell, `~` doesn't expand and the system `bash` may resolve to a broken WSL install. The PS1 wrapper is the right answer on Windows. The SH wrapper is kept for Git Bash users + portability + parity. Added 2026-05-11 — see `wiki/lessons/internal-migration-lesson.md` "Lesson 4".

## When to use

- Default for day-to-day work
- Project tasks that match Copilot CLI strengths: web fetch, GitHub-MCP, Microsoft Playwright MCP, M365-query-tool, MS Foundry skill, etc.
- Tasks where you want allow-all-tools execution without per-call confirmation

## When NOT to use

- Inside `~/projects/memory/` itself — that's the orchestrator hub, not a child project. Stay in the current session.
- When you specifically need Claude-only features (subagents, plan-mode toggle) — use `launch-claude.sh` instead.

## Examples

**PowerShell (Windows, primary):**
```powershell
# Open Copilot in a child project
~/projects/memory/scripts/launch-copilot.ps1 ~\projects\Acme\10-projects\agent-framework-engagement

# Relative path (resolves under ~/projects/)
~/projects/memory/scripts/launch-copilot.ps1 Contoso\10-projects\agentic-platform-workshop

# With an initial prompt
~/projects/memory/scripts/launch-copilot.ps1 ~\projects\Contoso\10-projects\agentic-platform-workshop "Review prep docs and propose the agenda"
```

**Bash (Git Bash / Linux / macOS):**
```bash
# Open Copilot in a child project
bash ~/projects/memory/scripts/launch-copilot.sh ~/projects/Acme/10-projects/agent-framework-engagement

# Relative path (resolves under ~/projects/)
bash ~/projects/memory/scripts/launch-copilot.sh Contoso/10-projects/agentic-platform-workshop

# With an initial prompt
bash ~/projects/memory/scripts/launch-copilot.sh ~/projects/Contoso/10-projects/agentic-platform-workshop "Review prep docs and propose the agenda"
```

**Bypass — just run copilot directly:**
```powershell
# When the launchers are unavailable or you want to pass extra flags
cd '~/projects/Acme/10-projects/agent-framework-engagement'; copilot --allow-all-tools
```

## Permission scope

`--allow-all-tools` allows the agent to run tools without per-call confirmation, but does NOT widen file-path or URL access (those use separate flags: `--allow-all-paths`, `--allow-all-urls`, or the umbrella `--allow-all` / `--yolo`). The wrapper deliberately picks `--allow-all-tools` only — same scope as Claude's `--dangerously-skip-permissions` — so the launcher behaviour is symmetric across both agents.

If the user ever needs broader scope (e.g., reading outside `~/projects/`), pass extra flags directly to `copilot` rather than widening this script. Document any contract change in `wiki/lessons/internal-migration-lesson.md`.
