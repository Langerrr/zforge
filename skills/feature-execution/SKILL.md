---
name: feature-execution
description: >
  This skill should be used when the user asks to "orchestrate the feature",
  "run the phases", "resume implementation", "continue the plan", "the phase
  agent died", "the agent stopped on its usage limit", "accept this phase",
  "can these phases run in parallel", or "is this phase done" — and whenever
  the zforge feature-orchestrate or feature-resume workflow executes. Use it as
  well when a phase reported done but its evidence was never re-run, or when a
  long chain is draining the planner's own budget rather than the agents'.
  Provides phase state classification, the subagent spawn contract and its
  budget-stop clause, recovery for interrupted and reported phases, scheduling
  judgment, and the evidence-based acceptance bar that closes a phase —
  including which decisions get promoted to the ledger and which stay put.
---

# Feature Execution

The shared execution model behind `$zforge:feature-orchestrate` and `$zforge:feature-resume`. The two workflows differ only in **who implements** — a spawned agent or the planner in-session — and **where decisions go** — `decision_review.md` or the conversation. Everything below is the same for both.

## Phase state

Phase state is read from the phase file's `> Status:` header and its contents. There is no signal protocol and no PID file.

| State | Meaning |
|---|---|
| PENDING | Not started |
| READY | Dependencies complete, not started |
| WAITING | Dependencies incomplete |
| RUNNING | An agent holds this phase now |
| REPORTED | An agent has reported DONE; the planner has not re-run its evidence |
| COMPLETED | Accepted by the planner |
| PAUSED | Agent hit a pause trigger and stopped |
| FAILED | Unrecoverable error |
| INTERRUPTED | Agent died mid-phase — usage limit, API error, session end |

REPORTED is the state acceptance runs *in*. Nobody holds the phase and nothing has been accepted; the work is on disk and the verification is missing.

## Spawning

One worker per phase. In Codex, spawn a subagent and instruct it to load `$zforge:phase-agent`; applicable skill instructions are allowed to request this delegation. In Claude Code, use the plugin's `zforge:phase-agent` agent type. Both routes use the same phase contract below.

**The phase file is the authoritative prompt.** The spawn message is a pointer to it plus the report contract — never a second copy of the phase's instructions. Two copies drift, and the copy the agent reads wins.

A spawn message contains only:

1. The absolute path to the phase file, with the instruction to read it and its `## Required Context` before anything else.
2. A one-paragraph statement of the phase's postcondition and its required evidence classes.
3. The report contract below.
4. The budget-stop clause below.

Set the phase's `> Status:` to RUNNING before spawning.

### The budget-stop clause

Every spawn message carries it:

> If you reach ~95% of your usage or context budget before the phase is finished, stop cleanly. Flush everything durable into the phase file first — checklist marks, `## Decisions`, `## Files Created/Modified`, `## Open Items`, and a `## Resume Point` naming what is done, what is half-done, and the next concrete action — then report `STATUS: PAUSED` with `REASON: USAGE_LIMIT_95`.

It goes in the spawn message rather than being sent when the limit approaches, because the harness's limit warning arrives at the **planner** and there is no channel to an already-running agent. Carried up front, it converts the most expensive recovery case — INTERRUPTED, resuming from a transcript that may be gone — into the cheapest, which is a resume point on disk.

## The report contract

The agent's final report is the transient channel; the phase file is the durable one. The report carries:

```
STATUS: DONE | PAUSED | FAILED
REASON: <only when PAUSED — the trigger that fired, or USAGE_LIMIT_95>
EVIDENCE: <one line per Evidence Required row — claim, class achieved, artifact>
DECISIONS: <count recorded in ## Decisions>
FILES: <count created/modified>
OPEN: <count of unresolved ## Open Items>
```

Anything longer belongs in the phase file, where it survives the session.

## Recovery

When an agent dies mid-phase, **resume it — do not re-spawn from the phase file.** A re-spawn discards the agent's working context and repeats work that is already on disk.

1. Send a follow-up to the same Codex subagent thread when it is still available.
2. The resume message mandates **re-orientation against disk before any new work**:
   - `git status` and `git diff --stat` — what actually changed
   - re-run the phase's verification commands — what actually passes
   - diff `## Checklist` against what exists in the tree
   - read `## Resume Point` if the agent wrote one
   - Treat memory of prior progress as a hypothesis and the working tree as the fact. Where they disagree, the tree wins.
3. Only when the transcript is gone — a new session, or the agent is unreachable — spawn fresh from the phase file. This is the fallback, not the procedure.

**A REPORTED phase is not resumed.** Its recovery rule runs the other way: do not resume the agent, and do not trust the report — re-run the evidence. Resuming spends an agent's context on a phase it has already finished, and trusting the report skips the only step that closes a phase.

Record usage-limit deaths distinctly in `session_log.md`. They are a budgeting signal, not a defect, and they say the run is asking for more concurrent tokens than it has.

## Failure handling

| Status | Response |
|---|---|
| REPORTED | Run acceptance (below). The agent is finished; do not resume it |
| COMPLETED | Already adjudicated. Advance |
| PAUSED | Answer from the plan if it resolves the question; otherwise ask the user. Resume the same subagent thread with a follow-up |
| PAUSED, `REASON: USAGE_LIMIT_95` | No question to answer. Wait for capacity, then resume the same subagent thread with a follow-up pointed at the phase's `## Resume Point` |
| FAILED | Stop. Surface the phase's `## Open Items` to the user with full context |
| INTERRUPTED | Wait for capacity, then resume the same reachable subagent thread. **Never re-spawn when that thread still exists** — the work is not lost, only paused |
| ORPHANED | The orchestrator session died. On the next session, resume from the phase file plus disk state |

## Scheduling

**Sequential is the default.** Parallelize only when all three hold:

1. **Dependencies allow it** — the plan's dependency edges are disjoint.
2. **Collision surfaces are disjoint** — generated files, route trees, lockfiles, package installs, migrations. Two agents regenerating the same file will silently clobber each other. Where surfaces overlap, keep the phases serial unless the planner explicitly provisions separate Git worktrees before spawning; after merging isolated results, re-run the combined evidence.
3. **The token budget supports it** — concurrent long-running agents drain one shared budget, and each concurrent agent multiplies the odds of a mid-phase usage-limit death. After any INTERRUPTED phase in this run, treat the budget as constrained.

Dependency edges say what *can* run in parallel. These three say what *should*. When parallelizing, state the reason in `session_log.md`.

### The planner's budget is the one that cannot be reset

An agent's cost is per-phase and bounded: it reads a phase file, works, reports five lines, and its context dies with it. The planner's cost is **cumulative across the whole run** — it holds the plan, reads every report, re-runs every evidence command, writes every acceptance section, promotes decisions, updates the overview and session log, and commits. Serialising agents makes the agent side cheaper and does nothing about the planner.

A long chain is therefore a planner-budget question before it is an agent-budget question, and two things follow. Delegate the evidence re-run once the chain is long. Checkpoint on REPORTED rather than after acceptance, because a planner that dies mid-acceptance otherwise leaves a phase whose evidence has been claimed and not checked, with nothing on disk saying so.

## Acceptance

An agent's green report is a claim. Acceptance is the planner's independent confirmation, and it is what closes a phase.

**Checkpoint first.** The moment a report arrives, set `> Status:` to REPORTED and append the report's lines to the phase's `## Session Log`. That is one edit, and it is what makes the rest of this procedure recoverable.

1. Read the phase's `## Evidence Required` table.
2. **Re-run the named commands and re-apply the named methods.** Not the agent's transcript of them — the commands. A J row is re-checked by walking the method the row names.
3. Compare achieved class against required class for every row, **within its axis**:

| Result | Response |
|---|---|
| achieved = required | Accept the row |
| achieved > required | Accept, and note the surplus |
| achieved < required | **Do not accept silently.** Either PAUSE the phase back to the agent, or open a standing flag in `05_progress_overview.md` with a stated *closes when* |

4. Write `## Acceptance` in the phase file: what was re-run, the result, and achieved-versus-required per row. This section is planner-owned; the agent never writes it.
5. **Promote the load-bearing decisions** into `decision_review.md` §C as 🟡, by the criterion below. Name in `## Acceptance` which rows went up and why.
6. Roll any unmet class up to the overview's Standing Flags.
7. Set `> Status:` to COMPLETED and update `05_progress_overview.md`.

A phase whose evidence table is entirely E0 and J0 has demonstrated nothing, regardless of how complete its checklist looks.

### Which decisions get promoted

**A decision is promoted only when it reaches beyond this feature's implementation** — it contradicts or extends a design document, asserts something the domain model does not define, or hands an obligation to a later band. A decision that only binds later phases stays in the phase file, where phase agents already read it.

The ledger is an adjudication queue the user drains asynchronously. A phase routinely records ten or more decisions and most are implementation conventions — which package call, which transport, which pinned version. Promoting all of them makes the ledger a second copy of the progress folder and hands the triage to the user, which is the work the planner was there to do.

The line that settles borderline rows: **a question the user must answer** belongs in the ledger; **a question a later phase will answer** belongs in `## Open Items`, which is the mechanism that carries cross-phase obligations. An interpretation the agent flagged for a later phase to confirm is an open item, however much it reads like ledger material.

### Delegating the re-run

Step 2 is the largest recurring cost on the planner and it needs the least of the planner's context — a phase file and a shell. Where the chain is long or the budget is tight, delegate to the specialized acceptance role: in Codex, instruct a subagent to use `$zforge:acceptance-agent`; in Claude Code, use the plugin's `zforge:acceptance-agent` agent type. Adjudicate the table it returns.

Steps 3 through 7 stay with the planner. Judging whether an achieved class is good enough, writing `## Acceptance`, and deciding what gets promoted are the parts that need the run.

## Completion bookkeeping

A feature is complete when every phase is COMPLETED **and no standing flag is open.** Closing a flag requires naming the evidence that closed it — a flag is not closed by the run ending.

On completion:

1. Final status for all phases in `05_progress_overview.md`.
2. Fill the current session's row in `session_log.md` — phases touched, summary, and any usage-limit interruptions.
3. Report to the user: phases completed, evidence classes achieved against those planned, open 🟡 decisions awaiting review, and any flag that had to be carried.
4. Suggest `$zforge:review` for feature `{name}` to check the implementation against the ledger.

If flags remain open, say so plainly and name them. A feature with an open flag is not finished; it is finished-except-for-a-named-gap, and the difference is the entire point of tracking them.
