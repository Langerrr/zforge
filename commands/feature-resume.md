---
description: Resume implementation on an existing feature, interactively
argument-hint: [feature-name]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, Agent, SendMessage, AskUserQuestion
---

<!-- Bash is unrestricted for the same reason as /feature-orchestrate: this command implements
     phases directly and accepts them by re-running their verification commands. -->


# /feature-resume — Interactive Feature Implementation

Continue a feature plan with the planner implementing in-session and checking in with the user between phases.

Load the `feature-execution` skill. It owns phase state, recovery, and acceptance. This command supplies the interactive intent only.

## Arguments

- `$1`: Feature name (snake_case, or will be converted)

## Pre-flight

Same as `/feature-orchestrate`: resolve the feature directory, read the overview, context, plan, Doc Map, decision ledger and session log, append this session's row, and note inherited standing flags.

Then scan the phase files and report the current state to the user before doing anything: which phases are complete, which is next, what is REPORTED, PAUSED or INTERRUPTED, and which standing flags are open.

## Order of work

1. **REPORTED** — a previous session took a report and never verified it. Run acceptance before anything else; do not resume that phase's agent and do not trust the report.
2. **PAUSED** — answer the question first. Present it with enough context for the user to decide, or resolve it from the plan and say that you did. A `REASON: USAGE_LIMIT_95` pause has no question in it — pick up from the phase's `## Resume Point`.
3. **INTERRUPTED** — resume per the skill's recovery procedure. Re-orient against disk before continuing; the phase may be further along than the checklist claims.
4. **FAILED** — present the error and ask whether to fix, skip, or stop.
5. **READY** — start the next phase in order.

## Executing a phase

The planner implements directly rather than spawning. The phase file's contract still governs:

- Read the phase file and everything in its `## Required Context` before starting.
- Work the checklist, marking items as they complete.
- Record decisions in `## Decisions` as they are made — including the ones settled with the user in conversation, which are otherwise lost when the session ends.
- Fill each `## Evidence Required` row **when its command runs, from the artifact that command wrote** — the command's captured output for an **E** row, the method walked and the referent it was walked against for a **J** row. Name artifacts per run, so a re-run does not overwrite the file an earlier row quotes. Writing rows at the end of the phase, from what the console said, is what makes a correct implementation fail its own acceptance.
- Keep `## Files Created/Modified` current.

The pause triggers still apply. In this mode a trigger is a conversation rather than a stop — raise it, settle it with the user, record it.

## Between phases

Accept the phase per the skill's acceptance procedure: reconcile every row against its artifact, re-execute what a fact forces or judgment selects, compare achieved against required within each axis, settle each shortfall by materiality, write `## Acceptance`, promote the decisions that reach beyond this feature's implementation and the harness facts to `07_harness_conventions.md`, and roll up any material unmet class as a standing flag.

Implementing and accepting in the same context is what this mode trades away: you are checking work you just did, and the tier-1 reconciliation is the part that survives that. Reconcile every figure against the artifact rather than against your memory of running the command — the memory and the artifact are the two things this mode cannot keep independent, and only one of them is on disk. Where a row's claim depends on a clean state, run it from one — a removed build directory, a fresh database — so the check is of the code and not of what the session left lying around.

Then ask the user: continue to the next phase, run `/zforge:review --feature {name}`, or stop.

## Discussion

This command does not maintain `discussion.md` by default — it is an implementation mode, and its record is the phase files and the decision ledger.

When a session genuinely opens design discussion before continuing — a phase turns out to need a decision the plan never made, and settling it takes real conversation — append to `discussion.md` for that stretch, under the same rule that governs planning: nothing new is asked until the last answer is on disk.

## Completion

Follow the skill's completion bookkeeping.
