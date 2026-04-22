<!-- Article draft — copy to LinkedIn editor -->

# 🧠 How I Gave My AI Coding Agents a Living Memory

I was trying to find a way to share lessons learned across projects and feed them to my different agents — without having to maintain separate config files for each one.

I had tried different approaches. Notes files, per-project instructions, copy-pasting context at the start of every session. Nothing stuck. Then, a few weeks ago, I saw Andrej Karpathy's [LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — the idea that an LLM can incrementally build and maintain a personal wiki from raw sources. Not RAG, not vector search. A living wiki that the LLM itself curates and keeps current.

I decided to use it for my day-to-day work with **GitHub Copilot** — coding, infrastructure, documentation, communication — regardless of which underlying agent Copilot is using (built-in, Claude, Codex, or others). The result is a central markdown wiki that grows with every session and works across all my projects.

Here's what I built, and how it works today.

---

## What I Built

I took Karpathy's pattern and applied it to my daily workflow. The result is a **central markdown wiki** — a `memory/` folder that lives alongside all my projects. Every project points to it. Every agent reads from it. It grows every day.

The wiki holds everything I want my agents to know: platform preferences, workflow conventions, domain knowledge, reusable patterns, and debugging lessons. It's plain markdown, tracked in git, browsable in Obsidian or any editor.

Here's what makes it work: **every project has an `AGENT.md`** at the root that references the wiki. Each agent-specific config file (`.github/copilot-instructions.md` for Copilot, `CLAUDE.md` for Claude Code, etc.) simply redirects to that same `AGENT.md`. Since Copilot's agent mode supports 3rd-party models, a single `.github/copilot-instructions.md` serves every agent in the ecosystem. I configure once, and every agent gets the same context.

```
~/projects/
├── memory/                  ← The wiki (shared by all projects)
│   ├── index.md             ← Content catalog
│   ├── agent-config/        ← Global rules & preferences
│   ├── workflows/           ← Skills: ingest, end-session, query
│   └── wiki/
│       ├── projects/        ← Per-project knowledge
│       ├── domains/         ← Tech deep-dives
│       ├── patterns/        ← Reusable solutions
│       └── lessons/         ← Debugging gotchas
│
├── client-project-a/        ← AGENT.md → memory/
├── client-project-b/        ← AGENT.md → memory/
└── client-project-c/        ← AGENT.md → memory/
```

---

## The 3 Skills

The system runs on three workflows — I think of them as **skills**. They're markdown files in `memory/workflows/` that any agent can follow. You reference them in your agent's instruction file and they become part of the agent's capabilities.

### Skill 1: Ingest

Say **"ingest"** followed by any content — a document, a conversation, an article, a lesson. The agent compiles it into a wiki page, updates the index, adds cross-references and backlinks.

Here's a real example. I say:

> "Ingest: We found that APIM policy rewrites break when header casing changes on the legacy backend. The fix is to normalize headers to lowercase before the rewrite rule."

The agent creates `wiki/lessons/apim-header-casing.md`, updates `index.md`, and links it to the project page and the Azure/APIM domain page. Next time any agent hits an APIM header issue — on any project — the lesson is already there.

### Skill 2: End Session

Say **"end session"** at the end of a coding session. The agent reviews everything that happened — corrections I made, bugs we found, decisions we took — and captures the lessons into the wiki.

This is the most important skill. It's what makes the memory **living**. Every session feeds the wiki. Every mistake becomes a lesson. The next session starts smarter than the last.

### Skill 3: Query

Ask any question. The agent reads `index.md` first, finds relevant pages, synthesizes an answer with citations, and flags knowledge gaps.

### How to Add the Skills

Reference the workflow files in your agent's instruction file. For GitHub Copilot, add this to `.github/copilot-instructions.md`:

```markdown
## Wiki Skills (available in ALL projects)

### Ingest
When the user says "ingest" followed by content, follow the LLM ingestion pipeline at:
`~/projects/memory/workflows/ingest.md`

### End Session
When the user says "end session", follow:
`~/projects/memory/workflows/end-session.md`

### Query
When the user asks a question, check the wiki first:
`~/projects/memory/workflows/query.md`
```

That's it. The agent reads the workflow file and follows the procedure step by step. No plugins, no extensions — just markdown files that the agent treats as instructions. The same approach works with `CLAUDE.md`, `AGENTS.md`, or `.cursor/rules/` — the workflow files are agent-agnostic, though reliability varies by agent.

---

## What Changed

After a few weeks of daily use, the difference was clear. Saved me 5–10 minutes per session in context-setting alone. But the real payoff was cross-project.

When I debug an Azure APIM issue on one client project and call "end session", that lesson gets written to the wiki. The next day, on a completely different project, the agent already knows about it. A retry pattern I refined on project A is available in project B. A deployment gotcha from project C saves me hours on project D.

The wiki doesn't belong to any single project — it belongs to *me*. It's my accumulated knowledge as an engineer, structured in a way that every agent can use. After a couple of months, it's like having an engineering notebook that actively participates in my work.

One thing I learned the hard way: **quality matters at ingest time.** If you let low-quality notes in, you compound bad context too. I treat ingest and end-session as editorial steps, not raw dumping. Periodically, I clean up stale pages and fix summaries that drifted.

---

## What I Store vs What I Don't

Since I work across client projects and use 3rd-party agents, data hygiene is critical.

**What goes into the wiki:**
- ✅ Abstracted patterns and conventions
- ✅ Debugging lessons (root cause + fix, no client-specific details)
- ✅ Architecture decisions (the *why*, not the *what*)
- ✅ Domain knowledge (public technical info)

**What never goes in:**
- ❌ Client-sensitive data or proprietary code
- ❌ API keys, tokens, passwords
- ❌ Internal architecture with real endpoints
- ❌ PII or raw client data

Patterns get generalized before being stored. "Client X's APIM breaks on header casing" becomes "APIM rewrites can break when header casing changes on legacy backends." The lesson is reusable. The specifics stay out.

---

## Before vs After

Before:
> Agent: "What framework?" "Where are the routes?" "What auth method?"
> → 5 minutes wasted. Still missing context.

After:
> Agent reads AGENT.md + wiki → "I see the Redis TTL is 5 minutes and the last issue was an encoding bug on Windows — I'll use `encoding='utf-8'`."
> → Zero questions. Full context from day one.

---

## Try It

I've open-sourced the full setup:

👉 **[github.com/ozgurkarahan/ai-agent-memory](https://github.com/ozgurkarahan/ai-agent-memory)**

### Option 1: Fork the repo

Clone it, explore the demo content, adapt the structure to your workflow. Replace the demo pages with your own projects.

### Option 2: Ask your agent to build it

This is the approach I recommend. You don't need to set anything up manually — **your agent does it for you.**

1. Download [`bootstrap.md`](https://github.com/ozgurkarahan/ai-agent-memory/blob/main/bootstrap.md) from the repo
2. Open your agent (GitHub Copilot, Claude Code, Codex, Cursor — any of them)
3. Say: *"Follow the instructions in bootstrap.md to set up a persistent memory wiki"* and attach the file
4. The agent creates the full directory structure: schema, workflows, templates, and starter content
5. Verify the structure, commit, done

Then, in each of your projects, add a reference to the wiki in your agent's instruction file. For GitHub Copilot, add this to `.github/copilot-instructions.md`:

```markdown
Read these files for full context:
- `AGENT.md` — Project instructions
- `~/projects/memory/agent-config/workflow.md` — Global workflow rules

## Wiki Skills
When the user says "ingest", follow: `~/projects/memory/workflows/ingest.md`
When the user says "end session", follow: `~/projects/memory/workflows/end-session.md`
```

From that point on, your agent has persistent memory and three skills: ingest, end-session, and query. The wiki starts empty and grows with every session.

The core ideas aren't mine — full credit to [Andrej Karpathy](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) for the LLM Wiki pattern, [Simon Willison](https://simonwillison.net/) for championing context engineering, and the [AGENTS.md](https://agents-md.org) open standard. What I did is package it for daily multi-agent, multi-project coding work.

---

If you use Copilot, Claude, or Codex across multiple repos — how are you handling memory today? Notes, prompts, RAG, or something else?

I'd love to hear what's working for you.

---

*Ozgur Karahan — Solution Engineer at Microsoft. I use AI coding agents daily across 25+ active projects. This article reflects my personal workflow, not Microsoft's position.*
