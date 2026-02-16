---
description: Show feature plan status for the current workspace
allowed-tools: Bash(find:*), Read, Glob, Grep
model: haiku
---

# /plan-status — Workspace Feature Status

Scan for all feature plans under the **current working directory** and display their status.

## Process

1. Search for all `05_progress_overview.md` files under the current working directory using Glob: `**/docs/*/05_progress_overview.md`

2. For each found file:
   - Extract the feature name from the directory path
   - Read the file and parse the phase summary table
   - Count: total phases, completed, in progress, blocked, pending

3. Display a summary table:

```
Feature Plans in {current_directory}:

  Feature              Status      Progress    Path
  ──────────────────────────────────────────────────────────
  ai_assistant         In Progress 3/5 phases  docs/ai_assistant/
  video_pipeline       Blocked     1/3 phases  docs/video_pipeline/
  api_refactor         Complete    2/2 phases  docs/api_refactor/
```

4. If any features have active blockers, show them below the table.

5. If no `05_progress_overview.md` files are found, report: "No feature plans found under {current_directory}."

## Scope

ONLY look under the current working directory. Do not search parent directories or sibling projects.
