---
name: close-week
description: "Close out the working ISO week: aggregate ops/activity.jsonl events, regenerate the activity table between BEGIN/END sentinels, draft Friday review (wins, misses, lessons to graduate, seed for next week), freeze the week file. Trigger: 'close week', 'Friday review', '/close-week'."
---

# Close Week

When the user says "close week", "Friday review", or "/close-week":

## Resolve the memory root

Resolve `WIKI_ROOT` using `memory/schema.md`, then `schema.md`, then the pointer in `AGENT.md`. Stop with the missing path if none contains both `schema.md` and `index.md`. All paths below are relative to `WIKI_ROOT`.

1. Resolve active ISO week (TZ Europe/Paris) → `ops/weekly/2026-W{NN}.md`.
2. **Aggregate** `ops/activity.jsonl` events for that week — group by `topic`, count `touches`, list `days`, find `last`. Sort by touches desc.
3. **Regenerate the activity block** between the sentinels (wholesale replace):
   ```
   <!-- BEGIN GENERATED ACTIVITY -->
   ...table...
   <!-- END GENERATED ACTIVITY -->
   ```
   Wikilink rule: `[[topic]]` only if `resolved: true`; else plain text + `*(unresolved)*`.
4. **Optional connected-source pull** for "what shipped" — sent mail, collaboration decisions, meetings, or modified files. Skip when no work-data tool is available.
5. **Draft Friday review** sections: Wins · Misses · Lessons → graduate (propose ingest targets, don't auto-run) · Seed for W+1 (top-3 carry-over per topic).
6. **Freeze**: `status: closed`, bump `date_updated`, append `log.md` entry: `... CLOSE-WEEK | 2026-W{NN} | events: N | topics: [...] | wins: N | lessons-promoted: N`.
7. **(Optional) Seed W+1** — create `ops/weekly/{next}.md` skeleton.

Anti-patterns:
- ❌ Do not edit outside the sentinels on regenerate.
- ❌ Do not auto-`/ingest` lessons — explicit user confirm per item.
- ❌ Do not reopen a closed week. Late events → current open week with a note.
- ❌ `ops/activity.jsonl` is append-only — never delete events at close.
