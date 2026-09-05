---
name: plan-status
description: Summarize all zforge feature plans, phase counts, and standing flags in the current workspace.
---

# Workspace Feature Status

Scan for all feature plans under the **current working directory** and display their status.

## Process

1. Search for all `05_progress_overview.md` files under the current working directory using Glob: `**/docs/*/05_progress_overview.md`

2. For each found file:
   - Extract the feature name from the directory path
   - Read the file and parse the phase summary table and the **Standing Flags** section
   - Count: total phases, completed, running, pending, and open standing flags

3. Display a summary table:

```
Feature Plans in {current_directory}:

  Feature              Status       Progress    Flags   Path
  ────────────────────────────────────────────────────────────────
  ai_assistant         In Progress  3/5 phases  —       docs/ai_assistant/
  video_pipeline       In Progress  1/3 phases  1 open  docs/video_pipeline/
  api_refactor         Complete     2/2 phases  —       docs/api_refactor/
```

**A feature with every phase complete and an open standing flag is not Complete.** Show it as `Flagged` with the flag count — the whole point of tracking flags is that they survive the run ending.

4. List open standing flags below the table, with the phase that opened each, its kind, and what closes it. Name the `OUTWARD` ones first: an inward flag is a gap this feature can still close, and an `OUTWARD` one is an obligation waiting on a planner who has not read the feature that found it.

5. If no `05_progress_overview.md` files are found, report: "No feature plans found under {current_directory}."

## Scope

ONLY look under the current working directory. Do not search parent directories or sibling projects.
