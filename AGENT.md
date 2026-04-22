# AI Agent Memory

## Overview

This is a demo repo showing the Karpathy LLM Wiki pattern for persistent AI coding agent memory. It provides a practical, git-native approach to giving AI agents (Claude Code, GitHub Copilot, Codex, Cursor) long-term memory across sessions using a local wiki of markdown files.

All demo content is fictional — no client data, no personal information.

## Key Paths

| Path | Description |
|------|-------------|
| `memory/` | The LLM Wiki — agent config, wiki pages, glossary, logs |
| `project-template/` | Starter files for onboarding a new project |
| `demo-project/` | A fictional project demonstrating the pattern end-to-end |
| `docs/` | Guides, tutorials, and reference documentation |
| `bootstrap.md` | Quick-start guide for setting up memory in a new project |

## Conventions

- All demo content uses fictional projects, people, and data.
- No client data, credentials, or personal information — ever.
- Keep markdown files concise and scannable.
- Use consistent frontmatter and `[[backlink]]` conventions from `memory/schema.md`.

## Workflow

Read `memory/agent-config/workflow.md` for generic workflow rules that apply across all projects. Key rules:

1. **Plan Before Coding** — For any task with 3+ steps, outline first.
2. **Verify Before Done** — Never mark complete without proving it works.
3. **Learn From Mistakes** — Update lessons-learned after corrections.
4. **No Blind Retries** — Diagnose root cause on failure.
5. **Keep It Simple** — Don't over-engineer.

## What NOT To Do

- Do not add real client data or personal information.
- Do not create files unless necessary — prefer editing existing ones.
- Do not commit secrets or `.env` files.
- Do not skip verification steps.
