---
name: project-status
description: "Produce a 30-second situational-awareness briefing for any child project: tech stack, folder structure, git history, recent changes, deployment status, current state, link to wiki project page. Trigger: 'project status', 'status briefing', '/project-status'."
---

# Project Status

When the user says **"project status"**, **"status briefing"**, or invokes `/project-status` from inside any project directory (NOT memory itself), produce a complete situational-awareness briefing so the user can get up to speed on that project in 30 seconds.

> This skill is for any child project. When invoked from the memory system itself, refuse and direct the user to the wiki because the wiki is its status.
>
> **Coexists with the per-project `/status` command** that ships in every scaffolded project under `.claude/commands/status.md`. The per-project version is Claude-Code-specific. THIS memory skill is the agent-agnostic version (works under GitHub Copilot CLI, Claude Code, or any tool that loads `.github/instructions/`). When both are available, prefer the per-project one if you are inside Claude Code (richer integration), otherwise use this skill.

## Instructions

Gather information from ALL the sources below, then produce a single structured briefing. Use parallel tool calls to speed up the research.

### Resolve the memory root

1. If the current project contains `schema.md` or `memory/schema.md`, it is the memory system or its installer; refuse as described above.
2. Otherwise follow the memory-wiki path declared in the child project's `AGENT.md`.
3. If no memory root resolves, continue the codebase briefing but mark the wiki page as unavailable instead of guessing a personal path.

### 1. Codebase analysis

- **Tech stack**: languages, frameworks, key dependencies (check `package.json`, `requirements.txt`, `pyproject.toml`, `*.csproj`, `Cargo.toml`, `go.mod`, `pom.xml`, etc.)
- **Folder structure**: high-level tree (max 2 levels deep), explain what each top-level folder contains
- **Key files**: entry points, config files, main modules
- **Architecture patterns**: monolith/microservices, API style (REST/GraphQL/gRPC), state management, key abstractions
- **Size**: approximate number of source files and lines of code

### 2. Project history — what we've done

- Read `AGENT.md` for project overview and objectives
- Read the project's page at `{WIKI_ROOT}/wiki/projects/{project-slug}.md` for lessons and reference, if it exists
- Summarise git log: total commits, contributors, major milestones
- Run: `git log --oneline --since="2 weeks ago"` for recent activity
- Run: `git log --oneline --all | tail -5` for the earliest commits

### 3. Last modifications

- Run: `git log -5 --format="%h %s (%ar)"` for the last 5 commits with relative dates
- Run: `git diff --stat HEAD~3` to show what files changed recently (if enough commits exist)
- Check `git status` for any uncommitted work in progress
- Check for any open branches: `git branch -a`

### 4. Deployment status

Check for deployment indicators and report what you find:

- **Azure (azd)**: check for `azure.yaml`, `.azure/` folder, `infra/` folder with Bicep files
- **GitHub Actions**: check `.github/workflows/` for CI/CD pipelines
- **Docker**: check for `Dockerfile`, `docker-compose.yml`
- **Other CI/CD**: check for `.gitlab-ci.yml`, `Jenkinsfile`, `.circleci/`, `bitbucket-pipelines.yml`
- **Git tags**: run `git tag --sort=-creatordate | head -5` for release/deploy tags
- **Last deploy**: if azd is used, check `.azure/` for environment state. If GitHub Actions, note the workflow files and what they do.
- If NO deployment config is found, say "No deployment configuration detected"

### 5. Current state

- Current branch and how it relates to main/master
- Any uncommitted changes or stashed work (`git stash list`)
- Open TODO items in code: search for `TODO`, `FIXME`, `HACK` in source files (report count, not each one)

## Output format

Produce a briefing in this exact format:

```
## 🔍 Project Status: {project name}

### Tech Stack
{languages, frameworks, key deps — one line each}

### Architecture
{folder structure overview + patterns — keep it brief}

### History
- **Created:** {first commit date}
- **Total commits:** {count}
- **Recent activity:** {last 2 weeks summary}

### Last 5 Changes
{table: hash | message | when}

### Deployment
{deployment status, last deploy if known, CI/CD setup}

### Current State
- **Branch:** {current branch}
- **Uncommitted work:** {yes/no + summary}
- **Open TODOs:** {count}

### Wiki page
- Link to `{WIKI_ROOT}/wiki/projects/{slug}.md` (or note that it does not exist yet)

### Key Takeaways
{2-3 bullet points: what's the most important thing to know right now}
```

Keep the entire briefing concise and scannable. No fluff. The user wants to read this in 30 seconds and know exactly where things stand.
