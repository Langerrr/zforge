---
description: Autonomous multi-phase feature execution
argument-hint: [feature-name]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, Agent, SendMessage, AskUserQuestion
---

<!-- Bash is unrestricted rather than filtered: acceptance means re-running each phase's own
     verification commands, which vary per project and are named by the plan rather than known
     here. A filtered allowlist would make the acceptance bar unenforceable. -->


# /feature-orchestrate — Autonomous Feature Execution

Run a feature plan to completion without blocking on the user. Phases execute as background subagents; decisions are recorded for asynchronous review; the planner accepts each phase by re-running its evidence.

Load the `feature-execution` skill. It owns phase state, the spawn contract, recovery, scheduling, and acceptance. This command supplies the autonomous intent only.

## Arguments

- `$1`: Feature name (snake_case, or will be converted)

## Pre-flight

1. Convert the feature name to snake_case and resolve `docs/{feature_name}/`. If the directory is missing, report it and suggest `/zforge:plan`.
2. Read `05_progress_overview.md`, `01_context.md`, `02_plan.md`, and the Doc Map in `01_context.md` for anything else binding.
3. Read `decision_review.md`. If it does not exist, create it from `${CLAUDE_PLUGIN_ROOT}/templates/decision_review.md`.
4. Read `session_log.md`, creating it from `${CLAUDE_PLUGIN_ROOT}/templates/session_log.md` if absent, and append a row for this session.
5. Note any open standing flags in the overview. A flag opened by an earlier session is inherited by this one.

**If the feature predates v3** — phase files with no `## Evidence Required` table — say so once, treat every phase's evidence as E0, and offer to backfill the Verification Matrix in `02_plan.md` before executing. Executing without it is allowed; it just means acceptance can only check that commands run, not that they were the right class.

## Run loop

1. Classify every phase. Pick what to run using the skill's scheduling rules — sequential unless dependencies, collision surfaces and token budget all permit otherwise.
2. Spawn READY phases per the skill's spawn contract.
3. Handle each report by its status. Completion arrives natively; do not poll.
4. Accept COMPLETED phases per the skill's acceptance procedure — re-run the evidence commands before marking anything complete.
5. Repeat until no phase is READY.

## Autonomy boundary

Run without stopping. Two things stop the loop:

- **A pause trigger fires** — the agent hit one of the five forks in its contract and stopped. Answer it from the plan if the plan resolves it; ask the user only if it does not.
- **A phase FAILS** — stop and surface it. Do not attempt a third variation of a failing approach autonomously.

Everything else is recorded and the run continues. Decisions the agents made land in `decision_review.md` as 🟡 for the user to review whenever they choose; they do not block later phases.

## Completion

Follow the skill's completion bookkeeping. Report phases completed, evidence achieved against evidence planned, the count of 🟡 decisions awaiting review, and every standing flag still open.
