#!/usr/bin/env python3
"""Regenerate bootstrap.md from the canonical skill bodies + project-template files.

Bootstrap.md is the paste-and-go onboarding prompt for AI coding agents.
It must be fully self-contained (no network access required).

This script keeps it in sync with the repo by:
  - Inlining each skill BODY once from memory/workflows/{slug}.md
  - Emitting 3 frontmatter wrappers per skill (tri-surface convention)
  - Inlining the full project-template/ scaffold

Run after any skill or project-template change:
    python scripts/regenerate-bootstrap.py
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Order matters: ingest+end-session+query first (core), then advanced workflows.
SKILLS = [
    "ingest",
    "end-session",
    "query",
    "lint",
    "plan-week",
    "close-week",
    "project-status",
    "review-sessions",
    "new-engagement",
]

# Project-template files, in creation order (parents first).
TEMPLATE_FILES = [
    "LICENSE",
    "README.md",
    ".gitignore",
    "AGENT.md",
    "CLAUDE.md",
    ".github/copilot-instructions.md",
    ".github/instructions/end-session.instructions.md",
    ".claude/CLAUDE.md",
    ".claude/commands/status.md",
]

FRONTMATTER_RE = re.compile(r"^---\n.*?\n---\n", re.DOTALL)
FORBIDDEN_CONSUMER_REFERENCES = {
    "unshipped helper script": re.compile(r"(?<![\w.-])scripts[\\/][\w./\\-]+\.py\b", re.IGNORECASE),
    "maintainer-specific memory path": re.compile(r"~[\\/]projects[\\/]memory\b", re.IGNORECASE),
    "maintainer-specific template path": re.compile(r"~[\\/]projects[\\/]project-template\b", re.IGNORECASE),
    "hardcoded Windows user path": re.compile(r"\b[A-Za-z]:\\Users\\[^\\\s]+\\", re.IGNORECASE),
}


def read_body(path: Path) -> str:
    """Read a markdown file and strip the leading YAML frontmatter block."""
    text = path.read_text(encoding="utf-8")
    return FRONTMATTER_RE.sub("", text, count=1).lstrip()


def read_body_exact(path: Path) -> str:
    """Strip frontmatter while preserving all body whitespace for parity checks."""
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    return FRONTMATTER_RE.sub("", text, count=1)


def read_claude_description(slug: str) -> str:
    """Extract the description: field from .claude/skills/{slug}/SKILL.md."""
    skill_file = ROOT / ".claude" / "skills" / slug / "SKILL.md"
    text = skill_file.read_text(encoding="utf-8")
    match = re.search(r'^description:\s*(.+)$', text, re.MULTILINE)
    if not match:
        raise ValueError(f"No description: field found in {skill_file}")
    return match.group(1).strip()


def read_file(rel: str) -> str:
    """Read a project-template file."""
    return (ROOT / "project-template" / rel).read_text(encoding="utf-8")


def validate_consumer_text(text: str, origin: str) -> list[str]:
    """Return consumer-facing dependency violations found in text."""
    errors = []
    for label, pattern in FORBIDDEN_CONSUMER_REFERENCES.items():
        matches = sorted(set(match.group(0) for match in pattern.finditer(text)))
        if matches:
            errors.append(f"{origin}: {label}: {', '.join(matches)}")
    return errors


def validate_sources() -> None:
    """Fail closed when source surfaces drift or require unshipped local files."""
    errors = []
    for slug in SKILLS:
        paths = {
            "workflow": ROOT / "memory" / "workflows" / f"{slug}.md",
            "Copilot": ROOT / ".github" / "instructions" / f"{slug}.instructions.md",
            "Claude": ROOT / ".claude" / "skills" / slug / "SKILL.md",
        }
        bodies = {surface: read_body_exact(path) for surface, path in paths.items()}
        canonical = bodies["workflow"]
        for surface, body in bodies.items():
            if body != canonical:
                errors.append(f"{slug}: {surface} body differs from memory/workflows/{slug}.md")
        errors.extend(validate_consumer_text(canonical, f"skill {slug}"))

    for rel in TEMPLATE_FILES:
        errors.extend(validate_consumer_text(read_file(rel), f"project-template/{rel}"))

    if errors:
        details = "\n- ".join(errors)
        raise ValueError(f"Bootstrap source validation failed:\n- {details}")


def fence(content: str, lang: str = "markdown") -> str:
    """Wrap content in a triple-backtick fence. Uses ~~~ if content has ```."""
    if "```" in content:
        return f"~~~{lang}\n{content.rstrip()}\n~~~"
    return f"```{lang}\n{content.rstrip()}\n```"


# ---------------------------------------------------------------------------
# Static sections (preserved from prior bootstrap.md drafting).
# These describe the BOOTSTRAPPED project's wiki structure — not this repo's.
# ---------------------------------------------------------------------------

HEADER = """# AI Agent Memory — Bootstrap Prompt

> **Give this file to your AI coding agent** (GitHub Copilot, Claude Code, Codex, Cursor, Windsurf, etc.) in a new project folder.
>
> The agent will create a **persistent memory wiki** that compounds knowledge across coding sessions, plus a complete set of triggerable workflows (ingest, query, end-session, lint, plan-week, close-week, project-status, review-sessions, new-engagement) wired for **both GitHub Copilot CLI and Claude Code**.
>
> Based on the [Karpathy LLM Wiki pattern](https://x.com/karpathy/status/1882839370598990104): raw sources → compiled wiki → structured schema.

---

## Instructions

You are setting up a **persistent memory system** for an AI coding agent. Follow each step below. Create every file with the exact content provided. Do not skip steps.

This bootstrap installs **9 skills across 2 native agent surfaces**, plus an agent-neutral Markdown copy:

| Copy | Path | Read by |
|---|---|---|
| Native GitHub Copilot CLI instructions | `.github/instructions/{slug}.instructions.md` | GitHub Copilot CLI (auto-loaded via `applyTo: "**"`) |
| Native Claude Code skills | `.claude/skills/{slug}/SKILL.md` | Claude Code (auto-routed by `description:` field) |
| Agent-neutral workflows | `memory/workflows/{slug}.md` | Any agent that follows `AGENT.md`; portable reference copy |

The **body** of each skill is identical across the 3 copies. Only the YAML frontmatter differs.

## Non-negotiable execution contract

This is an **installation task**, not a document to summarize. Work directly in the current folder unless the user supplied another target.

1. Install the executable skill surfaces first. A wiki without `.github/instructions/` and `.claude/skills/` is an incomplete installation.
2. Complete each mandatory gate before continuing. Do not skip a failed gate.
3. Be resume-safe: inspect existing files first, keep files that already match, and create or repair every missing or incomplete file.
4. Do not report success until the Definition of Done in Step 12 passes.
5. If interrupted, the next run starts at the first failed gate rather than recreating the wiki from scratch.

`memory/wiki/skills/` contains knowledge *about* skills. It does **not** make skills executable. The native executable locations are `.github/instructions/` and `.claude/skills/`.

---

### Step 1: Create the directory structure

Create the following directory tree at the root of the current project (or at a path the user specifies):

```
project-root/
├── AGENT.md                                    # Main AI instructions (created in Step 10)
├── CLAUDE.md                                   # Pointer to AGENT.md (Step 10)
├── .github/
│   ├── copilot-instructions.md                 # Pointer to AGENT.md (Step 10)
│   └── instructions/                           # GitHub Copilot CLI surface (Step 2)
│       ├── ingest.instructions.md
│       ├── end-session.instructions.md
│       ├── query.instructions.md
│       ├── lint.instructions.md
│       ├── plan-week.instructions.md
│       ├── close-week.instructions.md
│       ├── project-status.instructions.md
│       ├── review-sessions.instructions.md
│       └── new-engagement.instructions.md
├── .claude/
│   └── skills/                                 # Claude Code surface (Step 2)
│       ├── ingest/SKILL.md
│       ├── end-session/SKILL.md
│       ├── query/SKILL.md
│       ├── lint/SKILL.md
│       ├── plan-week/SKILL.md
│       ├── close-week/SKILL.md
│       ├── project-status/SKILL.md
│       ├── review-sessions/SKILL.md
│       └── new-engagement/SKILL.md
├── memory/
│   ├── schema.md                               # Wiki governance (Step 3)
│   ├── index.md                                # Content catalog (Step 4)
│   ├── log.md                                  # Append-only audit log (Step 5)
│   ├── glossary.md                             # Canonical terms (Step 6)
│   ├── agent-config/
│   │   ├── workflow.md                         # Cross-project rules (Step 7)
│   │   └── platform.md                         # Platform & preferences (Step 8)
│   ├── workflows/                              # Agent-neutral skill bodies (Step 2)
│   │   ├── ingest.md
│   │   ├── end-session.md
│   │   ├── query.md
│   │   ├── lint.md
│   │   ├── plan-week.md
│   │   ├── close-week.md
│   │   ├── project-status.md
│   │   ├── review-sessions.md
│   │   └── new-engagement.md
│   ├── templates/                              # Page templates (Step 9)
│   │   ├── project.md
│   │   └── lesson.md
│   ├── wiki/                                   # The compiled knowledge graph
│   │   ├── projects/
│   │   ├── domains/
│   │   ├── patterns/
│   │   ├── lessons/
│   │   ├── skills/
│   │   ├── agents/
│   │   ├── tools/
│   │   └── _queries/
│   ├── raw/                                    # Immutable source snapshots (Karpathy Layer 1)
│   └── ops/                                    # Operational state for plan-week/close-week
│       ├── weekly/                             # ISO week files (e.g., 2026-W18.md)
│       └── activity.jsonl                      # Append-only event log
└── project-template/                           # Required offline scaffold for new engagements (Step 11)
```

Create all directories (including empty ones like `raw/`, `wiki/projects/`, `memory/ops/weekly/`).

Also create an empty `memory/ops/activity.jsonl` (touch the file so `plan-week`/`close-week` can append to it).

---
"""


def section_schema() -> str:
    return """### Step 3: Create `memory/schema.md`

```markdown
---
title: Wiki Schema
category: meta
date_created: {{today}}
date_updated: {{today}}
---

# Wiki Schema

This document governs how the wiki is structured. The LLM reads this to understand conventions, categories, and workflows.

## Category Taxonomy

| Category | Folder | Description | Example Pages |
|----------|--------|-------------|---------------|
| Projects | `wiki/projects/` | Per-project knowledge: architecture, lessons, technical reference | `my-api`, `mobile-app` |
| Domains | `wiki/domains/` | Technical domain deep-dives | `authentication`, `kubernetes`, `react` |
| Patterns | `wiki/patterns/` | Reusable architecture & design patterns | `retry-with-backoff`, `event-sourcing` |
| Lessons | `wiki/lessons/` | Consolidated debugging history & gotchas | `encoding-gotchas`, `deployment-failures` |
| Skills | `wiki/skills/` | Triggerable workflows (durable knowledge of the skill itself) | `ingest`, `query` |
| Agents | `wiki/agents/` | Role-based executors / subagents | `code-review`, `research` |
| Tools | `wiki/tools/` | Products, CLIs, SDKs, APIs, services | `gh-cli`, `playwright-mcp` |
| Queries | `wiki/_queries/` | Synthesized answers to past questions | `how-to-deploy-X` |
| Agent Config | `agent-config/` | Cross-project AI agent configuration | `workflow`, `platform` |

## Article Format

Every wiki page has YAML frontmatter + markdown body:

~~~markdown
---
title: Page Title
category: projects|domains|patterns|lessons|skills|agents|tools|queries
tags: [tag1, tag2, tag3]
source_docs: []
date_created: YYYY-MM-DD
date_updated: YYYY-MM-DD
---

# Page Title

## Summary
One-paragraph overview.

## Content
Main content with [[wikilinks]] to related pages.

## Related
- [[related-page-1]]
- [[related-page-2]]

## Sources
- Source documents, URLs, or references
~~~

## Naming Conventions

- **File names**: lowercase, hyphenated (`my-project.md`, not `My Project.md`)
- **Folders**: lowercase, hyphenated
- **Category in frontmatter**, not in path (allows migration without renaming)
- **Derive filename from content**, not from LLM-generated titles (deterministic)

## Wikilink Syntax

- `[[page-name]]` — link to another wiki page
- `[[page-name|Display Text]]` — link with custom display text
- `[[page-name#Section]]` — link to a specific section
- Pages are resolved by filename (shortest unique match)

## Index Files

- **`index.md`** (root) — master content catalog, grouped by category, with counts
- The LLM updates indexes on every ingest
```

---
"""


def section_index() -> str:
    return """### Step 4: Create `memory/index.md`

```markdown
---
title: Wiki Index
category: meta
date_created: {{today}}
date_updated: {{today}}
---

# Wiki Content Catalog

This is the master catalog of all wiki pages, grouped by category.

**Always update this file when adding or removing pages.** The LLM reads this file to find pages by topic.

## Projects (0 articles)

<!-- Per-project knowledge: architecture, lessons, technical reference -->

## Domains (0 articles)

<!-- Technical domain deep-dives -->

## Patterns (0 articles)

<!-- Reusable architecture & design patterns -->

## Lessons (0 articles)

<!-- Consolidated debugging history & gotchas -->

## Skills (0 articles)

<!-- Durable knowledge about triggerable workflows -->

## Agents (0 articles)

<!-- Role-based executors / subagents -->

## Tools (0 articles)

<!-- Products, CLIs, SDKs, APIs, services -->

## Queries (0 articles)

<!-- Synthesized answers to past questions -->

## Agent Config

- [workflow](agent-config/workflow.md) — Cross-project workflow rules
- [platform](agent-config/platform.md) — Platform & environment preferences

## Installed Workflows

- [ingest](workflows/ingest.md) — Ingest a source into the wiki
- [end-session](workflows/end-session.md) — Wrap up a coding session
- [query](workflows/query.md) — Answer a question from the wiki
- [lint](workflows/lint.md) — Run wiki health checks
- [plan-week](workflows/plan-week.md) — Draft the Monday plan
- [close-week](workflows/close-week.md) — Friday review + activity aggregation
- [project-status](workflows/project-status.md) — 30-sec project briefing
- [review-sessions](workflows/review-sessions.md) — Analyse past sessions for improvements
- [new-engagement](workflows/new-engagement.md) — Scaffold a new client engagement
```

---
"""


def section_log() -> str:
    return """### Step 5: Create `memory/log.md`

```markdown
---
title: Activity Log
category: meta
date_created: {{today}}
date_updated: {{today}}
---

# Activity Log

Append-only log of all wiki changes. Every ingest, update, or significant edit gets a line.

Format: `- **YYYY-MM-DDTHH:MM** | TYPE | "description" | metadata`

Types: `INGEST`, `UPDATE`, `QUERY`, `CLOSE-WEEK`, `LINT`

## Log

- **{{today}}T00:00** | INIT | "Memory wiki bootstrapped" | bootstrap: ai-agent-memory
```

---
"""


def section_glossary() -> str:
    return """### Step 6: Create `memory/glossary.md`

```markdown
---
title: Glossary
category: meta
date_created: {{today}}
date_updated: {{today}}
---

# Glossary

Canonical terms used across the wiki. One-line definitions. Update when ingesting new acronyms, product names, or domain-specific jargon.

## Terms

<!-- Add entries alphabetically:
- **Term** — one-line definition. See [[related-page]].
-->
```

---
"""


def section_agent_workflow() -> str:
    return """### Step 7: Create `memory/agent-config/workflow.md`

```markdown
---
title: Cross-Project Workflow Rules
category: agent-config
date_created: {{today}}
date_updated: {{today}}
---

# Cross-Project Workflow Rules

These rules apply to all projects and all AI coding assistant sessions.

> Each project has an `AGENT.md` in its root with project-specific instructions.
> Lessons learned and technical reference live in the central memory wiki at `memory/`.

## Rules

### 1. Plan Before Coding
- **For any task with 3+ expected steps, outline the approach before writing code.**
- Define what "done" looks like — including acceptance criteria and verification steps.
- List the files you expect to change and why.
- Get approval before implementing.

### 2. Verify Before Done
- Never mark a task complete without proving it works.
- Run tests, check logs, demonstrate correctness.
- Diff behavior between before and after when relevant.

### 3. Learn From Mistakes
- After ANY correction from the user: update the project's wiki page at `memory/wiki/projects/{project-name}.md` — append to "## Lessons Learned".
- Write rules that prevent the same mistake from recurring.
- Review the project's wiki page at session start.

### 4. No Blind Retries
- **Never retry a command that failed with a non-transient error.** Diagnose the root cause instead.
- Non-transient: validation errors, 401, 403, permission denied.
- Transient (ok to retry once): network timeout, 429, 503, connection reset.
- After 2 failures on the same command: stop, explain the issue, ask the user.

### 5. Keep It Simple
- Don't add features, refactor code, or make improvements beyond what was asked.
- For non-trivial changes: pause and ask "is there a more elegant way?"
- If a fix feels hacky: step back and implement the clean solution.

## Session Routine

**Start of session:**
- Read the project's wiki page at `memory/wiki/projects/{project-name}.md` — especially "## Lessons Learned".
- Review any active work notes or prior session context.

**End of session:**
- Capture any new lessons in the project's wiki page ("## Lessons Learned").
- Note what was done and what's next.
- Follow the end-session skill (`memory/workflows/end-session.md` or trigger word "end session").

**Wiki compounding (when significant work was done):**
- If a reusable pattern was discovered, create or update a page in `memory/wiki/patterns/`.
- If a domain gotcha was learned, update the relevant `memory/wiki/domains/*.md` page.
- Update `memory/log.md` with: `- **{timestamp}** | UPDATE | "{what changed}" | project: {name}`

## Available Skills

The following skills are installed via tri-surface (both GitHub Copilot CLI and Claude Code can trigger them):

| Skill | Trigger | Purpose |
|---|---|---|
| `ingest` | "ingest X" | Compile a source into the wiki with raw-source and graph checks |
| `end-session` | "end session", "wrap up" | Capture lessons, update project page, git check |
| `query` | "query X", "what do we know about X" | Answer a question with `[[wikilinks]]` |
| `lint` | "lint", "health check" | Run wiki health checks, report findings |
| `plan-week` | "plan week", "Monday plan" | Draft the ISO week's plan |
| `close-week` | "close week", "Friday review" | Aggregate the week's activity, freeze the file |
| `project-status` | "project status" (from inside a child project) | 30-sec situational briefing |
| `review-sessions` | "review sessions" | Analyse past sessions for workflow improvements |
| `new-engagement` | "new engagement <Client> — <topic> (format)" | Scaffold a new client engagement from `project-template/` |

## Project Structure Convention

Every project scaffolded by `new-engagement` (or created manually) has this shape:

```
project-root/
├── AGENT.md                                            # MAIN — overview, env, commands, workflow, refs
├── CLAUDE.md                                           # Thin shim → "Read AGENT.md"
├── README.md                                           # Human-facing
├── LICENSE                                             # Open-source license
├── .gitignore
├── .github/
│   ├── copilot-instructions.md                         # GitHub Copilot CLI shim → AGENT.md
│   └── instructions/
│       └── end-session.instructions.md                 # Per-project end-session shim
├── .claude/
│   ├── CLAUDE.md                                       # Claude Code project config
│   └── commands/
│       └── status.md                                   # /status slash-command (30-sec briefing)
└── (format-specific folders: slides/, demos/, exercises/, docs/...)
```

Lessons learned and technical reference are centralized in `memory/wiki/projects/{project-name}.md` — not duplicated in the repo.
```

---
"""


def section_agent_platform() -> str:
    return """### Step 8: Create `memory/agent-config/platform.md`

Ask the user what platform they're on (OS, language runtimes, cloud provider). If the user doesn't specify, create sensible defaults:

```markdown
---
title: Platform & Preferences
category: agent-config
tags: [platform, environment]
date_created: {{today}}
date_updated: {{today}}
---

# Platform & Preferences

## Environment

- OS: (ask user, or detect from current environment)
- Primary language(s): (ask user)
- Cloud provider: (ask user, or "none" if local-only)

## Platform Gotchas

<!-- Add platform-specific gotchas as you discover them -->
<!-- Example: "Always use encoding='utf-8' for subprocess on Windows" -->

## Cross-Project Knowledge

Shared domain knowledge files are stored in `agent-config/knowledge/` — consult when working in the relevant domain.
```

---
"""


def section_skills() -> str:
    """Generate Step 2 — all 9 skills × 3 copies.

    Strategy: emit each skill body once inside a fenced block, then provide
    instructions to save it to 3 paths with 3 frontmatter wrappers.
    """
    parts = [
        "### Step 2: Install all 9 skills before creating wiki content\n",
        "**This is the first mandatory deliverable. Do not continue to Step 3 until its gate passes.**\n",
        "For each skill below, create **3 files** containing the **same body** but **different frontmatter**:\n",
        "1. `.github/instructions/{slug}.instructions.md` — frontmatter: `---\\napplyTo: \"**\"\\n---`",
        "2. `.claude/skills/{slug}/SKILL.md` — frontmatter: `---\\nname: {slug}\\ndescription: <see per-skill description below>\\n---`",
        "3. `memory/workflows/{slug}.md` — frontmatter: `---\\napplyTo: \"**\"\\n---`",
        "",
        "Create each set of 3 files immediately before moving to the next skill. The body is byte-identical across all 3 files; only the frontmatter differs.",
        "",
        "If a destination file already exists, verify its frontmatter and body. Keep it if correct; otherwise repair it. This makes interrupted installs safe to resume.",
        "",
        "---\n",
    ]

    for slug in SKILLS:
        body = read_body(ROOT / "memory" / "workflows" / f"{slug}.md")
        description = read_claude_description(slug)
        parts.append(f"#### Skill: `{slug}`\n")
        parts.append(f"**Claude Code description** (for `.claude/skills/{slug}/SKILL.md` frontmatter):\n")
        parts.append("```yaml")
        parts.append(f"name: {slug}")
        parts.append(f"description: {description}")
        parts.append("```\n")
        parts.append(f"**Body** (save to all 3 paths — `.github/instructions/{slug}.instructions.md`, `.claude/skills/{slug}/SKILL.md`, `memory/workflows/{slug}.md`):\n")
        parts.append(fence(body, "markdown"))
        parts.append("\n---\n")

    parts.extend(
        [
            "#### Mandatory Gate A: executable skills are installed\n",
            "Before creating any wiki content, inspect the filesystem and prove all of the following:\n",
            "",
            "- `.github/instructions/` contains the 9 generated `*.instructions.md` files.",
            "- `.claude/skills/` contains the 9 generated `{slug}/SKILL.md` files.",
            "- `memory/workflows/` contains the 9 generated `{slug}.md` files.",
            "- Every native file has the required frontmatter.",
            "- After stripping frontmatter, each skill's body matches across all 3 copies.",
            "",
            "Expected counts: **9 Copilot + 9 Claude + 9 agent-neutral = 27 files**.",
            "",
            "If any check fails, stop here and repair the skill installation. **Do not proceed with a wiki-only installation.**",
            "",
            "---\n",
        ]
    )

    return "\n".join(parts) + "\n"


def section_templates() -> str:
    return """### Step 9: Create template files

#### Create `memory/templates/project.md`

```markdown
---
title: "{{title}}"
category: projects
tags: []
source_docs: []
date_created: {{date}}
date_updated: {{date}}
---

# {{title}}

## Overview
<!-- What this project does, its purpose -->

## Architecture
<!-- Key components, tech stack, data flow -->

## Key Paths
<!-- Important files and directories -->

## Lessons Learned
<!-- Append discoveries here. Format: ### Lesson title\\n- What/Why/How -->

## Open Actions
<!-- Active work items -->

## Related
<!-- [[wikilinks]] to domains, patterns, lessons -->

## Sources
<!-- Reference docs, URLs, raw/ files -->
```

#### Create `memory/templates/lesson.md`

```markdown
---
title: "{{title}}"
category: lessons
tags: []
source_docs: []
date_created: {{date}}
date_updated: {{date}}
---

# {{title}}

## Context
<!-- Where this came up, what we were doing -->

## What Happened
<!-- The failure mode, error message, surprise -->

## Root Cause
<!-- The actual underlying reason -->

## Fix
<!-- What we did, why it works -->

## Prevention
<!-- How to avoid hitting this again -->

## Related
<!-- [[wikilinks]] -->
```

---
"""


def section_root_files() -> str:
    return """### Step 10: Create project root files

#### Create `AGENT.md` at the project root

```markdown
# AGENT.md

This project uses a **persistent memory wiki** at `memory/`. Read these files to understand the workflow:

- `memory/agent-config/workflow.md` — Cross-project rules (plan before coding, verify before done, etc.)
- `memory/agent-config/platform.md` — Platform & environment preferences
- `memory/schema.md` — Wiki governance and article format
- `memory/index.md` — Content catalog (read first when answering a query)
- `memory/glossary.md` — Canonical terms

## Triggerable Skills

The following workflows can be invoked by name (both GitHub Copilot CLI and Claude Code will route them):

| Trigger | Skill |
|---|---|
| "ingest <X>" | Compile X into the wiki |
| "query <Q>" | Answer Q from the wiki |
| "end session" | Capture lessons, update docs, git check |
| "lint" | Run wiki health checks |
| "plan week" | Draft this week's Monday plan |
| "close week" | Friday review + activity aggregation |
| "project status" | 30-sec briefing of the current project |
| "review sessions" | Analyse past sessions for improvements |
| "new engagement <Client> — <topic> (<format>)" | Scaffold a new engagement from `project-template/` |

## Project-Specific Notes

<!-- Add project-specific instructions here. Tech stack, key commands, etc. -->
```

#### Create `CLAUDE.md` at the project root

```markdown
# Claude Code Instructions

Read `AGENT.md` for all project instructions, workflow rules, and references.
```

#### Create `.github/copilot-instructions.md` at the project root

```markdown
# GitHub Copilot Instructions

Read `AGENT.md` for all project instructions, workflow rules, and references.

All triggerable skills live under `.github/instructions/` and are auto-loaded via `applyTo: "**"`.
```

---
"""


def section_project_template() -> str:
    """Generate Step 11 — the project-template/ scaffold."""
    parts = [
        "### Step 11: Create the required `project-template/` scaffold\n",
        "The `new-engagement` skill uses `project-template/` as its offline source when scaffolding a client engagement. Create all 9 files below at `project-template/<path>`; do not skip this step.\n",
        "---\n",
    ]
    for rel in TEMPLATE_FILES:
        content = read_file(rel)
        ext = Path(rel).suffix.lstrip(".")
        lang_map = {"md": "markdown", "yml": "yaml", "yaml": "yaml"}
        lang = lang_map.get(ext, "")
        if rel == "LICENSE":
            lang = "text"
        elif rel == ".gitignore":
            lang = "gitignore"
        parts.append(f"#### Create `project-template/{rel}`\n")
        parts.append(fence(content, lang))
        parts.append("\n---\n")
    return "\n".join(parts) + "\n"


def section_verification() -> str:
    return """### Step 12: Verification

## Definition of Done

The setup is complete only when every required item below passes. Inspect the files; do not mark boxes based on intended work.

```
[ ] SKILL GATE: 9 Copilot instruction files exist under .github/instructions/
[ ] SKILL GATE: 9 Claude SKILL.md files exist under .claude/skills/
[ ] SKILL GATE: 9 agent-neutral workflow files exist under memory/workflows/
[ ] SKILL GATE: all 9 skill bodies match across the 3 copies after frontmatter is removed
[ ] DEPENDENCY GATE: no installed skill or template requires a helper script that this bootstrap does not create
[ ] PORTABILITY GATE: no installed skill or template contains a maintainer-specific home-directory path
[ ] memory/schema.md exists with YAML frontmatter
[ ] memory/index.md exists with category sections
[ ] memory/log.md exists with INIT entry
[ ] memory/glossary.md exists
[ ] memory/agent-config/workflow.md exists
[ ] memory/agent-config/platform.md exists
[ ] memory/templates/project.md exists with frontmatter template
[ ] memory/templates/lesson.md exists with frontmatter template
[ ] memory/wiki/{projects,domains,patterns,lessons,skills,agents,tools,_queries}/ directories exist
[ ] memory/raw/ directory exists
[ ] memory/ops/weekly/ directory exists and memory/ops/activity.jsonl exists (empty)
[ ] project-template/ scaffold exists with all 9 canonical files
[ ] AGENT.md exists at project root and references memory/agent-config/workflow.md + lists all 9 skills
[ ] CLAUDE.md exists at project root and points to AGENT.md
[ ] .github/copilot-instructions.md exists at project root and points to AGENT.md
```

### Required completion report

Report one of these outcomes:

- `SETUP COMPLETE — 9/9 skills installed for Copilot CLI and Claude Code; 27/27 skill files present; wiki ready.`
- `SETUP INCOMPLETE — <failed checks and missing paths>.` Then continue repairing the failed checks; do not stop at this report unless blocked by permissions or missing tool access.

Do not call a directory under `memory/wiki/skills/` an installed skill surface. It is wiki content only.

Newly created skills may require a **new agent session** before GitHub Copilot CLI or Claude Code discovers them. File verification happens now; discovery is smoke-tested after restarting the agent in this folder.

---
"""


def section_next_steps() -> str:
    return """## Next Steps

Setup is complete. Here's how to use your memory system:

1. **Try your first ingest:** Tell your agent `ingest` followed by any topic you've learned today — a debugging breakthrough, a new tool, an architecture decision. The agent will preserve the raw source, compile durable knowledge, update the graph, and run its audit gates.

2. **At the end of your session:** Tell your agent `end session` to capture lessons learned, update project docs, and compound knowledge.

3. **Query your knowledge:** Ask your agent `query <question>` — it will search the wiki and synthesize an answer with `[[wikilink]]` citations.

4. **Weekly rhythm:** On Monday, `plan week`. On Friday, `close week`. The activity log (`memory/ops/activity.jsonl`) accumulates ingest events, and `close-week` aggregates them into the week's file.

5. **Health checks:** Run `lint` periodically to surface orphan pages, broken wikilinks, and thin pages.

6. **Project briefings:** From inside any child project, run `project status` for a 30-second situational summary.

7. **New engagements:** When starting a new client engagement, say `new engagement <Client> — <topic> (<format>)` and the agent will scaffold the project from `project-template/`.

8. **Session review:** Run `review sessions` to analyse GitHub Copilot CLI and Claude Code JSONL data for workflow improvements.

It compounds over time. Each session adds to the wiki. After a few weeks, your agent will have a rich knowledge base of your projects, patterns, and hard-won lessons — and it never forgets.
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Regenerate bootstrap.md from canonical skill bodies + project-template files.")
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=ROOT / "bootstrap.md",
        help="Path to write bootstrap.md (default: <repo>/bootstrap.md)",
    )
    args = parser.parse_args()

    validate_sources()

    out = []
    out.append(HEADER)
    out.append(section_skills())
    out.append(section_schema())
    out.append(section_index())
    out.append(section_log())
    out.append(section_glossary())
    out.append(section_agent_workflow())
    out.append(section_agent_platform())
    out.append(section_templates())
    out.append(section_root_files())
    out.append(section_project_template())
    out.append(section_verification())
    out.append(section_next_steps())

    final = "\n".join(out)
    final = final.replace("\r\n", "\n").rstrip() + "\n"
    consumer_errors = validate_consumer_text(final, "generated bootstrap")
    if consumer_errors:
        raise ValueError("Generated bootstrap dependency validation failed:\n- " + "\n- ".join(consumer_errors))

    # Write directly as UTF-8 bytes — never go through stdout (Windows
    # PowerShell `>` redirect re-encodes the stream and produces mojibake).
    args.output.write_bytes(final.encode("utf-8"))
    print(f"Wrote {args.output} ({len(final.encode('utf-8'))} bytes)")


if __name__ == "__main__":
    main()
