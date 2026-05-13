---
applyTo: "**"
---

# Sync Projects

When the user says "sync", "sync projects", or "check for drift":

1. Run: `python scripts/sync-projects.py`
2. Review the drift report showing which projects have updated `.ai/` files
3. If the user approves, run: `python scripts/sync-projects.py --update`
4. After sync, check if any updated content should also update domain/pattern/lesson pages
5. Update `log.md` with sync entries
