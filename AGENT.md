# AI Agent Memory

## Overview

Public demo repo showing the Karpathy LLM Wiki pattern for persistent AI coding agent memory. Provides a practical, git-native approach to giving AI agents (GitHub Copilot, Claude Code, Codex, Cursor) long-term memory across sessions and across projects.

The wiki is agent-agnostic — GitHub Copilot reads `.github/copilot-instructions.md`, which points to `AGENT.md`, which references the central wiki. 3rd-party agents within Copilot (Claude, Codex) share the same instruction file. Knowledge compounds regardless of which agent or project you're working on.

All demo content is fictional — no client data, no personal information.

## Key Paths

| Path | Description |
|------|-------------|
| `memory/` | The demo LLM Wiki — agent config, wiki pages, glossary, logs |
| `project-template/` | Starter files for onboarding a new project |
| `demo-project/` | A fictional project demonstrating the pattern end-to-end |
| `docs/workflows.md` | Human-readable workflows overview |
| `docs/article-llm-wiki-memory.md` | Article draft — LLM Wiki memory system |
| `bootstrap.md` | Single-file starter prompt — give to any agent to set up the system |
| `README.md` | Comprehensive guide for GitHub visitors |

## Conventions

- All demo content uses fictional projects, people, and data — marked with `<!-- DEMO DATA -->`
- No client data, credentials, or personal information — ever
- Use consistent frontmatter and `[[wikilink]]` conventions from `memory/schema.md`

## Workflow Rules

Read `~/projects/memory/agent-config/workflow.md` for global workflow rules. Key rules:

1. **Plan Before Coding** — For any task with 3+ steps, outline first.
2. **Verify Before Done** — Never mark complete without proving it works.
3. **Learn From Mistakes** — Update the project wiki page at `~/projects/memory/wiki/projects/ai-agent-memory.md`.
4. **No Blind Retries** — Diagnose root cause on failure.
5. **Keep It Simple** — Don't over-engineer.

## Reference Documents

| Document | Contents |
|----------|----------|
| `~/projects/memory/wiki/projects/ai-agent-memory.md` | Project wiki page (lessons, decisions) |
| `~/projects/memory/agent-config/workflow.md` | Global workflow rules |
| `~/projects/memory/agent-config/platform.md` | Platform preferences |

## What NOT To Do

- Do not add real client data or personal information
- Do not create files unless necessary — prefer editing existing ones
- Do not commit secrets or `.env` files
- Do not skip verification steps
