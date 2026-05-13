---
title: Wiki Schema
category: meta
date_created: 2026-04-06
date_updated: 2026-04-30
---

# Wiki Schema

This document governs how the wiki is structured. It is the "AGENT.md of the wiki" — the LLM reads this to understand conventions, categories, and workflows.

## Category Taxonomy

| Category | Folder | Description | Example Pages |
|----------|--------|-------------|---------------|
| Clients | `wiki/clients/` | Per-customer hub pages: profile, MS team, customer contacts, project backlinks | `acme`, `fabrikam`, `contoso` |
| Projects | `wiki/projects/` | Per-project knowledge: architecture, lessons, technical reference | `receipt-agent`, `orchestrator` |
| Domains | `wiki/domains/` | Technical domain deep-dives | `azure-identity`, `salesforce`, `mcp-servers` |
| Patterns | `wiki/patterns/` | Reusable architecture & design patterns | `async-pipelines`, `agent-conventions` |
| Skills | `wiki/skills/` | Executable AI workflows, slash commands, triggerable procedures, and skill shims. Primary question: "what should the assistant do when invoked?" | `end-session`, `ingest`, `query`, `plan-week` |
| Agents | `wiki/agents/` | Role-based executors, subagents, agent personas, hosted agents, and delegation contracts. Primary question: "who/what actor executes this work?" | `code-review`, `explore`, `foundry-prompt-agent` |
| Lessons | `wiki/lessons/` | Consolidated debugging history & gotchas | `windows-dev`, `encoding-gotchas` |
| Tools | `wiki/tools/` | External products, CLIs, services, SDKs, and utilities. Workflows only live here when the page's subject is the tool itself. | `docker`, `markitdown`, `gh-copilot-cli` |
| Meetings | `wiki/meetings/` | Recurring meeting hubs and rolling meeting logs | `br-personal`, `contoso-weekly-team` |
| Career | `wiki/career/` | Professional goals, BR/career artefacts, and priority planning not better represented as meeting logs | `goals`, `2026-q2-priorities` |
| Microsoft | `wiki/microsoft/` | MS-internal context: my Microsoft colleagues (manager, peers, account-team contacts), MS-specific processes, MS account-team structures. **Scope rule:** Microsoft employees / MS-internal entities only — customer and partner contacts stay tabular under [[clients]] hub pages. | `colleagues/colleague-a`, `colleagues/colleague-b` |
| Personal | `wiki/personal/` | Health, reading, journal, personal goals | `reading/sapiens`, `journal/2026-04-06` |
| Queries | `wiki/_queries/` | Durable answers synthesized from the wiki when a query result is worth preserving | `token-usage-weekly-method` |
| Ops | `ops/` | Weekly operating rhythm, activity events, and time-series feeds. Not general knowledge pages. | `weekly/2026-W19`, `activity.jsonl`, `copilot-token-usage.jsonl` |
| Agent Config | `agent-config/` | Cross-project AI agent configuration | `workflow`, `platform`, `knowledge/*` |

## Article Format

Every wiki page has YAML frontmatter + markdown body:

```markdown
---
title: Page Title
category: meta|agent-config|clients|projects|domains|patterns|skills|agents|lessons|tools|meetings|career|microsoft|personal|queries|ops
tags: [tag1, tag2, tag3]
source_docs: []
source_type: source-backed-summary
sensitivity: internal
system_of_record: memory-wiki
retention: durable
sharing: private
date_created: YYYY-MM-DD
date_updated: YYYY-MM-DD
---

# Page Title

## Summary
One-paragraph overview.

## Content
Main content with [[wikilinks]] to related pages.

## Related
- [[related-page-1]]
- [[related-page-2]]

## Sources
- Source documents, URLs, or references
```

## Naming Conventions

- **File names**: lowercase, hyphenated (`azure-identity.md`, not `Azure Identity.md`)
- **Folders**: lowercase, hyphenated
- **Category in frontmatter**, not in path (allows migration without renaming)
- **Derive filename from content**, not from LLM-generated titles (deterministic)

### Client-folder rule for `wiki/projects/` (adopted 2026-05-13)

Project pages tied to a specific top-level client live under `wiki/projects/{client-folder}/` instead of using a client-prefixed flat slug. Current client folders: `acme/`, `fabrikam/`, `contoso/`, `northwind/`. Non-client / personal / generic project pages stay flat at `wiki/projects/`.

**Slug-strip rule:** when moving a flat client-prefixed page into its client folder, **strip the client prefix only when the basename has a unique identifying token** (codename, sub-affiliate, dated event, distinctive compound). **Keep the prefix when the basename is generic** and could apply to multiple clients.

| Example old slug | Decision | Why |
|---|---|---|
| `acme-alpha-rfi` → `acme/alpha-rfi` | strip | `alpha` is a codename |
| `acme-beta-ai-ml-model-building` → `acme/beta-ai-ml-model-building` | strip | `beta` is a sub-affiliate |
| `acme-account` → `acme/acme-account` | **keep** | `account` is generic across clients |
| `contoso-account-plan` + `fabrikam-account-plan` | **keep both** | collision: would both reduce to `account-plan` |
| `acme-business-review-20260417` → `acme/business-review-20260417` | strip | dated event |
| `acme-contract-renewal` → `acme/acme-contract-renewal` | **keep** | every client has contracts |

Wikilinks resolve by basename (`Pages are resolved by filename (shortest path in Obsidian)` — see Wikilink Syntax below), so folder placement is transparent to authoring: `[[alpha-rfi]]` works regardless of where the file lives. Collisions across folders are the only failure mode and are addressed by the conservative slug-strip rule above. Sub-affiliate sub-folders (e.g. `acme/beta/`) are intentionally NOT used — flat per-top-client folders only.

The migration that introduced this rule is documented in [[internal-reorg-lesson]].

## Wikilink Syntax

- `[[page-name]]` — link to another wiki page
- `[[page-name|Display Text]]` — link with custom display text
- `[[page-name#Section]]` — link to a specific section
- Pages are resolved by filename (shortest path in Obsidian)

## AI Operating Layer Routing

Use these rules when filing assistant-operating knowledge. The classification should follow the primary subject, not the implementation detail:

| Primary subject | Category | Rule |
|---|---|---|
| A triggerable procedure, slash command, command shim, `SKILL.md`, or canonical instruction set | Skills | If the user says a phrase and the assistant must execute a defined workflow, file it under `wiki/skills/`. Example: `end-session` is a skill even though it may run Git or `ingest`. |
| A role-based executor, subagent, agent persona, hosted/cloud agent, or delegation contract | Agents | If the durable knowledge describes an actor with a role, tools, boundaries, and handoff contract, file it under `wiki/agents/`. |
| A product, CLI, SDK, API, external service, or utility used by humans or agents | Tools | If the page answers "how does this tool work?" or "how do I use this CLI/service?", file it under `wiki/tools/`. |
| A reusable design, architecture, or authoring technique independent of one named skill/agent | Patterns | If the knowledge generalizes across skills, agents, or projects, file it as a pattern. Example: `thin-skill-shim` is a pattern; `end-session` is the skill. |
| Global preferences/rules loaded into assistants | Agent Config | If the content changes assistant behavior across all projects but is not a queryable wiki article, keep it in `agent-config/` and link from wiki pages when durable. |
| Time-bounded planning, activity, or telemetry streams | Ops | If the artifact is a weekly plan, activity event, or graph feed, keep it in `ops/`. Promote only durable lessons back into wiki pages. |

When a concept has multiple surfaces, keep one canonical page in the category that owns the concept and list the other surfaces in an "Implementation surfaces" table. Do not bury skills under Tools merely because a command uses a tool.

## Entity Registry

Canonical names for frequently referenced entities (use these consistently):

| Entity | Canonical Name | Aliases |
|--------|---------------|---------|
| Azure AI Foundry | `Foundry` | AI Foundry, Azure AI |
| Microsoft Entra ID | `Entra ID` | Azure AD, AAD |
| Model Context Protocol | `MCP` | Model Context Protocol |
| Claude Code | `Claude Code` | claude-code |
| GitHub Copilot | `GH Copilot` | Copilot, GitHub Copilot |

*This registry grows as the wiki grows.*

## Source Classification Fields

These optional frontmatter fields make memory routing and data handling explicit. Historical pages do not need to be backfilled immediately, but new or materially updated pages should use them when sensitivity or system-of-record boundaries matter.

| Field | Allowed values | Meaning |
|---|---|---|
| `source_type` | `source-backed-summary`, `policy`, `meeting`, `conversation`, `web-research`, `code`, `legacy-provenance` | What kind of source or synthesis produced the page |
| `sensitivity` | `public`, `internal`, `personal`, `customer-confidential`, `confidential`, `restricted` | Highest sensitivity level of the page content |
| `system_of_record` | `memory-wiki`, `raw-source`, `m365-query`, `foundry-memory`, `session-store`, `git-repo`, `external-system` | Where the authoritative truth lives |
| `retention` | `durable`, `project-lifetime`, `session`, `ephemeral`, `external-retained`, `delete-on-request` | Expected retention behavior |
| `sharing` | `private`, `team`, `org`, `public`, `customer-approved`, `do-not-share` | Intended sharing boundary |

## Index Files

- **`index.md`** (root) — master content catalog, grouped by category, with counts and one-line summaries
- **`wiki/{category}/_index.md`** — per-category index for every `wiki/` subdirectory; the lint gate checks these exist
- The LLM updates indexes on every ingest

## Log Format

`log.md` is append-only. Each entry:

```markdown
- **YYYY-MM-DDTHH:MM** | ACTION | "Title" | details
```

Actions: `INGEST`, `QUERY`, `LINT`, `UPDATE`, `CREATE`, `SEED`, `SCHEMA-FIX`

## When to Create a New Page vs Update Existing

- **New page**: new entity, new project, new concept not covered anywhere
- **Update existing**: new information about an existing entity, correction, additional detail
- **Consolidate**: if 3+ pages cover overlapping topics, merge into one and redirect

## Quality Rules

- Every page must have frontmatter with at least: title, category, date_created
- Every page should have at least one `[[wikilink]]` to another page (no orphans)
- Contradictions between pages must be flagged and resolved
- Source documents must be cited when information comes from external sources; for non-meta wiki pages, each `source_docs:` entry must point to an existing immutable file under `raw/`
- **No speculation**: pages must be source-backed. No "likely", "probably", "planned". If a project has no source docs, mark it as a `stub` (add `stub` to tags) with a `> ⚠️ Stub` callout
- **Overlapping pages must disambiguate**: when two pages cover related topics (e.g., `azure-identity` vs `entra-id`), each must have a scope note at the top pointing to the other
- **Glossary links must point to canonical pages**: always link to the most specific page (e.g., `[[bicep]]` not `[[azure-identity]]` for Bicep)
