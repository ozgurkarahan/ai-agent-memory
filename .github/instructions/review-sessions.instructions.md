---
applyTo: "**"
---

# Review Sessions

When the user says **"review sessions"**, **"session review"**, or invokes `/review-sessions`, analyse coding-agent session data to identify workflow improvements, prompt-quality patterns, error trends, and security hygiene issues.

Works across both supported agents:

| Agent | Where sessions live | Format |
|---|---|---|
| **GitHub Copilot CLI** | `~/.copilot/session-state/{session-id}/events.jsonl` (+ `plan.md`, `checkpoints/`, `command-history-state.json`) | JSONL event stream — typed events (`session.start`, `session.mode_changed`, `turn.user`, `turn.assistant`, `tool.invoked`, …) with `timestamp`, `id`, `parentId` |
| **Claude Code** | `~/.claude/projects/{project-hash}/{session-id}.jsonl` (+ `~/.claude/history.jsonl`) | JSONL conversation turns — `type: user|assistant|tool_use|tool_result` records with timestamps |

## Resolve the memory root

1. If `memory/schema.md` exists in the current workspace, set `WIKI_ROOT` to `memory/`.
2. Else if `schema.md` exists, set `WIKI_ROOT` to the current directory.
3. Else follow the memory-wiki path in `AGENT.md`.
4. If no folder containing both `schema.md` and `index.md` can be resolved, report the missing path and stop.

All `ops/...` paths below are relative to `WIKI_ROOT`.

## Scope modifiers

Interpret these optional modifiers from the user's request:

- `--agent {copilot,claude,all}` — source to review; default `all`
- `--all` — ignore the watermark and review every session
- `--project SLUG` — match the session `cwd` or git root
- `--since YYYY-MM-DD` — include sessions on or after this date
- No modifiers — incremental review using `ops/review-state.json`

## Step 1: Discover and normalize sessions directly

Use the agent's native file listing, search, JSON/JSONL reading, and reasoning capabilities. **Do not require or create a helper extraction script.**

1. Inventory session files for the selected agent source(s).
2. For incremental mode, read `ops/review-state.json` if it exists and exclude namespaced file IDs already present in `watermark.reviewed_files`. A file ID is `copilot:{absolute-path}` or `claude:{absolute-path}`.
3. Apply project and date filters before reading large files.
4. Read each JSONL file in manageable chunks. Parse each line independently; count and report malformed lines instead of silently discarding them.
5. Normalize records into this common in-memory model:
   - `agent`: `copilot` or `claude`
   - `session_id`, `timestamp`
   - `kind`: `user_turn`, `assistant_turn`, `tool_call`, `tool_result`, `error`, or `mode_change`
   - `text`, `tool_name`, `success`, `duration_ms` when available
6. Copilot mapping: use event `type` values such as `turn.user`, `turn.assistant`, `tool.invoked`, tool completion/error events, and `session.mode_changed`.
7. Claude mapping: use `type: user|assistant` records and nested `tool_use` / `tool_result` content; infer plan-mode changes only when explicitly represented.
8. Keep the processed namespaced file IDs for the state update in Step 6.

## Step 2: Handle "nothing new"

If the filtered inventory contains no unreviewed session files, report:
- When the last review was performed
- How many total sessions are available **per agent**
- Suggest running with `--all` (and optionally `--agent copilot` or `--agent claude`) for a full review

Stop here — do not generate an empty report or change the watermark.

## Step 3: Interpret the findings

Analyse the JSON output across all 6 dimensions. For each, provide:
- **Key findings** — cite specific numbers and examples, not just summaries
- **What's working well** — positive patterns to reinforce
- **Areas for improvement** — specific, actionable suggestions
- **Per-agent split** when behaviour materially differs between Copilot CLI and Claude Code (e.g., plan-mode adoption, subagent usage, error rate)

### Dimensions

1. **Workflow efficiency** — session lengths, turn durations, restart frequency, plan-mode adoption (Copilot: `session.mode_changed` events; Claude: plan-mode toggle in turns)
2. **Prompt quality** — average length, vague prompts (cite examples), correction rate, multi-intent prompts
3. **Error patterns** — error rate, retry loops (cite specifics), most common errors, "file not read" errors, tool failures
4. **Tool usage** — most/least used tools, subagent adoption, Write vs Edit ratio, task-management adoption (TodoWrite / SQL todos)
5. **Security hygiene** — any secrets detected (cite masked values), bypass-permissions rate (Copilot: `--allow-all-tools`; Claude: `--dangerously-skip-permissions`)
6. **Session patterns** — peak hours, busiest days, project distribution, knowledge capture rate (how often `end-session` or `ingest` is invoked)

## Step 4: Build the recommendation table

| Priority | Finding | Recommendation | Effort | Applies to |
|----------|---------|----------------|--------|------------|
| HIGH | ... | ... | Low/Medium/High | copilot / claude / both |
| MEDIUM | ... | ... | ... | ... |
| LOW | ... | ... | ... | ... |

Rules:
- HIGH = security issues, frequent errors, significant time waste
- MEDIUM = suboptimal patterns with clear improvements
- LOW = nice-to-have optimizations
- Maximum 10 recommendations
- Use the **Applies to** column to make agent-specific guidance explicit

## Step 5: Save the full report

Create `ops/review-reports/` if needed and save to `ops/review-reports/YYYY-MM-DD.md`.

Format:

```markdown
# Session Review Report — YYYY-MM-DD

## Executive Summary
[Top 3 findings in bullet points — call out per-agent splits when relevant]

## Metrics Overview
| Metric | Copilot CLI | Claude Code | Combined |
|---|---|---|---|
| Sessions reviewed | ... | ... | ... |
| Total turns | ... | ... | ... |
| Avg turn duration | ... | ... | ... |
| Error rate | ... | ... | ... |
| Plan-mode rate | ... | ... | ... |

## Detailed Analysis

### 1. Workflow Efficiency
### 2. Prompt Quality
### 3. Error Patterns
### 4. Tool Usage
### 5. Security Hygiene
### 6. Session Patterns

## Recommendations
[The prioritized table from Step 4]

## Trend Deltas
[If previous snapshots exist, show changes since last review]
```

## Step 6: Update state

Update `ops/review-state.json`:
1. Set `watermark.last_review_date` to today's ISO date
2. Append the namespaced processed file IDs collected in Step 1 to `watermark.reviewed_files`, deduplicated, so re-processing one agent does not invalidate the other
3. Append a trend snapshot to `trend_snapshots`:
   ```json
   {
     "date": "YYYY-MM-DD",
     "by_agent": {
       "copilot": { "sessions_reviewed": N, "error_rate": X.XXX, "plan_mode_rate": X.XXX, "avg_turn_duration_ms": N },
       "claude":  { "sessions_reviewed": N, "error_rate": X.XXX, "plan_mode_rate": X.XXX, "avg_turn_duration_ms": N }
     },
     "combined": { "sessions_reviewed": N, "correction_rate": X.XXX, "subagent_rate": X.XXX, "secrets_detected": N }
   }
   ```

## Step 7: Knowledge graduation

If any finding is cross-cutting (applies beyond one project), update the relevant page under `wiki/lessons/`, `wiki/patterns/`, or `agent-config/knowledge/`.

## Step 8: Show results

Display to the user:
1. **Executive summary** — top 3 findings (with per-agent annotation when relevant)
2. **Recommendation table** — full table including the **Applies to** column
3. **Report path** — where the full report was saved
4. **Trend deltas** — if previous snapshots exist, show key metric changes per agent (arrows: up/down/stable)
