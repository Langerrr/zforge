# Zforge Template — Full Reference

The complete specification for zforge feature documentation.

## File structure

```
docs/{feature_name}/
├── 00_design_spec.md              # Problem, actors, requirements, boundary, acceptance vocabulary
├── 01_context.md                  # Doc Map, key decisions, open questions with owner + method
├── 02_plan.md                     # Technical plan, phases, Verification Matrix, env assumptions, invariants
├── discussion.md                  # Reasoning captured during planning (unnumbered, append-only)
├── decision_review.md             # Decisions awaiting review (unnumbered, 🟡 → ✅/❌)
├── session_log.md                 # Which sessions touched this feature, and how each ended
├── 05_progress_overview.md        # Phase status + standing flags (PLANNER ONLY)
├── 05_progress/
│   ├── 05_01_{phase_name}.md      # Phase 1
│   ├── 05_XX_{phase_name}.md      # Additional phases
│   └── review.md                  # zforge review findings
├── {NN}_{named_for_what_it_is}.md # Core patterns, UI flows, infra reference — registered in the Doc Map
├── 03_integration_summary.md      # API types → frontend mapping (when the plan spans both)
├── 04_integration_plan.md         # Frontend integration steps
├── 06_post_deployment.md          # Smoke checks, deferred items, rollback
├── 07_harness_conventions.md      # How the project is run and observed (planner writes, phases read)
├── 08_configuration.md            # Env vars, feature flags, external services
├── 09_troubleshooting.md          # Issues, solutions, debug commands
├── 10_refactor_spec.md            # [Refactoring] Requirements, goals, scope
├── 11_refactor_context.md         # [Refactoring] Current-state audit
├── 12_refactor_plan.md            # [Refactoring] Migration steps
├── .zforge-retro/{session_id}.md  # Plugin eval artifacts (only if zforge retro is invoked)
└── _archive/{name}__{date}.md     # Superseded docs
```

Documents outside the fixed `00`–`02` and `05` set take the next free number and a name that says what they are. The **Doc Map** in `01_context.md` is what makes them findable; a document not in the Doc Map is a document no agent will read.

## Creation timeline

**By the zforge plan workflow:** `00`, `01`, `02`, `discussion.md`, `decision_review.md`, `session_log.md`, `05_progress_overview.md`, one `05_progress/05_XX_*.md` per phase.

The plan workflow writes each of these as its contract group fills, so a blocked item stops the tree at a group boundary rather than blocking everything.

**During implementation, when needed:** the core patterns doc (before the first phase that depends on it — usually written at plan time), `03`/`04` when frontend work begins, `05_progress/review.md` when the zforge review runs, `06` at completion, `07` at the first acceptance that promotes a harness fact, `08` and `09` as config and gotchas emerge.

## Ownership matrix

| File | Read | Write | Rule |
|------|------|-------|------|
| `00_design_spec.md` | All | /plan only | Agents do not modify unless told to |
| `01_context.md` | All | Planner | Doc Map and decisions kept current |
| `02_plan.md` | All | Planner | Updated when scope or the matrix changes |
| `discussion.md` | All | Planner | Append-only, during planning |
| `decision_review.md` | All | Planner appends · user adjudicates | Agents never write it directly |
| `05_progress_overview.md` | All | **Planner only** | Prevents contested writes |
| `05_XX_*.md` | Assigned agent | Assigned agent | One agent per file |
| `05_XX_*.md` → `## Acceptance` | All | **Planner only** | The agent's file, the planner's section |
| `05_progress/review.md` | All | zforge review | Findings citing both document and code |
| `session_log.md` | All | Planner | Includes how each session ended |
| `06`, `08`, `09` | All | Planner | Extracted from phase findings |
| `07_harness_conventions.md` | All | Planner | Promoted from phase `kind: harness` decisions; graduated to the project doc at completion |
| `.zforge-retro/*.md` | All | zforge retro | Created on demand |

## Phase file sections

### `## Agent Prompt`
Authoritative and the only copy. The spawn message points at it and does not restate it. States what to build, the postcondition, and which files are in scope.

### `## Required Context`
`File | Sections | Why`. Bind specific sections, not whole documents. This is what makes an agent write structurally correct code instead of merely checklist-complete code.

### `## Evidence Required`
`Claim | Required | Command / method | Achieved | Artifact`. Required is inherited from the Verification Matrix before the phase runs; achieved and artifact are filled by the agent. Commands must be re-runnable by someone else.

Each row is written **when its command runs, from the artifact that command wrote** — not at session end and not from console scrollback. Artifacts are named per run, so a second run cannot overwrite the file an earlier row quotes. Every figure presented as a measurement appears verbatim in a committed artifact, or the row says it cannot.

### `## Environment Assumptions`
`Assumed by plan | Actual here | Substitution | What it defers`. A substitution with no deferral stated is one nobody will remember to undo.

### `## Checklist`
Actionable items. Marked as they complete.

### `## Decisions`
`Kind | Decision | Why | Alternative rejected | Impact`. Recorded as made. Rationale states why, never who — `not stated` where no reason was given.

Kind is `design` or `harness`. At acceptance the planner promotes `design` rows reaching beyond the feature to `decision_review.md` §C, and `harness` rows — facts about how the project is run and observed — to `07_harness_conventions.md`.

### `## Open Items`
`Kind | What | Raised at | Status / Resolution`. One home for questions, errors, blockers and evidence gaps. Resolved items stay with their resolution.

### `## Files Created/Modified`
`File | Step | Action`.

### `## Session Log`
`Date | Session | Steps | Summary`. One agent execution is one session; several per phase is normal.

### `## Resume Point`
Written by the agent only when it stops before the phase is finished — a pause trigger, or the budget-stop clause at ~95% of usage. What is done, what is half-done, the next concrete action. The resuming agent verifies it against the tree and deletes it once past the point it names. A phase that closes with one still in it did not finish.

### `## Acceptance`
Planner-owned. Which rows were reconciled against their artifacts and which were re-executed, the result, and achieved-versus-required per evidence row.

A row accepted below its required class carries the reasoning that settled it: what the missing class would have ruled out, why the postcondition does not depend on it, and what would make it matter. Also names which `## Decisions` rows were promoted to the ledger and which stayed, which harness facts went to `07_harness_conventions.md`, and any drift between what the phase file specified and what was implemented.

## Phase state

Read from the phase file's `> Status:` header:

`PENDING` · `READY` · `WAITING` · `RUNNING` · `REPORTED` · `PAUSED` · `INTERRUPTED` · `FAILED` · `COMPLETED`

`REPORTED` — an agent has reported DONE and the planner has not re-run the evidence — is the state acceptance runs in. Its recovery rule is its own: **re-run the evidence, do not resume the agent.** The work is on disk; only the verification is missing.

`INTERRUPTED` — an agent killed mid-phase by a usage limit, API error or session end — resumes in the same reachable subagent thread with a mandatory re-orientation against disk, never re-spawned while that thread remains available. `COMPLETED` is only reached through acceptance.

## Naming

| Item | Convention | Example |
|------|-----------|---------|
| Feature folder | `snake_case` | `ai_assistant/` |
| Numbered docs | `NN_name` | `03_core_patterns.md` |
| Phase files | `05_XX_description` | `05_01_backend_schema.md` |
| Archive | `{name}__{date}.md` | `02_plan__2026-01-15.md` |

## When to update which file

| Scenario | File | Who |
|----------|------|-----|
| New requirement | `00_design_spec.md` | User |
| Reasoning behind a design choice | `discussion.md` | Planner, during the conversation |
| Architecture decision | `01_context.md` | Planner |
| Decision made mid-run without blocking | phase `## Decisions` | Agent |
| Decision reaching beyond the feature's implementation | phase `## Decisions` → `decision_review.md` §C | Agent, then planner at acceptance |
| Agent stopped before the phase finished | phase `## Resume Point` | Agent |
| Scope change | `01_context.md` + `02_plan.md` | Planner |
| Step completed | own `05_XX_*.md` | Agent |
| Evidence fell short of its class, materially | phase `## Open Items` → overview Standing Flags | Agent, then planner |
| Evidence fell short of its class, immaterially | phase `## Acceptance`, with the reasoning | Agent records the class, planner settles it |
| A fact about how the project is run and observed | phase `## Decisions` (`kind: harness`) → `07_harness_conventions.md` | Agent, then planner at acceptance |
| Harness facts still true at completion | `07_harness_conventions.md` → the project's conventions doc | Planner, trimmed |
| Phase accepted | `## Acceptance` + `05_progress_overview.md` | Planner |
| Ledger contradicted by code | `05_progress/review.md` | zforge review |
| Feature deferred | `06_post_deployment.md` | Planner |
| Doc superseded | `_archive/` | Planner |
