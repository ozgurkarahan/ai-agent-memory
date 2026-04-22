---
title: Platform Preferences
category: meta
date_created: 2026-04-22
date_updated: 2026-04-22
---

# Platform Preferences

> Customize this file for your environment. Replace placeholders with your actual setup.

## Environment

| Setting          | Value                                        |
|------------------|----------------------------------------------|
| OS               | {Your OS — e.g., Windows 11, macOS, Ubuntu}  |
| Shell            | {Your shell — e.g., PowerShell, Bash, Zsh}   |
| Python           | 3.11+ (`python` command)                     |
| Node.js          | 20+ LTS                                      |
| Package manager  | {pip, uv, npm, pnpm — your preference}       |

## Common Settings

### File Encoding
Always use UTF-8 encoding. On Windows, explicitly set encoding in subprocess calls:

```python
subprocess.run(cmd, encoding="utf-8", errors="replace")
```

### Subprocess Safety
- Always capture stderr for debugging
- Set timeouts on long-running commands
- Use `errors="replace"` to handle encoding edge cases on Windows

### Git
- Use `git --no-pager` in automated scripts to avoid interactive output
- Commit messages: imperative mood, 50-char subject line
- Always include relevant co-author trailers when AI-assisted

## Domain Knowledge Index

Cross-project knowledge files live in `agent-config/knowledge/`:

| File             | Topic                                        |
|------------------|----------------------------------------------|
| *(empty)*        | Add knowledge files as your wiki grows       |

To add a knowledge file, create a Markdown file in `agent-config/knowledge/` and add it to this table.
