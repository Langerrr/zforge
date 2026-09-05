---
name: template-conventions
description: >
  This skill should be used when the user asks to "plan a feature", "what goes
  in the phase file", "which file owns this", "what evidence class is this",
  "how do I verify a claim no test can settle", "where should this doc go", or
  when writing, reading or updating any zforge feature document under
  docs/{feature}/. Provides the template structure, file ownership rules, the
  two-axis evidence scale for what was executed and what was judged, phase
  states, and naming conventions.
---

# Zforge Template Conventions

Features are documented in `docs/{feature_name}/`, snake_case.

## Core files

Always created by the zforge plan workflow:

| File | Owner | Purpose |
|------|-------|---------|
| `00_design_spec.md` | Planner | Problem, actors, requirements, boundary, acceptance vocabulary |
| `01_context.md` | Planner | Doc Map, key decisions, open questions with owner and method |
| `02_plan.md` | Planner | Technical plan, phase decomposition, Verification Matrix, environment assumptions, invariants |
| `discussion.md` | Planner | Reasoning generated during planning — written while thinking, not after |
| `decision_review.md` | Planner appends · user adjudicates | Decisions made without blocking, awaiting review |
| `05_progress_overview.md` | **Planner only** | Phase status, standing flags |
| `05_progress/05_XX_*.md` | One agent each | Per-phase contract, evidence, decisions, work log |
| `session_log.md` | Planner | Which sessions touched this feature, and how they ended |

Created when the feature needs them, never as empty placeholders:

| File | When |
|------|------|
| Core patterns doc | The feature changes data models, abstractions or architectural patterns. Without it agents follow the checklist and write structurally wrong code |
| `03_integration_summary.md`, `04_integration_plan.md` | The plan spans backend and frontend |
| `07_harness_conventions.md` | A phase learns something about how the project is run and observed that a later phase would otherwise pay for again |
| `05_progress/review.md` | The zforge review workflow has findings |
| `06_post_deployment.md` | At completion |
| `08_configuration.md`, `09_troubleshooting.md` | Config or gotchas emerge |
| `10_`–`12_refactor_*` | The task is a refactoring rather than a new feature |
| `.zforge-retro/*.md` | The zforge retro workflow is invoked |

## Numbering

`00`–`02` and the `05` family have fixed prefixes. **Everything else is named for what it is** and numbered by creation order in whatever slot is free — the name carries the identity, the number only sorts. Register every document in the **Doc Map** in `01_context.md` with its purpose and which phases it binds.

Running ledgers are unnumbered: `discussion.md`, `decision_review.md`, `session_log.md`. Each has a distinct job — reasoning during thinking, decisions settled, what happened when.

## Ownership

1. **`05_progress_overview.md` — planner only.** Implementation agents never write it. This is what prevents contested writes.
2. **Phase files — one agent each.** An agent reads and writes its own phase file and the source files in its declared surface.
3. **`## Acceptance` is planner-owned** even though it lives in the agent's file. The agent fills the *achieved* and *artifact* columns of `## Evidence Required`; the planner writes `## Acceptance` after independently verifying them.
4. **`00_design_spec.md`** is not modified by agents unless the user says so.
5. **`decision_review.md`** — agents record every decision in their phase file's `## Decisions`; at acceptance the planner promotes only the ones **reaching beyond the feature's implementation**. The rest stay in the phase file, where phase agents already read them. The ledger is an adjudication queue for the user, not an index of everything decided.
6. **`07_harness_conventions.md` — planner writes, every phase reads.** Agents record harness facts as `kind: harness` decisions in their own file; the planner promotes them at acceptance and binds the file into later phases' `## Required Context`. At completion the planner graduates the facts still true into the project's conventions document.

## Evidence

Phases declare what class of evidence closes them, and the planner confirms it. See `references/evidence-scale.md` for the classes, how to choose one at plan time, and what happens when achieved falls short of required.

Two axes. **E0–E4** for what was executed, ranked by what each rules out — algorithm errors, integration mismatches, runtime divergence, wiring defects. **J0–J2** for what was judged: a claim no test runner settles, checked by a stated method against a named referent. Classes rank within an axis only; neither substitutes for the other.

The short version: `02_plan.md`'s Verification Matrix declares the classes per phase before work starts, each phase's `## Evidence Required` inherits its row, and acceptance verifies rather than reads — every row reconciled against the artifact it names, and what a fact forces or judgment selects re-executed.

**Rows are written when their commands run, from the artifact each command wrote**, with artifacts named per run so a re-run cannot overwrite the file an earlier row quotes. A figure presented as a measurement appears verbatim in its artifact or the row says it cannot. This is what makes the cheap half of acceptance possible at all.

Artifacts live in `/tmp/zforge/artifacts/{feature}/` — outside every repository, and dropped when the feature closes. A row cites one by its full path. The docs tree carries the finding and the path; the file itself is working state that acceptance reads once.

Where achieved falls short of required, the gap is settled by materiality: a **material** shortfall becomes a standing flag in the overview and the feature is not complete while one is open, and an **immaterial** one is accepted with the reasoning recorded. Two shortfalls are never immaterial — a command that selected nothing and exited 0, and a user-reachable surface nothing reached. The achieved class is recorded as reached either way.

## Reporting

There is no signal protocol. Phase state is the `> Status:` header in the phase file; completion is delivered by the harness. An agent's final report is:

```
STATUS: DONE | PAUSED | FAILED
REASON: <only when PAUSED — the trigger that fired, or USAGE_LIMIT_95>
EVIDENCE: <one line per Evidence Required row>
DECISIONS: <count>
FILES: <count>
OPEN: <count of unresolved Open Items>
```

Everything else belongs in the phase file, which is what survives the session.

Legacy `<!-- AGENT_SIGNAL:... -->` comments in pre-v3 feature directories are inert history.

## Phase file sections

`## Agent Prompt` (authoritative) · `## Required Context` · `## Evidence Required` · `## Environment Assumptions` · `## Checklist` · `## Decisions` · `## Open Items` · `## Files Created/Modified` · `## Session Log` · `## Resume Point` (only when the agent stopped early) · `## Acceptance`

`## Decisions` carries a `kind` column: `design` by default, `harness` for a fact about how the project is run and observed. The planner promotes `design` rows that reach beyond the feature to `decision_review.md`, and `harness` rows to `07_harness_conventions.md`.

`## Open Items` is the single home for anything needing the planner or the user — question, error, blocker, or evidence gap — with a `kind` column distinguishing them.

## Naming

- Feature folders: `snake_case` — `ai_assistant/`
- Phase files: `05_XX_description.md` — `05_01_backend_schema.md`
- Archive: `_archive/{name}__{date}.md`

For the full file tree, ownership matrix, and per-section detail, see `references/full-template.md`.
