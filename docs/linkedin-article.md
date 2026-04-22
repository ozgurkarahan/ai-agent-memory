<!-- LinkedIn article draft — copy to LinkedIn editor -->

# 🧠 I Built a Persistent Memory System for AI Coding Agents. Here's How It Works.

**I got tired of re-explaining my projects every time I switched agents or started a new session.**

I use AI coding agents every day — Claude Code, GitHub Copilot with Claude and Codex agents. They're incredible. But every new session starts from scratch. The agent doesn't know my architecture, my past mistakes, my conventions, the debugging gotcha I solved last Tuesday.

So I spend the first 5–10 minutes of every session providing context. "This project uses FastAPI." "The routes are in `src/api/`." "We authenticate with Entra ID tokens." "Don't use `subprocess` without `encoding='utf-8'` on Windows."

And when I switch between agents? The problem multiplies. My knowledge compounds across sessions. My agents' doesn't.

---

## The Problem: Session Amnesia

AI coding agents are stateless between sessions. Every session starts cold — no memory of past decisions, lessons learned, or architecture choices.

This means:
- The agent re-discovers your project structure every time
- Lessons from debugging sessions are lost
- Patterns you've established get forgotten
- The same mistakes get suggested again
- Switching between Claude Code, Copilot, and Codex triples the context cost

Your brain compounds knowledge naturally. You remember that the Redis cache has a 5-minute TTL, that the staging environment needs a VPN, that the APIM policy needs double braces. Your agents remember none of it.

---

## The Constraint: It Had to Work Everywhere

Before building anything, I set constraints:

- **Tool-agnostic** — Must work with ANY agent. Not locked to one vendor.
- **Local-first** — No hosted service, no API keys, no vendor dependency.
- **Human-readable** — I should be able to browse it in my editor too.
- **Git-native** — Version history comes for free.
- **Simple** — Just markdown files. No databases, no complex infrastructure.

If it required a proprietary format or a running service, it would eventually break or get abandoned. Markdown in a git repo doesn't break.

---

## The Solution: Karpathy's LLM Wiki, Applied to Coding

The foundation comes from Andrej Karpathy's [LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — a system where an LLM incrementally builds and maintains a persistent wiki from raw sources.

The core philosophy: **not RAG.** Most LLM + document systems retrieve chunks at query time and re-derive answers from scratch every time. The Karpathy pattern is different — the LLM synthesizes knowledge once at ingest time, maintains cross-references, and keeps the wiki current as an evolving artifact.

As Karpathy puts it: *"Obsidian is the IDE, the LLM is the programmer, the wiki is the codebase."*

I took this pattern and applied it specifically to coding-agent continuity — making the wiki live alongside my projects, referenced automatically from agent instruction files.

---

## The Architecture: 3 Layers

The system has three layers, each serving a different purpose:

### Layer 1: Instructions (`AGENT.md`)

Every project gets an `AGENT.md` file at the root. It's always loaded by the agent automatically. It contains:

- Project overview and architecture diagram
- Key file paths
- Setup commands
- Workflow rules
- References to the memory wiki

This is the project's identity card. The agent reads it first and already knows what it's working with.

Different tools pick it up through their own mechanisms: Claude Code reads `CLAUDE.md` (which points to `AGENT.md`), GitHub Copilot reads `.github/copilot-instructions.md` (same pointer), Codex reads `AGENTS.md`. One source of truth, multiple entry points.

### Layer 2: Workflows (`memory/workflows/`)

Three markdown procedures that agents follow on demand:

- **Ingest** — "Add this knowledge to the wiki." The agent compiles new information into a wiki page, updates the index, adds cross-references. Targets 8–15 files touched per ingest.
- **End Session** — "Wrap up." The agent reviews the session for lessons learned, updates the project wiki page, checks for uncommitted git changes.
- **Query** — "What do we know about X?" The agent reads the index, finds relevant pages, synthesizes an answer with citations.

These are agent-agnostic markdown files. Any tool that can read a file can follow the procedure.

### Layer 3: Memory (`memory/wiki/`)

The accumulated knowledge. This is the actual wiki — it grows over time as the agent ingests information and captures lessons:

- **Projects** — Per-project knowledge (architecture decisions, deployment notes, known issues)
- **Domains** — Technical deep-dives (Azure Identity, FastAPI patterns, MCP protocol)
- **Patterns** — Reusable architecture (retry-with-backoff, identity propagation, meta-tool pattern)
- **Lessons** — Debugging gotchas (Windows encoding, JWT token quirks, deployment pitfalls)

Here's the file structure:

```
~/projects/
├── memory/                  ← Persistent memory (the wiki)
│   ├── schema.md            ← Wiki governance rules
│   ├── index.md             ← Content catalog (agent reads this first)
│   ├── workflows/           ← Ingest, end-session, query
│   └── wiki/
│       ├── projects/        ← Per-project knowledge
│       ├── domains/         ← Technical deep-dives
│       ├── patterns/        ← Reusable patterns
│       └── lessons/         ← Debugging gotchas
├── project-a/               ← AGENT.md references memory/
├── project-b/               ← Same convention
└── project-c/
```

---

## The Proof: Before vs After

Here's what a session start looks like without persistent memory:

```
Agent: "What framework is this project using?"
Agent: "Where are the API routes?"
Agent: "What authentication method?"
Agent: "Any known issues I should be aware of?"
Agent: "What's the deployment process?"
→ 8 questions, 5 minutes wasted, still missing context
```

And with persistent memory:

```
Agent reads AGENT.md
  → Finds: FastAPI, routes in src/api/, Redis cache, Docker deploy

Agent reads memory/wiki/projects/weather-api.md
  → Finds: lessons learned, past decisions, known issues

Agent reads memory/wiki/patterns/retry-with-backoff.md
  → Finds: reusable retry pattern already used in this project

→ 0 questions. Proceeds immediately with full context.
```

The difference is not subtle. The agent goes from "tell me about your project" to "I see the Redis TTL is 5 minutes and the last issue was an encoding bug on Windows — I'll use `encoding='utf-8'` in the subprocess call."

Multiply this across 25 active projects and multiple agent tools. Without memory, that's 25 cold starts. With memory, every session picks up where the last one left off — regardless of which agent I'm using.

---

## Daily Workflow

Three key moments in every session:

**1. Session start** — The agent reads `AGENT.md` and the project's wiki page. It already knows the architecture, past lessons, and active issues. No orientation period.

**2. During work** — When the agent discovers something worth remembering — a tricky deployment step, a dependency version conflict, a useful pattern — I say "ingest this." The agent compiles it into a wiki page, updates the index, adds cross-references.

**3. Session end** — I say "end session." The agent reviews what we did, captures lessons into the wiki, updates the project page, and checks for uncommitted git changes.

The wiki compounds. After two weeks of daily use, the agent knows more about my projects than I can keep in my head. After a month, it's like having a junior engineer who actually remembers every conversation.

The best part: knowledge transfers between agents automatically. I debug an Azure deployment gotcha in Claude Code, the lesson gets ingested into the wiki, and the next day GitHub Copilot already knows about it. No manual syncing, no copy-paste. The wiki is the single source of truth that all agents share.

---

## Agent Compatibility

This system works across tools because it's just markdown files:

| Tool | Entry Point | How It Discovers Memory |
|------|------------|------------------------|
| Claude Code | `CLAUDE.md` → `AGENT.md` | Native file reading |
| GitHub Copilot | `.github/copilot-instructions.md` → `AGENT.md` | Instruction file convention |
| Codex | `AGENTS.md` → `AGENT.md` | Agent instruction standard |
| Cursor | Rules / `.cursorrules` → `AGENT.md` | Custom rules file |

The wiki itself is tool-agnostic. Any agent that can read a markdown file can use it.

---

## Security Note

A quick but important note on what goes in the wiki:

- **Do:** Store patterns, architecture decisions, debugging lessons, workflow summaries
- **Don't:** Store secrets, PII, proprietary code, or raw client data
- Use `.gitignore` for sensitive paths
- The wiki is local-first — you control what's in it and where it goes

Store summaries and patterns, not raw data. If you need to reference a client project, use sanitized descriptions. The whole point is to capture reusable knowledge — the kind of thing you'd put in a team wiki — not sensitive specifics.

---

## What's Not Novel (and What Is)

I want to be honest about what's new here and what isn't:

**Not new:**
- The Karpathy LLM Wiki pattern — full credit to [Andrej Karpathy](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- `AGENTS.md` / instruction files — emerging as an [open standard](https://github.com/anthropics/claude-code/blob/main/AGENTS.md) across the industry
- Dynamic memory systems exist: [Mem0](https://github.com/mem0ai/mem0), [Letta/MemGPT](https://github.com/letta-ai/letta), [Graphiti](https://github.com/getzep/graphiti)

**What IS novel:**
- Applying the Karpathy wiki pattern specifically to **coding-agent session continuity**
- Packaging it as a cross-agent system that works with Claude Code, Copilot, Codex, and Cursor simultaneously
- The `bootstrap.md` approach — a single markdown file that any agent can execute to set up the entire memory system from scratch. Give it to your agent, it creates the full directory structure, schema, workflows, and templates in minutes.
- Reusable workflows (ingest, end-session, query) as agent-agnostic markdown procedures that work identically across tools

---

## Try It

I've open-sourced the full setup as a template repo:

👉 **[github.com/ozgurkarahan/ai-agent-memory](https://github.com/ozgurkarahan/ai-agent-memory)**

Two ways to get started:

1. **Fork the repo** — Clone it, explore the demo project, adapt the structure to your workflow.

2. **Use `bootstrap.md`** — Download the single bootstrap file and give it to your AI coding agent in any project folder. The agent will create the entire memory system from scratch. It works with any AI coding agent.

---

## Over to You

How do you handle persistent context across AI coding sessions? Do you re-explain every time, keep a notes file, or have you built something similar?

I'd love to hear what's working for you — drop a comment or reach out.

---

*Credits: [Andrej Karpathy](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) for the LLM Wiki pattern · [Simon Willison](https://simonwillison.net/) for championing explicit context engineering · The [AGENTS.md](https://github.com/anthropics/claude-code/blob/main/AGENTS.md) open standard · Related projects: [Mem0](https://github.com/mem0ai/mem0), [Letta/MemGPT](https://github.com/letta-ai/letta), [Graphiti](https://github.com/getzep/graphiti), [rohitg00/agentmemory](https://github.com/rohitg00/agentmemory)*

---

*Ozgur Karahan — Solution Engineer at Microsoft. I use AI coding agents daily across 25+ active projects. This article reflects my personal workflow, not Microsoft's position.*
