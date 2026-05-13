# 🧠 AI Agent Memory

> A practical, git-native implementation of the [Karpathy LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) pattern for persistent coding-agent memory.

**The problem:** AI coding agents are stateless — every session starts from scratch. But it gets worse: if you use GitHub Copilot with multiple agents (built-in + 3rd-party like Claude, Codex), each has its own instruction format. Maintaining separate config files across every project, for every agent, doesn't scale. And knowledge stays siloed per project — a pattern you discovered in one client project is invisible to the next.

**The solution:** A central markdown wiki that all your agents share, across all your projects. Each project points to it through a single `AGENT.md`; each agent-specific config file (`.github/copilot-instructions.md`, `CLAUDE.md`, etc.) simply redirects there. The wiki grows with every session — call `end-session` and the agent captures lessons, decisions, and patterns back into the wiki. Knowledge learned in one project (a deployment gotcha, an API pattern, a debugging technique) is immediately available in every other project. The next session, with *any* agent, on *any* project, starts with all that accumulated knowledge.

Works with: **GitHub Copilot** · **Claude Code** · **Codex** · **Cursor** · **Gemini CLI** · **Aider**

---

## Motivation

I use **GitHub Copilot** daily — not just the built-in agent, but also the 3rd-party agents available inside it (Claude, Codex, and others). Each agent has its own instruction file format (`.github/copilot-instructions.md`, `CLAUDE.md`, `AGENTS.md`, `.cursor/rules/`…). Creating and maintaining agent-specific config files across every project doesn't scale.

Instead of duplicating context everywhere, I built a **central LLM wiki** using the [Karpathy pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). It holds my skills, commands, workflows, domain knowledge, and lessons learned — all in plain markdown. Every project points to it through a single `AGENT.md`, and every agent-specific config file simply redirects there.

The wiki is a **living memory**. It keeps growing regardless of which agent I'm using. At the end of every coding session, I call `end-session` — the agent reviews the session, captures lessons, and writes them back to the wiki. The next session — with *any* agent — starts with all that accumulated knowledge. No context is lost, no knowledge is siloed.

---

## Quick Start

### Option 1: Fork this repo (recommended)

```bash
git clone https://github.com/{your-username}/ai-agent-memory.git ~/projects/memory

# Edit your preferences
$EDITOR memory/agent-config/platform.md

# In each project, add a pointer in AGENT.md:
# "Read ~/projects/memory/agent-config/workflow.md for global rules."
```

### Option 2: Ask your agent to bootstrap it

You don't need to set anything up manually. Just give [`bootstrap.md`](bootstrap.md) to your AI coding agent — it contains step-by-step instructions that the agent will follow to create the entire memory system.

`bootstrap.md` is **fully self-contained** (~80 KB, no network access required). It installs all 9 skills × 3 surfaces (`.github/instructions/`, `.claude/skills/`, `memory/workflows/`) plus the optional `project-template/` scaffold consumed by `new-engagement`.

> **Maintainers:** `bootstrap.md` is regenerated from the canonical skill bodies + `project-template/` files by [`scripts/regenerate-bootstrap.py`](scripts/regenerate-bootstrap.py). Run `python scripts/regenerate-bootstrap.py` after any skill or template change.

**With GitHub Copilot (VS Code):**

1. Open a new folder in VS Code (this will become your `memory/` project)
2. Open Copilot Chat (Ctrl+I) in agent mode
3. Say: *"Follow the instructions in bootstrap.md to set up a persistent memory wiki"* and attach the file
4. The agent creates the full directory structure, schema, workflows, templates, and example content
5. Verify the structure, then commit

**With any other agent (Claude Code, Codex, Cursor…):**

1. Copy the contents of `bootstrap.md`
2. Paste it into your agent's chat
3. The agent follows the instructions and creates everything
4. Verify and commit

Once the wiki exists, add a pointer in each project's instruction file. For GitHub Copilot, add this to `.github/copilot-instructions.md`:

```markdown
Read these files for full context:
- `AGENT.md` — Project instructions
- `~/projects/memory/agent-config/workflow.md` — Global workflow rules

## Wiki Skills
When the user says "ingest", follow: `~/projects/memory/workflows/ingest.md`
When the user says "end session", follow: `~/projects/memory/workflows/end-session.md`
```

That's it — your agent now has persistent memory and 3 skills.

---

## Architecture

Projects reference the memory wiki via `AGENT.md` pointers. Each project has agent-specific config files (`.github/copilot-instructions.md`, `CLAUDE.md`) that all redirect to the same `AGENT.md`, which in turn points to the central memory wiki. The wiki has three layers:

```
┌──────────────────────────────────────────────────────────────────┐
│                         YOUR PROJECTS                            │
│                                                                  │
│  project-a/                project-b/             project-c/     │
│  ├── .github/              ├── .github/           ├── .github/   │
│  │   └── copilot-          │   └── copilot-       │   └── ...    │
│  │       instructions.md   │       instructions.md│              │
│  ├── AGENT.md ──┐          ├── AGENT.md ──┐       ├── AGENT.md   │
│  ├── CLAUDE.md  │          ├── CLAUDE.md  │       └── src/       │
│  └── src/       │          └── src/       │                      │
│                 │                         │                      │
│                 ▼                         ▼                      │
│          ┌──────────────────────────────────────┐                │
│          │           MEMORY WIKI                │                │
│          │  ┌────────────────────────────────┐  │                │
│          │  │ Layer 1: Instructions          │  │                │
│          │  │ agent-config/workflow.md       │  │                │
│          │  │ agent-config/platform.md       │  │                │
│          │  ├────────────────────────────────┤  │                │
│          │  │ Layer 2: Workflows             │  │                │
│          │  │ workflows/ingest.md            │  │                │
│          │  │ workflows/end-session.md       │  │                │
│          │  │ workflows/query.md             │  │                │
│          │  ├────────────────────────────────┤  │                │
│          │  │ Layer 3: Knowledge             │  │                │
│          │  │ wiki/projects/                 │  │                │
│          │  │ wiki/domains/                  │  │                │
│          │  │ wiki/patterns/                 │  │                │
│          │  │ wiki/lessons/                  │  │                │
│          │  └────────────────────────────────┘  │                │
│          └──────────────────────────────────────┘                │
└──────────────────────────────────────────────────────────────────┘
```

**Layer 1 — Instructions:** Global rules (workflow conventions, platform preferences) that every agent reads at session start.

**Layer 2 — Workflows:** Step-by-step procedures agents follow for ingesting knowledge, ending sessions, and querying the wiki.

**Layer 3 — Knowledge:** The wiki itself — project pages, domain references, reusable patterns, and debugging lessons. Grows over time.

### How GitHub Copilot Connects

GitHub Copilot automatically reads `.github/copilot-instructions.md` at the start of every chat session. This file acts as the entry point into the memory system:

```markdown
# .github/copilot-instructions.md

# Copilot Instructions

Read these files for full context:

- `AGENT.md` — Project instructions, workflow rules, architecture, key paths
- `~/projects/memory/wiki/projects/{project}.md` — Project wiki page (lessons, decisions)
- `~/projects/memory/agent-config/workflow.md` — Global workflow rules

## Copilot-Specific Tips

- Use `@workspace` to give Copilot full project context
- Pin `AGENT.md` in chat for persistent context
- Use Copilot Edits (Ctrl+Shift+I) for multi-file changes
- When corrected, update the project wiki page
```

This same pattern works for every agent — each reads its own config file, but all of them end up at the same `AGENT.md` and the same memory wiki. One source of truth, multiple entry points.

---

## How It Works

Nine skills drive the system. The three core skills below are the heart of the wiki workflow; six more (`lint`, `plan-week`, `close-week`, `project-status`, `review-sessions`, `new-engagement`) ship alongside them in every supported surface. Agents discover all nine through one of three parallel locations — `.github/instructions/` (GitHub Copilot CLI), `.claude/skills/` (Claude Code), or `memory/workflows/` (human-readable canonical source) — see [CONTRIBUTING.md](CONTRIBUTING.md) for the per-surface frontmatter contract.

### 1. Ingest — Add knowledge to the wiki

Say "ingest" followed by content (a document, lesson, conversation). The agent runs a 7-phase pipeline: gather context → classify → compile → update graph → copy raw → self-audit → report.

**Key rule:** Target 8–15 files touched per ingest. If you only touched 2–3, you missed graph updates (index, glossary, backlinks).

### 2. End Session — Capture lessons before context is lost

Say "end session" at the end of a coding session. The agent runs a 5-step routine: capture lessons → cross-project knowledge → update log → git check → summary.

This is where knowledge compounds. Mistakes, decisions, and patterns get written to the wiki so the next session starts smarter.

### 3. Query — Ask questions against the wiki

Ask any question. The agent reads `index.md` first for navigation, then reads relevant pages, synthesizes an answer with `[[wikilink]]` citations, and flags knowledge gaps for future ingest.

📄 **Full details:** [`docs/workflows.md`](docs/workflows.md) and [`memory/workflows/`](memory/workflows/)

---

## Agent Compatibility

### GitHub Copilot — Primary Workflow

GitHub Copilot is the primary agent for this system. It reads `.github/copilot-instructions.md` automatically, and with the **agent mode** in VS Code, it can also use 3rd-party models (Claude, Codex, Gemini) — all of which inherit the same instruction file. This means you configure once and every agent inside Copilot gets the same context.

| File | Purpose | Read By |
|------|---------|---------|
| `.github/copilot-instructions.md` | Auto-loaded by Copilot → points to `AGENT.md` | **GitHub Copilot** (+ all agents within it) |
| `.github/instructions/*.instructions.md` | Auto-loaded by GitHub Copilot CLI; each file is a skill keyed off a trigger phrase | **GitHub Copilot CLI** |
| `AGENT.md` | Project identity + workflow rules + wiki pointers | All agents (standard) |
| `CLAUDE.md` | Pointer → `AGENT.md` | Claude Code (standalone) |
| `.claude/skills/{slug}/SKILL.md` | Auto-discovered by Claude Code inside this repo; routed by the `description:` field | **Claude Code** (project-scoped) |
| `.cursor/rules/` | Pointer → `AGENT.md` | Cursor |

### Agent Support

| Agent | Config File | Memory Access | Status |
|-------|-------------|---------------|--------|
| GitHub Copilot | `.github/copilot-instructions.md` | Workspace files | ✅ Tested |
| GitHub Copilot CLI | `.github/instructions/*.instructions.md` (auto-discovered) | Workspace files | ✅ Tested |
| GitHub Copilot (3rd-party agents) | `.github/copilot-instructions.md` (shared) | Workspace files | ✅ Tested |
| Claude Code | `CLAUDE.md` + `.claude/skills/*/SKILL.md` (auto-discovered, project-scoped) | Full filesystem | ✅ Tested |
| Codex (OpenAI) | `AGENT.md` (native) | Sandbox (limited) | ⚠️ Partial |
| Cursor | `.cursor/rules/` | Workspace files | ⚠️ Partial |
| Gemini CLI | `AGENT.md` (native) | Full filesystem | ⚠️ Partial |
| Aider | Convention files | Full filesystem | ⚠️ Partial |

### Memory Modes

Where you place the `memory/` folder depends on your agent's filesystem access:

| Mode | Layout | Best For |
|------|--------|----------|
| **Same-workspace** | `my-project/memory/` | Agents with workspace-only access (Cursor, Copilot) |
| **Sibling-folder** | `projects/memory/` alongside `projects/my-project/` | Most agents |
| **Central external** | `~/projects/memory/` | Claude Code, full-filesystem agents |

---

## Repo Structure

```
ai-agent-memory/
├── README.md                  # This file
├── AGENT.md                   # Project instructions for AI agents
├── CLAUDE.md                  # Claude Code pointer → AGENT.md
├── LICENSE                    # MIT
├── bootstrap.md               # Self-contained bootstrap prompt (regenerated from this repo)
├── CHANGELOG.md               # Calendar-versioned release notes
├── CONTRIBUTING.md            # Contribution & release process
│
├── scripts/
│   └── regenerate-bootstrap.py  # Regenerates bootstrap.md from skill bodies + project-template
│
├── .github/
│   ├── copilot-instructions.md  # GitHub Copilot pointer → AGENT.md
│   └── instructions/            # GitHub Copilot CLI skill auto-discovery
│       └── {slug}.instructions.md
│
├── .claude/                     # Claude Code project-scoped surface
│   └── skills/                  # Claude Code skill auto-discovery
│       └── {slug}/
│           └── SKILL.md
│
├── docs/
│   └── workflows.md           # Human-readable workflow documentation
│
├── memory/                    # ── THE WIKI ──
│   ├── index.md               # Content catalog (read this first)
│   ├── schema.md              # Wiki conventions and article format
│   ├── glossary.md            # Canonical terms
│   ├── log.md                 # Chronological session log
│   │
│   ├── agent-config/          # Layer 1: Instructions
│   │   ├── workflow.md        # Global workflow rules
│   │   └── platform.md       # Platform preferences & environment
│   │
│   ├── workflows/             # Layer 2: Plain-Markdown skill reference
│   │   ├── ingest.md          # Karpathy LLM-wiki ingest pipeline
│   │   ├── end-session.md     # End-of-session capture
│   │   ├── query.md           # Index-first query procedure
│   │   └── ...                # Other skills (one .md per skill)
│   │
│   ├── templates/             # Starter templates for new pages
│   │   ├── project.md         # New project wiki page
│   │   └── lesson.md          # New lesson page
│   │
│   ├── wiki/                  # Layer 3: Knowledge base
│   │   ├── projects/          # One page per project
│   │   ├── domains/           # Technology references
│   │   ├── patterns/          # Reusable solutions
│   │   └── lessons/           # Debugging stories
│   │
│   └── raw/                   # Raw source documents (pre-compilation)
│
├── demo-project/              # Example project showing AGENT.md setup
│   ├── AGENT.md
│   ├── CLAUDE.md
│   ├── .github/
│   └── src/
│
└── project-template/          # Canonical scaffold consumed by the new-engagement skill
    ├── AGENT.md               #   - Project identity (single source of truth)
    ├── CLAUDE.md              #   - Thin shim → "Read AGENT.md"
    ├── README.md              #   - Human-facing template README
    ├── LICENSE                #   - MIT
    ├── .gitignore             #   - Tracks .claude/CLAUDE.md + .claude/commands/, ignores the rest
    ├── .claude/
    │   ├── CLAUDE.md          #   - Claude Code project config + project-context block
    │   └── commands/
    │       └── status.md      #   - /status slash-command (30-second project briefing)
    └── .github/
        ├── copilot-instructions.md          # Copilot pointer → AGENT.md
        └── instructions/
            └── end-session.instructions.md  # Per-project end-session shim
```

---

## Demo Content

This repo ships with fictional demo content to illustrate the wiki structure:

- **2 demo projects:** Weather API, Recipe Chatbot
- **1 domain page:** FastAPI
- **1 pattern page:** Retry with Backoff
- **1 lesson page:** API Auth Debugging

All demo content is marked with `<!-- DEMO DATA -->` comments. After forking, replace it with your own content — or delete the demo pages and start fresh with an empty wiki.

---

## Obsidian (Optional)

The wiki uses `[[wikilinks]]`, YAML frontmatter, and a flat-ish directory structure — all of which work natively with [Obsidian](https://obsidian.md).

- Open `memory/` as an Obsidian vault for graph view, backlink navigation, and full-text search
- **Obsidian is not required** — the wiki works as plain markdown files in any editor or on GitHub

---

## Security & Privacy

### What NEVER goes into memory

- ❌ API keys, tokens, passwords, secrets
- ❌ Raw client data or PII
- ❌ Proprietary source code
- ❌ Internal architecture diagrams with real endpoints

### What SHOULD go into memory

- ✅ Patterns and conventions (abstracted)
- ✅ Lessons learned (root cause + rule)
- ✅ Architecture decisions (why, not what)
- ✅ Domain knowledge (public technical info)

The wiki is designed to be safe to commit to a private repo. If you keep it in a public repo, double-check that no sensitive information has been ingested.

---

## FAQ

**Do I need Obsidian?**
No. Obsidian is an optional visualization layer. The wiki is plain markdown — any editor works.

**Does this work offline?**
Yes. Everything is local markdown files tracked in git. No cloud services, no APIs, no subscriptions.

**How big does the wiki get?**
At ~100 pages it's very manageable. At 1000+ pages, consider adding hierarchical sub-indexes within each wiki category. The `index.md` file is the primary navigation aid.

**Can I use this with a team?**
Yes. The wiki is git-native, so branching and merging work normally. Define write conventions (e.g., who owns which project pages) and use PRs for contested changes.

**How is this different from Mem0 / Letta / other memory services?**
Those are hosted memory services with vector stores, APIs, and automatic retrieval. This is local, git-native, human-readable markdown. Simpler, more transparent, and fully under your control — but less automated. Use what fits your workflow.

**What if my agent can't access the memory folder?**
Use same-workspace mode: place `memory/` inside your project directory so the agent can reach it through workspace file access.

---

## Release notes

See [CHANGELOG.md](CHANGELOG.md) for the version history. Contributions are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md) for skill style, changelog conventions, and the release process.

---

## Credits

- [Andrej Karpathy — LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — the original idea
- [AGENTS.md — open standard](https://agents-md.org) — agent instruction file convention
- [Simon Willison — files-to-prompt](https://github.com/simonw/files-to-prompt) — useful companion tool

### Related Projects

- [Mem0](https://github.com/mem0ai/mem0) — managed memory layer for AI agents
- [Letta](https://github.com/letta-ai/letta) — stateful LLM agents with memory
- [Graphiti](https://github.com/getzep/graphiti) — temporal knowledge graphs for agents
- [agentmemory](https://github.com/rohitg00/agentmemory) — simple agent memory library

---

## License

[MIT](LICENSE)
