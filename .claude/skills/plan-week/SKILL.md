---
name: plan-week
description: "Plan the upcoming ISO week: resolve active week (TZ Europe/Paris), lift carry-over from prior week's 'Seed for W+1' block, aggregate open `- [ ]` todos from project + meeting pages, draft a Monday plan grouped by topic. Trigger: 'plan week', 'Monday plan', '/plan-week'."
---

# Plan Week

When the user says "plan week", "Monday plan", or "/plan-week":

1. Resolve active ISO week (TZ Europe/Paris) → `ops/weekly/2026-W{NN}.md`. Create from template if missing.
2. Lift carry-over from prior week's `### Seed for W{NN}` block.
3. Grep open `- [ ]` todos in `wiki/projects/*.md` + `wiki/meetings/*.md` (recent activity, last 14 days).
4. Optional M365-query-tool pull: calendar (next 7 days), unread/flagged mail, open Teams threads.
5. Draft `## 🎯 Monday plan` grouped by `### [[topic]]`. Show diff. User confirms.
6. Update `touches: []` frontmatter with topic slugs touched. Bump `date_updated`.

Anti-patterns:
- ❌ Do not write to `ops/activity.jsonl` — planning ≠ work.
- ❌ Do not auto-resolve todos.
- ❌ Topics must be slugs in `index.md` — else group under `### unmapped`.
