# {Feature Name} - Progress Overview

> Last updated: {DATE}
> Status: Not Started
> **Owner: Planner only** — implementation agents do NOT write to this file

---

## Phase Summary

Status is one of PENDING · READY · WAITING · RUNNING · REPORTED · PAUSED · INTERRUPTED · FAILED · COMPLETED.
A phase reaches COMPLETED only through acceptance — the planner re-running its evidence commands. REPORTED is the state in between: an agent reported DONE and the evidence has not been re-run.

| Phase | Name | Status | Evidence achieved | Progress File |
|-------|------|--------|-------------------|---------------|
| 1 | {Phase 1 Name} | PENDING | | `05_progress/05_01_{phase_name}.md` |
| 2 | {Phase 2 Name} | PENDING | | `05_progress/05_02_{phase_name}.md` |

---

## Standing Flags

Declared-but-undischarged verification, rolled up at each acceptance and visible until closed.

**The feature is not complete while a flag is open.** Closing one requires naming the evidence that closed it — a flag is not discharged by the run ending, or by later phases succeeding.

`Kind` is `inward` or `OUTWARD`. An inward flag closes on evidence from this feature. An `OUTWARD` flag is an obligation this feature found and cannot discharge — a surface nothing reaches, that no decision chose and no later phase here owns. It closes when it has been written into the document this project's planners read, with that path cited.

| # | Opened | Unmet | Kind | Risk if it stays open | Closes when | Status |
|---|--------|-------|------|----------------------|-------------|--------|
| SF1 | Phase {N} | {class and scope} | inward | {what ships broken} | {the evidence that would close it} | OPEN |
| SF2 | Phase {N} | {the surface nothing reaches, and that no decision chose it} | OUTWARD | {the journey step that stays unreachable} | {the document a planner reads, cited by path} | OPEN |

---

## Quick Status

| Metric | Count |
|--------|-------|
| Total Phases | {N} |
| Completed | 0 |
| Running | 0 |
| Open standing flags | 0 |
| 🟡 decisions awaiting review | 0 |

---

## Session Log (All Phases)

| Date | Session | Phase | Summary |
|------|---------|-------|---------|

---

## Files Modified (All Phases)

| File | Phase | Status |
|------|-------|--------|

---

## Notes

- Plan created by /zforge:plan on {DATE}
