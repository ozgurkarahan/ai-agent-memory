# 🧠 AI Agent Memory

> A practical, git-native implementation of the [Karpathy LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) pattern for persistent coding-agent memory.

**The problem:** AI coding agents are stateless. Every session starts from scratch. Your knowledge compounds, but your agents' doesn't.

**The solution:** A local markdown wiki that lives alongside your projects. Your agents read it for context. You browse it in Obsidian. Knowledge compounds across sessions and tools.

Works with: **Claude Code** · **GitHub Copilot** · **Codex** · **Cursor** · **Gemini CLI** · **Aider**

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

### Option 2: Bootstrap from scratch

Give [`bootstrap.md`](bootstrap.md) to any AI coding agent. It contains the full setup instructions — the agent will create the wiki structure for you.

```
# Copy the contents of bootstrap.md → paste into your AI agent → verify setup
```

---

## Architecture

Projects reference the memory wiki via `AGENT.md` pointers. The wiki has three layers:

```
┌─────────────────────────────────────────────────────────┐
│                      YOUR PROJECTS                       │
│                                                          │
│  project-a/           project-b/          project-c/     │
│  ├── AGENT.md ──┐     ├── AGENT.md ──┐    ├── AGENT.md   │
│  ├── CLAUDE.md  │     ├── CLAUDE.md  │    └── ...        │
│  └── src/       │     └── src/       │                   │
│                 │                    │                    │
│                 ▼                    ▼                    │
│          ┌──────────────────────────────────┐             │
│          │          MEMORY WIKI             │             │
│          │  ┌────────────────────────────┐  │             │
│          │  │ Layer 1: Instructions      │  │             │
│          │  │ agent-config/workflow.md   │  │             │
│          │  │ agent-config/platform.md   │  │             │
│          │  ├────────────────────────────┤  │             │
│          │  │ Layer 2: Workflows         │  │             │
│          │  │ workflows/ingest.md        │  │             │
│          │  │ workflows/end-session.md   │  │             │
│          │  │ workflows/query.md         │  │             │
│          │  ├────────────────────────────┤  │             │
│          │  │ Layer 3: Knowledge         │  │             │
│          │  │ wiki/projects/             │  │             │
│          │  │ wiki/domains/              │  │             │
│          │  │ wiki/patterns/             │  │             │
│          │  │ wiki/lessons/              │  │             │
│          │  └────────────────────────────┘  │             │
│          └──────────────────────────────────┘             │
└─────────────────────────────────────────────────────────┘
```

**Layer 1 — Instructions:** Global rules (workflow conventions, platform preferences) that every agent reads at session start.

**Layer 2 — Workflows:** Step-by-step procedures agents follow for ingesting knowledge, ending sessions, and querying the wiki.

**Layer 3 — Knowledge:** The wiki itself — project pages, domain references, reusable patterns, and debugging lessons. Grows over time.

---

## How It Works

Three workflows drive the system. Agents discover them through `AGENT.md` → `agent-config/workflow.md` → `workflows/`.

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

### Config File Matrix

Each agent reads a different config file. All point to the same `AGENT.md`:

| File | Purpose | Read By |
|------|---------|---------|
| `AGENT.md` | Project identity + workflow rules | All agents (standard) |
| `CLAUDE.md` | Pointer → `AGENT.md` | Claude Code |
| `.github/copilot-instructions.md` | Pointer → `AGENT.md` | GitHub Copilot |
| `.cursor/rules/` | Pointer → `AGENT.md` | Cursor |

### Agent Support

| Agent | Config File | Memory Access | Status |
|-------|-------------|---------------|--------|
| Claude Code | `CLAUDE.md` | Full filesystem | ✅ Tested |
| GitHub Copilot | `.github/copilot-instructions.md` | Workspace files | ✅ Tested |
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
├── bootstrap.md               # Full bootstrap instructions for any agent
│
├── .github/
│   └── copilot-instructions.md  # GitHub Copilot pointer → AGENT.md
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
│   ├── workflows/             # Layer 2: Workflow procedures
│   │   ├── ingest.md          # 7-phase ingest pipeline
│   │   ├── end-session.md     # 5-step end-session routine
│   │   └── query.md           # Index-first query procedure
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
└── project-template/          # Starter template for new projects
    ├── AGENT.md
    ├── CLAUDE.md
    └── .github/
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
