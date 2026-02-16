---
description: Show or update progress for a feature
argument-hint: <feature-name>
allowed-tools: Read, Edit, Glob, Grep
model: haiku
---

# /track — Feature Progress Tracking

Show detailed progress for a specific feature and optionally update it.

## Arguments

- `$1`: Feature name (snake_case or will be converted)

## Process

1. Convert feature name to snake_case.
2. Look for `docs/{feature_name}/05_progress_overview.md`. If not found, check other common locations (`{feature_name}/05_progress_overview.md`).
3. If not found, report: "No plan found for '{feature_name}'. Run `/plan {name}` to create one."

4. Read and display:

**From `05_progress_overview.md`:**
- Phase summary table (phase name, status, progress file)
- Active blockers
- Overall completion percentage

**From phase files (`05_progress/05_XX_*.md`):**
- For each phase, show:
  - Checklist completion (X of Y items done)
  - Current status (signal if present)
  - Last session date and summary

5. Format as a clear status report:

```
## {Feature Name} — Progress Report

Overall: {completed}/{total} phases ({percentage}%)

Phase  Name                 Status       Checklist  Last Activity
─────────────────────────────────────────────────────────────────
1      Backend Schema       Complete     5/5        2026-02-08
2      Backend API          In Progress  3/7        2026-02-09
3      Frontend Types       Pending      0/4        —
4      Frontend Pages       Pending      0/6        —

### Active Blockers
- Phase 2: Waiting on DB migration approval

### Recent Activity
- Phase 2, Session 3 (2026-02-09): Implemented CRUD endpoints for users
```

6. If any phase has an uncleared signal (`<!-- AGENT_SIGNAL:PAUSED -->`), highlight the question from `## Questions`.
