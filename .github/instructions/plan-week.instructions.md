---
applyTo: "**"
---

# Plan Week

When the user says "plan week", "Monday plan", or "/plan-week":

## Resolve the memory root

Resolve `WIKI_ROOT` using `memory/schema.md`, then `schema.md`, then the pointer in `AGENT.md`. Stop with the missing path if none contains both `schema.md` and `index.md`. All paths below are relative to `WIKI_ROOT`.

1. Resolve active ISO week (TZ Europe/Paris) → `ops/weekly/2026-W{NN}.md`. If missing, create the minimal weekly skeleton defined by the `ingest` skill.
2. Lift carry-over from prior week's `### Seed for W{NN}` block.
3. Find open `- [ ]` todos recursively under `wiki/`, prioritizing pages updated in the last 14 days.
4. Optionally use any connected work-data source available to the agent for the next 7 days of calendar, flagged mail, or open collaboration threads. Skip this step when no such tool is available.
5. Draft `## 🎯 Monday plan` grouped by `### [[topic]]`. Show diff. User confirms.
6. Update `touches: []` frontmatter with topic slugs touched. Bump `date_updated`.

Anti-patterns:
- ❌ Do not write to `ops/activity.jsonl` — planning ≠ work.
- ❌ Do not auto-resolve todos.
- ❌ Topics must be slugs in `index.md` — else group under `### unmapped`.
