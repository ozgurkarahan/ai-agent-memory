---
applyTo: "**"
---

# New Engagement

When the user says **"new engagement"**, **"scaffold engagement"**, or invokes a slash command like `/new-engagement`, scaffold one or more new client engagement projects from `~/projects/project-template/`.

> **Canonical structure source of truth:** `wiki/projects/project-template.md`.
> The physical `~/projects/project-template/` repo may contain extra files (`.ai/`, `.claude/`, `README.md`, `.github/instructions/`) that are template-internal cruft and **must not** be copied into scaffolded projects.

## Step 1: Parse the request

Extract from the user input:
- **Client name** (e.g., "Acme", "Contoso", "Contoso")
- **Topics** — one or more engagement topics, each with a format

Expected input format: `<ClientName> — <topic1> (format), <topic2> (format)`

Formats: `presentation`, `workshop`, `demo`, `presentation + demo`, or combinations.

If the input is ambiguous or missing details, ask clarifying questions:
- What is the target audience? (e.g., technical leadership, developers, executives)
- What format? (presentation, workshop, demo, or combination)
- What are the key objectives?
- Any specific technologies or topics to cover?

## Step 2: Scaffold each project

For each topic, do the following.

### 2a. Create project directory

```bash
PROJECT_DIR=~/projects/{ClientName}/10-projects/{project-slug}
mkdir -p "$PROJECT_DIR"
```

Convert the topic to a kebab-case slug (e.g., "Agent Framework Engagement" → `agent-framework-engagement`).

The standard client workspace layout is `00-client/` (intel), `10-projects/` (delivery repos), `10-projects/_archive/`, `20-assets/` (raw client material), `90-scratch/`. Engagements always go under `10-projects/`.

### 2b. Copy template files

Copy the **canonical files** from `~/projects/project-template/` per the post-2026-05-11 canonical contract documented in [[project-template]] page. The full canonical scaffold is:

```
{project}/
├── AGENT.md                                          # MAIN — overview, env, commands, workflow, refs
├── CLAUDE.md                                         # Thin shim → "Read AGENT.md"
├── .claude/
│   ├── CLAUDE.md                                     # Claude Code project config + Project Context block
│   └── commands/status.md                            # /status slash-command for 30-sec briefing
├── .github/
│   ├── copilot-instructions.md                       # GitHub Copilot CLI instructions
│   └── instructions/
│       └── end-session.instructions.md               # end-session shim (5 steps)
├── .gitignore                                        # tracks .claude/CLAUDE.md, .vscode/; ignores runtime caches
├── LICENSE                                           # MIT
├── README.md                                         # Human-facing
└── (format-specific folders)                         # slides/, demos/, exercises/, etc.
```

```bash
# Easiest: clone the GitHub template repo, then strip .git
git clone --depth 1 https://github.com/{your-username}/project-template "$PROJECT_DIR"
rm -rf "$PROJECT_DIR/.git"

# OR (offline/local) copy from the local clone:
cp -R ~/projects/project-template/. "$PROJECT_DIR/"
rm -rf "$PROJECT_DIR/.git"
```

After copying, verify the scaffold matches the canonical structure above. If `~/projects/project-template/` accumulates extra files not in the canonical list, **the wiki page wins** — clean the physical template, do not loosen the contract. See the 2026-05-11 lesson on [[project-template]] page.

### 2c. Create format-specific folders

| Format | Folders to create |
|--------|-------------------|
| Presentation | `slides/`, `demos/`, `docs/` |
| Workshop | `slides/`, `exercises/`, `solutions/`, `instructor/`, `docs/` |
| Demo | `demos/`, `docs/` |
| Presentation + Demo | `slides/`, `demos/`, `docs/` |
| Mixed/Other | Combine as appropriate |

Create the folders with a `.gitkeep` in each:
```bash
mkdir -p "$PROJECT_DIR/{folder}" && touch "$PROJECT_DIR/{folder}/.gitkeep"
```

### 2d. Pre-fill AGENT.md

Replace the templated `AGENT.md` with engagement-specific content:

```markdown
# {Topic Title}

## Overview

{Client} engagement: {topic description}. Format: {format}. Target audience: {audience}.

## Engagement Details

| Field | Value |
|-------|-------|
| Client | {ClientName} |
| Topic | {Topic} |
| Format | {format} |
| Audience | {audience} |
| Status | Not started |

## Deliverables

{Based on format — see deliverables table below}

## Key Paths

| Path | Description |
|------|-------------|
{format-specific paths}

## Reference Documents

| Document | Contents |
|----------|----------|
| `~/projects/memory/wiki/projects/{client-folder}/{project-slug}.md` (clients: `acme`, `fabrikam`, `contoso`, `northwind`) or `~/projects/memory/wiki/projects/{project-slug}.md` (non-client) | Canonical project memory page |
| `~/projects/memory/wiki/clients/{client-slug}.md` | Client hub |

## First Session Instructions

When the agent is first launched in this project, follow these steps:

1. **Read all existing files** in the project to understand current state
2. **Research the topic** — find the latest capabilities, announcements, and best practices for {topic}
3. **Enter plan mode** and propose a detailed engagement plan including:
   - Agenda / slide outline with timing
   - Key talking points and messaging
   - Demo scenarios (if applicable)
   - Exercise descriptions (if workshop)
   - Competitive positioning where relevant
4. **Wait for user approval** before creating any content files
5. **After approval**, scaffold the content structure and begin development
```

### Deliverables by format

| Format | Deliverables |
|--------|-------------|
| Presentation | - [ ] Slide outline with talking points<br>- [ ] Speaker notes<br>- [ ] Demo script (if applicable)<br>- [ ] Leave-behind document<br>- [ ] Q&A preparation |
| Workshop | - [ ] Lab guide with prerequisites<br>- [ ] Exercise instructions (progressive difficulty)<br>- [ ] Solution files<br>- [ ] Instructor notes with timing<br>- [ ] Cheat sheet / quick reference<br>- [ ] Prerequisites checklist |
| Demo | - [ ] Demo script with steps<br>- [ ] Setup instructions<br>- [ ] Fallback plan<br>- [ ] Talking points |

### 2e. Create the project memory page

The canonical structure (per `wiki/projects/project-template.md`) does NOT include a `.claude/CLAUDE.md` per project. Project-specific context lives in two places:

1. **`AGENT.md`** in the project repo — identity, workflow, conventions (single source of truth)
2. **`~/projects/memory/wiki/projects/{client-folder}/{project-slug}.md`** — durable project memory (lessons, reference, technical details, related links). For known top-level clients (`acme`, `fabrikam`, `contoso`, `northwind`), file under the client folder. For non-client / personal / generic projects, file flat at `wiki/projects/{project-slug}.md`. See [[schema]] "Client-folder rule" for the slug-strip vs keep-prefix decision and [[internal-reorg-lesson]] for context.

If a project memory page does not yet exist for this engagement, create one using the minimal skeleton from `wiki/projects/project-template.md`:

```markdown
---
title: {Topic Title}
category: projects
tags: [{client-tag}, {topic-tags}]
date_created: {YYYY-MM-DD}
date_updated: {YYYY-MM-DD}
---
# {Topic Title}

## Summary
## Context
## Project notes
## Open actions
## Related
## Sources
```

Add the page entry to `wiki/projects/_index.md`, the root `index.md`, and append to `log.md`.

### 2f. Git init

```bash
cd "$PROJECT_DIR" && git init
git add -A
git commit -m "Initial scaffold: {topic} engagement for {Client}

Scaffolded from project-template by the new-engagement skill.

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

## Step 3: Output results

After scaffolding all projects, output:

### Launch commands

For each project, suggest BOTH agent options AND the platform-appropriate variant. Prefer PS1 on Windows (primary), SH on Git Bash / Linux / macOS:

**PowerShell (default on Windows):**
```powershell
# GitHub Copilot CLI (default agent today)
~/projects/memory/scripts/launch-copilot.ps1 ~\projects\{ClientName}\10-projects\{project-slug}

# Claude Code (alternative)
~/projects/memory/scripts/launch-claude.ps1 ~\projects\{ClientName}\10-projects\{project-slug}
```

**Bash:**
```bash
# GitHub Copilot CLI (default)
bash ~/projects/memory/scripts/launch-copilot.sh ~/projects/{ClientName}/10-projects/{project-slug}

# Claude Code (alternative)
bash ~/projects/memory/scripts/launch-claude.sh ~/projects/{ClientName}/10-projects/{project-slug}
```

### Suggested initial prompts

For each project, suggest a specific first prompt based on the topic and format. Example (PowerShell):
```powershell
~/projects/memory/scripts/launch-copilot.ps1 ~\projects\Acme\10-projects\agent-framework-engagement "Research the latest agentic AI capabilities, then propose a presentation outline with demo scenarios for technical leadership"
```

### Summary table

| Project | Path | Format | Status |
|---------|------|--------|--------|
| {topic} | `~/projects/{Client}/10-projects/{slug}/` | {format} | Scaffolded |
