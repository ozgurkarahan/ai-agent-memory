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

## Arguments

Pass CLI arguments directly:
- `--agent {copilot,claude,all}` — which agent's sessions to review. Default: `all`.
- `--all` — review every session
- `--project SLUG` — filter by project (matches the session's `cwd` / git root)
- `--since YYYY-MM-DD` — date filtering
- (no other args) — incremental, only new sessions since the last review

## Step 1: Run the extraction script

```powershell
python ~/projects/memory/scripts/review-sessions.py $ARGUMENTS
```

The script must:
1. Discover session files based on `--agent` (one or both source paths above).
2. Normalize the per-agent schema into a common event model — turn (user / assistant), tool call, error, mode change, timestamp — so the downstream metrics work identically.
3. Tag each session with `agent: "copilot" | "claude"` in the output so the LLM can split findings per agent when relevant.

If the script errors, diagnose and report. Do not proceed.

> **Reference implementation note:** the script that ships alongside this skill in the author's private wiki originally handled Claude JSONL only. Extending it to also parse Copilot CLI `events.jsonl` is a straightforward additive change (new event-type mapping + per-agent path resolver). The skill description here is the agent-agnostic contract — the parser layer is responsible for matching it.

## Step 2: Handle "nothing new"

If the output contains `"status": "nothing_new"`, report:
- When the last review was performed
- How many total sessions are available **per agent**
- Suggest running with `--all` (and optionally `--agent copilot` or `--agent claude`) for a full review

Stop here — do not generate a report.

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

Save to `ops/review-reports/YYYY-MM-DD.md`.

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
2. Append all processed file IDs to `watermark.reviewed_files` (from `meta.processed_file_ids` in the JSON output) — keys namespaced per agent (`copilot:{path}`, `claude:{path}`) so re-processing one agent doesn't invalidate the other
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
