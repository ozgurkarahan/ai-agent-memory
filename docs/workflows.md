# Workflows

This repo includes three core workflows that agents follow to maintain and use the memory wiki. Each workflow is agent-agnostic — any AI coding agent (Copilot, Claude Code, Cursor, Aider, etc.) can follow them.

## How Agents Discover Workflows

1. The project's `AGENT.md` points to `memory/agent-config/workflow.md` for global rules
2. Agent-specific config files (`.github/copilot-instructions.md`, `CLAUDE.md`) reference `AGENT.md`
3. `AGENT.md` references the wiki at `memory/` for accumulated knowledge
4. The wiki's `memory/workflows/` directory contains the step-by-step procedures below

**GitHub Copilot note:** `.github/copilot-instructions.md` is auto-loaded by Copilot at session start. When using 3rd-party agents within Copilot (Claude, Codex, etc.), they all share the same instruction file — so every agent in the Copilot ecosystem automatically discovers the memory wiki through one config file.

## Core Workflows

### 1. Ingest — Adding Knowledge to the Wiki

**When:** A user says "ingest" followed by content (a document, lesson, conversation, etc.)

**What it does:** Compiles new knowledge into a wiki page, connects it to the graph (backlinks, index, glossary), and preserves the raw source.

**Key rule:** Touch every file required for raw provenance and graph consistency, without padding the change count. The activity event and final report must agree on the exact distinct paths changed.

**Pipeline:** Resolve Root → Gather Context → Classify & Compile → Update Graph → Preserve Raw Source → Lint → Self-Audit → Emit Activity → Report

📄 **Full specification:** [`memory/workflows/ingest.md`](../memory/workflows/ingest.md)

---

### 2. End Session — Capturing Knowledge Before Context Is Lost

**When:** A user says "end session", "wrap up", or "done for today."

**What it does:** Reviews the session for lessons learned, updates the project wiki page, propagates cross-project knowledge, and checks for uncommitted git changes.

**5 Steps:** Capture Lessons → Cross-Project Knowledge → Update Log → Git Check → Summary

📄 **Full specification:** [`memory/workflows/end-session.md`](../memory/workflows/end-session.md)

---

### 3. Query — Answering Questions from the Wiki

**When:** A user asks a question that might be answered by project context, past decisions, known patterns, or debugging lessons.

**What it does:** Searches the wiki index, reads relevant pages, synthesizes an answer with `[[wikilink]]` citations, and flags knowledge gaps for future ingest.

**4 Steps:** Read Index → Read Pages → Synthesize Answer → Note Gaps

📄 **Full specification:** [`memory/workflows/query.md`](../memory/workflows/query.md)
