# /status — Project Briefing

When the user types `/status`, produce a 30-second situational-awareness briefing on **this project** so they can get up to speed instantly.

Gather information from all the sources below in parallel, then produce a single structured briefing.

## 1. Codebase analysis

- **Tech stack**: languages, frameworks, key dependencies (check `package.json`, `requirements.txt`, `pyproject.toml`, `*.csproj`, `Cargo.toml`, `go.mod`, `pom.xml`, etc.)
- **Folder structure**: high-level tree (max 2 levels deep)
- **Entry points / key files**: config files, main modules
- **Architecture patterns**: monolith / microservices, API style (REST / GraphQL / gRPC), state management
- **Size**: approximate source files + LOC

## 2. Project history

- Read `AGENT.md` for the project overview and objectives
- `git log --oneline --since="2 weeks ago"` — recent activity
- `git log -5 --format="%h %s (%ar)"` — last 5 commits with relative dates
- `git log --oneline --all | tail -5` — earliest commits (for context)

## 3. Last modifications

- `git diff --stat HEAD~3` (if enough commits exist) — what files changed recently
- `git status` — uncommitted work in progress
- `git branch -a` — open branches
- `git stash list` — stashed work

## 4. Deployment status

Check for deployment indicators:

- **Azure (azd)**: `azure.yaml`, `.azure/`, `infra/*.bicep`
- **GitHub Actions**: `.github/workflows/`
- **Docker**: `Dockerfile`, `docker-compose.yml`
- **Other CI/CD**: `.gitlab-ci.yml`, `Jenkinsfile`, `.circleci/`, `bitbucket-pipelines.yml`
- **Git tags**: `git tag --sort=-creatordate | head -5`

If no deployment config is found, say "No deployment configuration detected".

## 5. Current state

- Current branch and its relation to main / master
- Uncommitted changes / stashed work
- Open `TODO`, `FIXME`, `HACK` count in source files

## Output format

```
## 🔍 Project Status: {project name}

### Tech Stack
{languages, frameworks, key deps — one line each}

### Architecture
{folder overview + patterns — brief}

### History
- **Created:** {first commit date}
- **Total commits:** {count}
- **Recent activity:** {last 2 weeks summary}

### Last 5 Changes
{table: hash | message | when}

### Deployment
{deployment config + last deploy info if known}

### Current State
- **Branch:** {current branch}
- **Uncommitted work:** {yes/no + summary}
- **Open TODOs:** {count}

### Key Takeaways
{2-3 bullets — what's the most important thing to know right now}
```

Keep the briefing scannable. No fluff. The reader should know exactly where things stand in under 30 seconds.
