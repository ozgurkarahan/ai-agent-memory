---
applyTo: "**"
---

# Review Sessions

When the user says **"review sessions"**, **"session review"**, or invokes `/review-sessions`, analyse Claude Code session JSONL data to identify workflow improvements, prompt-quality patterns, error trends, and security hygiene issues.

## Arguments

Pass CLI arguments directly:
- `--all` — review every session
- `--project SLUG` — filter by project
- `--since YYYY-MM-DD` — date filtering
- (no args) — incremental, only new sessions since the last review

## Step 1: Run the extraction script

```powershell
python ~/projects/memory/scripts/review-sessions.py $ARGUMENTS
```

If the script errors, diagnose and report. Do not proceed.

## Step 2: Handle "nothing new"

If the output contains `"status": "nothing_new"`, report:
- When the last review was performed
- How many total sessions are available
- Suggest running with `--all` if the user wants a full review

Stop here — do not generate a report.

## Step 3: Interpret the findings

Analyse the JSON output across all 6 dimensions. For each, provide:
- **Key findings** — cite specific numbers and examples, not just summaries
- **What's working well** — positive patterns to reinforce
- **Areas for improvement** — specific, actionable suggestions

### Dimensions

1. **Workflow efficiency** — session lengths, turn durations, restart frequency, plan-mode adoption
2. **Prompt quality** — average length, vague prompts (cite examples), correction rate, multi-intent prompts
3. **Error patterns** — error rate, retry loops (cite specifics), most common errors, "file not read" errors
4. **Tool usage** — most/least used tools, subagent adoption, Write vs Edit ratio, task management adoption
5. **Security hygiene** — any secrets detected (cite masked values), bypass-permissions rate
6. **Session patterns** — peak hours, busiest days, project distribution, knowledge capture rate

## Step 4: Build the recommendation table

| Priority | Finding | Recommendation | Effort |
|----------|---------|----------------|--------|
| HIGH | ... | ... | Low/Medium/High |
| MEDIUM | ... | ... | ... |
| LOW | ... | ... | ... |

Rules:
- HIGH = security issues, frequent errors, significant time waste
- MEDIUM = suboptimal patterns with clear improvements
- LOW = nice-to-have optimizations
- Maximum 10 recommendations

## Step 5: Save the full report

Save to `ops/orchestrator/review-reports/YYYY-MM-DD.md` (memory's ops folder, not a per-project location).

Format:

```markdown
# Session Review Report — YYYY-MM-DD

## Executive Summary
[Top 3 findings in bullet points]

## Metrics Overview
[Key numbers: sessions processed, total turns, avg turn duration, error rate, etc.]

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

Update `ops/orchestrator/review-state.json`:
1. Set `watermark.last_review_date` to today's ISO date
2. Append all processed file IDs to `watermark.reviewed_files` (from `meta.processed_file_ids` in the JSON output)
3. Append a trend snapshot to `trend_snapshots`:
   ```json
   {
     "date": "YYYY-MM-DD",
     "sessions_reviewed": N,
     "error_rate": X.XXX,
     "correction_rate": X.XXX,
     "plan_mode_rate": X.XXX,
     "subagent_rate": X.XXX,
     "avg_turn_duration_ms": N,
     "secrets_detected": N
   }
   ```

> **Note (post-2026-05-11 migration):** the legacy `~/projects/Orchestrator/.claude/docs/review-state.json` watermark was NOT migrated. The first run after migration will re-process all available sessions once (one-time cost), then incremental works as before. See `wiki/lessons/internal-migration-lesson.md`.

## Step 7: Knowledge graduation

If any finding is cross-cutting (applies beyond one project), update the relevant page under `wiki/lessons/`, `wiki/patterns/`, or `agent-config/knowledge/`.

## Step 8: Show results

Display to the user:
1. **Executive summary** — top 3 findings
2. **Recommendation table** — full table
3. **Report path** — where the full report was saved
4. **Trend deltas** — if previous snapshots exist, show key metric changes (arrows: up/down/stable)
