---
title: Windows Subprocess Encoding
category: lessons
tags: [windows, python, subprocess, encoding, utf-8]
source_docs: []
date_created: 2026-04-12
date_updated: 2026-04-12
---

# Windows Subprocess Encoding

## Summary

On Windows, Python's `subprocess.run()` defaults to the system's ANSI code page (usually `cp1252`), not UTF-8. This causes `UnicodeDecodeError` or garbled output when subprocess output contains non-ASCII characters (accented names, emoji, Asian characters).

## What Happened

In [[partner-onboarding]], an Azure CLI command (`az ad app create`) returned a JSON response containing a partner name with accented characters ("Café Solutions GmbH"). The Python script crashed with:

```
UnicodeDecodeError: 'charmap' codec can't decode byte 0x82 in position 47
```

This only happened on Windows. The same script worked fine on macOS and Linux, where the default encoding is UTF-8.

## The Fix

Always specify `encoding='utf-8'` when calling `subprocess.run()` on any platform:

```python
# ❌ BAD — uses system default encoding (cp1252 on Windows)
result = subprocess.run(["az", "ad", "app", "create", ...], capture_output=True, text=True)

# ✅ GOOD — explicit UTF-8 everywhere
result = subprocess.run(["az", "ad", "app", "create", ...], capture_output=True, encoding="utf-8")
```

Also set the environment variable as a belt-and-suspenders approach:

```python
import os
os.environ["PYTHONUTF8"] = "1"
```

Or run Python with the `-X utf8` flag.

## Rules

1. **Always use `encoding='utf-8'`** in `subprocess.run()`, `Popen()`, and `check_output()`
2. **Never rely on `text=True` alone** — it uses the system default encoding, which varies by OS
3. **Set `PYTHONUTF8=1`** in your project's environment configuration for defense in depth
4. **Test with non-ASCII data** — include accented characters and emoji in test fixtures to catch encoding issues early

## Scope

This lesson applies to:
- Any Python project running on Windows
- Azure CLI commands that return JSON with user-supplied data
- Git commands that output file names with non-ASCII characters
- Any subprocess that may produce UTF-8 output

## Related

- [[partner-onboarding]] — project where this was discovered
- [[api-auth-debugging]] — similar "environment difference" debugging pattern

<!-- DEMO DATA: This content is fictional, created to demonstrate the wiki structure. -->
