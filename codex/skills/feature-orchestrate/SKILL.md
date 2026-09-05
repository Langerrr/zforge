---
name: feature-orchestrate
description: Execute an existing zforge feature plan autonomously with phase subagents and evidence-based acceptance.
---

# Autonomous Feature Execution

Run a feature plan to completion without blocking on the user. Phases execute as background subagents; decisions are recorded for asynchronous review; the planner accepts each phase by re-running its evidence.

Load `$zforge:feature-execution`. It owns phase state, the spawn contract, recovery, scheduling, and acceptance. This skill supplies the autonomous intent only.

## Arguments

- `$1`: Feature name (snake_case, or will be converted)

## Pre-flight

1. Convert the feature name to snake_case and resolve `docs/{feature_name}/`. If the directory is missing, report it and suggest `$zforge:plan`.
2. Read `05_progress_overview.md`, `01_context.md`, `02_plan.md`, and the Doc Map in `01_context.md` for anything else binding.
3. Read `decision_review.md`. If it does not exist, create it from `../../../templates/decision_review.md`, resolved relative to this `SKILL.md`.
4. Read `session_log.md`, creating it from `../../../templates/session_log.md`, resolved relative to this `SKILL.md`, if absent, and append a row for this session.
5. Note any open standing flags in the overview. A flag opened by an earlier session is inherited by this one.
6. Read `07_harness_conventions.md` if the feature has one. It says how this project is run and observed, and it is what keeps the run from re-learning a fact an earlier phase already paid for.

## Codex goal bridge

When Codex exposes goal tools, make an existing `/goal` the outer run contract without copying its state into zforge's files:

1. After the document pre-flight, call `get_goal`. Record whether this run adopted the active goal and retain the identity and objective fields the tool returns for later comparisons. If no goal is active on this initial check, continue normally and do not create one — invoking this skill is not permission to start or replace a goal.
2. When the run adopted a goal, treat its objective as the outer stopping condition and zforge's feature state as the implementation truth. Re-check the same active goal at each classification boundary before acceptance or delegation, and again immediately before spawning a worker. Apply the goal-budget overlay in `$zforge:feature-execution`.
3. Once a run has adopted a goal, a later check that finds it paused, cleared or replaced schedules no new phase. Preserve any report already delivered using the normal REPORTED checkpoint before yielding. Only a run that never adopted a goal uses normal no-goal scheduling.
4. Low remaining budget is a scheduling signal, never evidence that the feature is complete or blocked.

The bridge owns no second progress ledger: `/goal` answers whether Codex should keep working; the overview, phase files and session log answer what work is accepted, recoverable or open.

**If the feature predates v3** — phase files with no `## Evidence Required` table — say so once, treat every phase's evidence as E0, and offer to backfill the Verification Matrix in `02_plan.md` before executing. Executing without it is allowed; it just means acceptance can only check that commands run, not that they were the right class.

**If any phase is REPORTED** — an earlier session took its report and died before verifying it — acceptance is the first work of this session. Do not resume its agent.

## Run loop

1. Classify every phase. If this run adopted a goal, call `get_goal` now before acceptance or delegation. If the same goal is no longer active, or the runtime reports no remaining capacity, checkpoint any delivered report and yield without starting more work.
2. Accept REPORTED phases before scheduling implementation — reconcile every evidence row against its artifact, re-execute what a fact forces or COST, GAIN and MINIMUM EFFORT select, settle each shortfall by materiality, and commit the accepted phase as `zforge({feature}): phase {NN} {name}` with `git` directly. Below 15% goal budget, if a REPORTED phase exists, accept exactly one, skip implementation for this wave and return to classification to re-check the goal; if none exists, continue to the skill's single bounded action for this wave. Outside that band, accept every REPORTED phase. On a long chain, delegate the verification to a Codex subagent instructed to use `$zforge:acceptance-agent`, then adjudicate the report it returns; the run's context is the scarce resource, and checking evidence does not need it.
3. Pick what to run using the skill's scheduling rules — sequential unless dependencies, collision surfaces and token budget all permit otherwise. If this run adopted a goal, immediately before spawning, re-check that the same goal is active and that the runtime has not reported exhausted capacity; otherwise yield at the durable checkpoint. Then spawn READY phases per the skill's contract.
4. Handle each report by its status. Completion arrives natively; do not poll. **On arrival, set the phase to REPORTED and log the report before running anything** — that checkpoint is what survives a planner that dies mid-acceptance.
5. Return to classification. Exit to Completion when every phase is COMPLETED and no standing flag is open. If all phases are COMPLETED but a standing flag remains, stop and surface it. If incomplete phases remain but none can run, stop and surface their WAITING, PAUSED or INTERRUPTED conditions. Otherwise begin the next wave. A scheduling wave is one pass from this classification boundary through the bounded acceptance or implementation work selected there.

## Autonomy boundary

Run without stopping while the outer runtime permits work. A paused or cleared goal, or a goal runtime that refuses further work for exhausted capacity, yields at the latest durable checkpoint. The goal event does not invent a phase state, but any report already delivered still transitions from RUNNING to REPORTED and is logged before yielding. Within an active run, two phase conditions stop the loop:

- **A pause trigger fires** — the agent hit one of the five forks in its contract and stopped. Answer it from the plan if the plan resolves it; ask the user only if it does not.
- **A phase FAILS** — stop and surface it. Do not attempt a third variation of a failing approach autonomously.

Everything else is recorded and the run continues. The decisions that reach beyond this feature's implementation land in `decision_review.md` as 🟡 for the user to review whenever they choose; the rest stay in their phase files. Neither blocks a later phase.

A `PAUSED` report carrying `REASON: USAGE_LIMIT_95` is not a fork and needs no answer — the agent stopped on budget and left a `## Resume Point`. Wait for capacity and resume it.

## Completion

Follow the skill's completion bookkeeping. Report phases completed, evidence achieved against evidence planned on both axes, any row accepted below its required class and the reasoning that settled it, the count of 🟡 decisions awaiting review, every standing flag still open with its kind, and what the run cost. The closing commit is not pushed: name the push and `$zforge:review` as what is available next, each with its cost and what it could reopen.

Graduate the unowned absences into the document this project's planners read, then `07_harness_conventions.md` into the project's conventions document, trimmed to the facts still true. Both outlive the feature that paid for them.

When this run adopted an active Codex goal, call `get_goal` again before changing its status. Proceed only when the result confirms that the same adopted goal is still active; if it is paused, cleared, replaced or cannot be matched to the adopted contract, preserve zforge state and yield without any `update_goal` call:

- Call `update_goal` with `complete` only when every phase is COMPLETED, no standing flag is open, and the goal's full stopping condition is satisfied. Zforge completion is necessary but not sufficient when the goal also owns review, shipping or another tail. Include the final usage returned by the goal update in the completion report.
- A phase `FAILED`, an unresolved pause trigger, a permission denial or an unavailable dependency stops the inner zforge loop but does not immediately make the goal blocked. When the same condition has prevented meaningful progress for three consecutive goal turns and no safe in-scope alternative remains, call `update_goal` with `blocked` rather than leaving it active. If a blocked goal is later resumed, start a fresh three-turn blocked audit for the resumed run.
- Never mark a goal complete or blocked merely because its remaining budget is low. Do not pause, resume, clear or replace a goal on the user's behalf.
