---
name: feature-execution
description: >
  This skill should be used when the user asks to "orchestrate the feature",
  "run the phases", "resume implementation", "continue the plan", "the phase
  agent died", "can these phases run in parallel", or "is this phase done" —
  and whenever /zforge:feature-orchestrate or /zforge:feature-resume executes.
  Provides phase state classification, the subagent spawn contract, recovery
  for interrupted phases, scheduling judgment, and the evidence-based
  acceptance bar that closes a phase.
---

# Feature Execution

The shared execution model behind `/feature-orchestrate` and `/feature-resume`. The two commands differ only in **who implements** — a spawned agent or the planner in-session — and **where decisions go** — `decision_review.md` or the conversation. Everything below is the same for both.

## Phase state

Phase state is read from the phase file's `> Status:` header and its contents. There is no signal protocol and no PID file.

| State | Meaning |
|---|---|
| PENDING | Not started |
| READY | Dependencies complete, not started |
| WAITING | Dependencies incomplete |
| RUNNING | An agent holds this phase now |
| COMPLETED | Accepted by the planner |
| PAUSED | Agent hit a pause trigger and stopped |
| FAILED | Unrecoverable error |
| INTERRUPTED | Agent died mid-phase — usage limit, API error, session end |

## Spawning

One agent per phase, `subagent_type: zforge:phase-agent`, `run_in_background: true`.

**The phase file is the authoritative prompt.** The spawn message is a pointer to it plus the report contract — never a second copy of the phase's instructions. Two copies drift, and the copy the agent reads wins.

A spawn message contains only:

1. The absolute path to the phase file, with the instruction to read it and its `## Required Context` before anything else.
2. A one-paragraph statement of the phase's postcondition and its required evidence classes.
3. The report contract below.

Set the phase's `> Status:` to RUNNING before spawning.

## The report contract

The agent's final report is the transient channel; the phase file is the durable one. The report carries:

```
STATUS: DONE | PAUSED | FAILED
EVIDENCE: <one line per Evidence Required row — claim, class achieved, artifact>
DECISIONS: <count recorded in ## Decisions>
FILES: <count created/modified>
OPEN: <count of unresolved ## Open Items>
```

Anything longer belongs in the phase file, where it survives the session.

## Recovery

When an agent dies mid-phase, **resume it — do not re-spawn from the phase file.** A re-spawn discards the agent's working context and repeats work that is already on disk.

1. `SendMessage` to the same agent.
2. The resume message mandates **re-orientation against disk before any new work**:
   - `git status` and `git diff --stat` — what actually changed
   - re-run the phase's verification commands — what actually passes
   - diff `## Checklist` against what exists in the tree
   - Treat memory of prior progress as a hypothesis and the working tree as the fact. Where they disagree, the tree wins.
3. Only when the transcript is gone — a new session, or the agent is unreachable — spawn fresh from the phase file. This is the fallback, not the procedure.

Record usage-limit deaths distinctly in `session_log.md`. They are a budgeting signal, not a defect, and they say the run is asking for more concurrent tokens than it has.

## Failure handling

| Status | Response |
|---|---|
| COMPLETED | Adjudicate evidence (below), then advance |
| PAUSED | Answer from the plan if it resolves the question; otherwise ask the user. Resume via `SendMessage` |
| FAILED | Stop. Surface the phase's `## Open Items` to the user with full context |
| INTERRUPTED | Wait for capacity, then resume via `SendMessage`. **Never re-spawn** — the work is not lost, only paused |
| ORPHANED | The orchestrator session died. On the next session, resume from the phase file plus disk state |

## Scheduling

**Sequential is the default.** Parallelize only when all three hold:

1. **Dependencies allow it** — the plan's dependency edges are disjoint.
2. **Collision surfaces are disjoint** — generated files, route trees, lockfiles, package installs, migrations. Two agents regenerating the same file will silently clobber each other. Where surfaces overlap and parallelism is still wanted, use `isolation: "worktree"` and accept the merge-and-re-verify cost.
3. **The token budget supports it** — concurrent long-running agents drain one shared budget, and each concurrent agent multiplies the odds of a mid-phase usage-limit death. After any INTERRUPTED phase in this run, treat the budget as constrained.

Dependency edges say what *can* run in parallel. These three say what *should*. When parallelizing, state the reason in `session_log.md`.

## Acceptance

An agent's green report is a claim. Acceptance is the planner's independent confirmation, and it is what closes a phase.

1. Read the phase's `## Evidence Required` table.
2. **Re-run the named commands.** Not the agent's transcript of them — the commands.
3. Compare achieved class against required class for every row:

| Result | Response |
|---|---|
| achieved = required | Accept the row |
| achieved > required | Accept, and note the surplus |
| achieved < required | **Do not accept silently.** Either PAUSE the phase back to the agent, or open a standing flag in `05_progress_overview.md` with a stated *closes when* |

4. Write `## Acceptance` in the phase file: what was re-run, the result, and achieved-versus-required per row. This section is planner-owned; the agent never writes it.
5. Promote the phase's `## Decisions` rows into `decision_review.md` §C as 🟡.
6. Roll any unmet class up to the overview's Standing Flags.
7. Set `> Status:` to COMPLETED and update `05_progress_overview.md`.

A phase whose evidence table is entirely E0 has demonstrated nothing, regardless of how complete its checklist looks.

## Completion bookkeeping

A feature is complete when every phase is COMPLETED **and no standing flag is open.** Closing a flag requires naming the evidence that closed it — a flag is not closed by the run ending.

On completion:

1. Final status for all phases in `05_progress_overview.md`.
2. Fill the current session's row in `session_log.md` — phases touched, summary, and any usage-limit interruptions.
3. Report to the user: phases completed, evidence classes achieved against those planned, open 🟡 decisions awaiting review, and any flag that had to be carried.
4. Suggest `/zforge:review --feature {name}` to check the implementation against the ledger.

If flags remain open, say so plainly and name them. A feature with an open flag is not finished; it is finished-except-for-a-named-gap, and the difference is the entire point of tracking them.
