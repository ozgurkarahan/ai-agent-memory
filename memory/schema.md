---
title: Wiki Schema
category: meta
date_created: 2026-04-22
date_updated: 2026-04-22
---

# Wiki Schema

> ⚠️ **Demo Data** — This schema is part of a fictional demo wiki illustrating the Karpathy LLM Wiki pattern. Adapt categories and rules to your needs.

## Category Taxonomy

| Category   | Prefix     | Description                                  |
|------------|------------|----------------------------------------------|
| Projects   | `projects` | One page per codebase or engagement           |
| Domains    | `domains`  | Technology or platform knowledge              |
| Patterns   | `patterns` | Reusable solutions and design patterns        |
| Lessons    | `lessons`  | Debugging stories with root cause and rules   |

## Article Format

Every wiki page uses YAML frontmatter followed by a Markdown body:

```markdown
---
title: "Page Title"
category: projects | domains | patterns | lessons
tags: [tag-a, tag-b]
source_docs: ["path/to/source"]
date_created: YYYY-MM-DD
date_updated: YYYY-MM-DD
---

# Page Title

Body content in Markdown. Use [[wikilinks]] to connect pages.
```

## Naming Conventions

- **File names**: lowercase, hyphenated — `retry-with-backoff.md`, `weather-api.md`
- **Directories**: `wiki/projects/`, `wiki/domains/`, `wiki/patterns/`, `wiki/lessons/`
- **No spaces or special characters** in filenames

## Wikilink Syntax

- Basic link: `[[page-name]]` — resolves to `wiki/**/page-name.md`
- Display text: `[[page-name|Display Text]]` — renders as "Display Text"
- Links are relative to the wiki root; category subdirectories are searched automatically

## Quality Rules

1. **Frontmatter required** — every page must have `title`, `category`, `date_created`
2. **No orphans** — every page must be linked from at least one other page or from `index.md`
3. **Cite sources** — reference the session, commit, or document that produced the knowledge
4. **Keep pages focused** — one concept per page; split if a page exceeds ~300 lines
5. **Update timestamps** — set `date_updated` whenever content changes

## Templates

Starter templates live in `templates/`:

- `templates/project.md` — new project wiki page
- `templates/lesson.md` — new lesson page
