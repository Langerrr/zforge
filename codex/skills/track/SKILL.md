---
name: track
description: Show one zforge feature's phase progress, evidence gaps, standing flags, and open decisions.
---

# Feature Progress

Show where a feature stands, including what it owes.

## Arguments

- `$1`: Feature name (snake_case or will be converted)

## Process

1. Convert the feature name to snake_case and locate `docs/{feature_name}/05_progress_overview.md`, falling back to `{feature_name}/05_progress_overview.md`.
2. If not found: "No plan found for '{feature_name}'. Run `$zforge:plan {name}` to create one."
3. Read the overview, every phase file, and `decision_review.md`.

Phase status comes from each phase file's `> Status:` header. There are no signals to scan for.

## Report

```
## {Feature Name} — Progress

Phases: {completed}/{total}

Phase  Name                 Status      Checklist  Evidence      Last Activity
──────────────────────────────────────────────────────────────────────────────
1      Backend Schema       COMPLETED   5/5        E2 / E2       2026-02-08
2      Backend API          REPORTED    7/7        E2 / E2 *     2026-02-09
3      Frontend Types       PENDING     0/4        — / E1        —
4      Frontend Pages       PENDING     0/6        — / E4        —
5      Console Vocabulary   PENDING     0/3        — / J2        —

* claimed, not re-run — Phase 2 is REPORTED

### Standing Flags (2 open)
- SF1 (Phase 5): E4 unmet across all UI phases — closes when a browser-executed run passes
- SF3 (Phase 7): live vendor calls deferred to a mock adapter — closes when a token exists

### Decisions awaiting review: 14 🟡
- Most recent: P7.1 — tri-state run status supersedes P2.8

### Open Items
- Phase 2 · question · migration ordering under concurrent writes — unresolved
```

The **Evidence** column reads *achieved / required*, and classes compare within their axis — an `E` row and a `J` row are not ranked against each other. A phase showing `— / E4` has not yet demonstrated the class its plan asked for.

A completed phase showing anything below its requirement resolved that gap one of two ways: a standing flag against it, or reasoning in its `## Acceptance` for why the shortfall was immaterial. Either is an answer. **A shortfall with neither is the finding** — say so, and name the row.

**A REPORTED phase's achieved class is a claim, not a result.** Mark it as unverified rather than counting it, because nobody has re-run it yet.

Lead with what is owed. A feature at 8/8 phases with two open flags is not finished, and the report should not read as though it is.
