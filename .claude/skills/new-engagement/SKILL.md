---
name: new-engagement
description: "Scaffold client engagement projects from the installed project template: parse client, topic, format, and destination; create folders; pre-fill AGENT.md; create a wiki page; initialize git. Trigger: 'new engagement', 'scaffold engagement', '/new-engagement'."
---

# New Engagement

When the user says **"new engagement"**, **"scaffold engagement"**, or invokes a slash command like `/new-engagement`, scaffold one or more client engagement projects from the resolved project template.

## Resolve required roots

Before scaffolding:

1. Resolve `WIKI_ROOT` using `memory/schema.md`, then `schema.md`, then the memory-wiki path declared in `AGENT.md`.
2. Resolve `TEMPLATE_ROOT` by checking for `project-template/` beside `WIKI_ROOT`, then the path declared in `AGENT.md`.
3. If the template is absent but network access is available, the agent may clone `https://github.com/ozgurkarahan/ai-agent-memory.git` into a temporary folder and use its `project-template/` directory.
4. If either root remains unresolved, report the missing root and stop. Do not guess a personal path.
5. Remove any temporary clone after scaffolding.

All wiki paths below are relative to `WIKI_ROOT`.

## Step 1: Parse the request

Extract from the user input:
- **Client name** (e.g., "Acme", "Contoso", "Contoso")
- **Topics** — one or more engagement topics, each with a format
- **Projects root** — use an explicit destination from the request or `AGENT.md`; otherwise ask where to create the client workspace

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
PROJECT_DIR={PROJECTS_ROOT}/{ClientName}/10-projects/{project-slug}
mkdir -p "$PROJECT_DIR"
```

Convert the topic to a kebab-case slug (e.g., "Agent Framework Engagement" → `agent-framework-engagement`).

The standard client workspace layout is `00-client/` (intel), `10-projects/` (delivery repos), `10-projects/_archive/`, `20-assets/` (raw client material), `90-scratch/`. Engagements always go under `10-projects/`.

### 2b. Copy template files

Copy the **canonical files** from `TEMPLATE_ROOT`. The full canonical scaffold is:

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
# Copy with the platform's native filesystem tools, then strip template history
cp -R "$TEMPLATE_ROOT/." "$PROJECT_DIR/"
rm -rf "$PROJECT_DIR/.git"
```

Use the platform-native equivalent on Windows. After copying, verify the scaffold matches the canonical structure above; do not copy unrelated files that may have accumulated beside the template.

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

## Memory Wiki

Root: `{resolved WIKI_ROOT}`

## Reference Documents

| Document | Contents |
|----------|----------|
| `{resolved WIKI_ROOT}/wiki/projects/{project-slug}.md` | Canonical project memory page |

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

Project-specific context lives in two places:

1. **`AGENT.md`** in the project repo — identity, workflow, conventions (single source of truth)
2. **`wiki/projects/{project-slug}.md`** under `WIKI_ROOT` — durable project memory (lessons, reference, technical details, related links).

Save the user's engagement request verbatim to `raw/data/new-engagement-{project-slug}-{YYYY-MM-DD}.md`. If a project memory page does not yet exist, create it with this minimal skeleton:

```markdown
---
title: {Topic Title}
category: projects
tags: [{client-tag}, {topic-tags}]
source_docs: ["raw/data/new-engagement-{project-slug}-{YYYY-MM-DD}.md"]
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
- `raw/data/new-engagement-{project-slug}-{YYYY-MM-DD}.md`
```

Add the page entry to `wiki/projects/_index.md` when that index exists, update the Projects section and article count in `index.md`, and append to `log.md`.

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

For each project, suggest both agent options. Use whichever CLI the user has installed; the commands are equivalent in scope (allow-all-tools / bypass-permissions). `cd` first so the agent picks up the project's `AGENT.md`.

**PowerShell (Windows):**
```powershell
cd {actual-project-path}

# GitHub Copilot CLI
copilot --allow-all-tools

# Claude Code (alternative)
claude --dangerously-skip-permissions
```

**Bash (Linux / macOS / Git Bash):**
```bash
cd {actual-project-path}

# GitHub Copilot CLI
copilot --allow-all-tools

# Claude Code (alternative)
claude --dangerously-skip-permissions
```

### Suggested initial prompts

For each project, suggest a specific first prompt based on the topic and format. Pipe it to the agent with `-p`:
```powershell
cd {actual-project-path}
copilot --allow-all-tools -p "Research the latest agentic AI capabilities, then propose a presentation outline with demo scenarios for technical leadership"
```

### Summary table

| Project | Path | Format | Status |
|---------|------|--------|--------|
| {topic} | `{actual-project-path}` | {format} | Scaffolded |
