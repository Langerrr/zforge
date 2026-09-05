---
name: feature-execution
description: >
  This skill should be used when the user asks to "orchestrate the feature",
  "run the phases", "resume implementation", "continue the plan", "the phase
  agent died", "the agent stopped on its usage limit", "accept this phase",
  "can these phases run in parallel", "is this phase done", "does this
  shortfall matter", or "should I flag this or accept it" — and whenever the
  zforge feature-orchestrate or feature-resume workflow executes. Use it as
  well when a phase reported done but its evidence was never verified, when a
  phase reached a lower evidence class than its plan required, or when a long
  chain is draining the planner's own budget rather than the agents'.
  Provides phase state classification, the subagent spawn contract and its
  budget-stop clause, recovery for interrupted and reported phases, scheduling
  judgment, and the two-tier acceptance bar that closes a phase — what is
  reconciled against artifacts, what is re-executed, how a shortfall is settled
  by materiality, and which decisions get promoted to the ledger.
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
| REPORTED | An agent has reported DONE; the planner has not verified its evidence |
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

**A REPORTED phase is not resumed.** Its recovery rule runs the other way: do not resume the agent, and do not trust the report — verify the evidence. Resuming spends an agent's context on a phase it has already finished, and trusting the report skips the only step that closes a phase.

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

### Goal-budget overlay

Apply this overlay only when Codex is running `$zforge:feature-orchestrate` under an active goal and `get_goal` exposes both the goal budget and its remainder. Re-check immediately before each scheduling wave and calculate the remaining percentage from the tool's values; when either value is absent, use the ordinary scheduling rules rather than inventing an estimate.

| Remaining | Scheduling response |
|---|---|
| Above 60% | Apply the ordinary dependency, collision and budget gates. Parallelism is eligible, not required. |
| `>30%` through `60%` | Run phases serially. Delegate a costly evidence re-run when doing so protects the planner's cumulative context. |
| 15–30% | Accept REPORTED work first, then recover one INTERRUPTED phase through its next report and acceptance — resume its thread when reachable, otherwise use the disk-first fallback — then schedule at most one READY phase per wave. Delegate the evidence re-run when the acceptance role can verify it from the phase file without reconstructing planner context. Prefer the bounded action that leaves the strongest durable checkpoint. |
| Below 15% | Do no speculative or parallel work. Accept an existing report, finish or checkpoint the held phase, or take one bounded action that materially advances the nearest acceptance condition. Do not idle solely because the budget is low. |

After any usage-limit interruption in the current run, do not parallelize again during that run. Delegated acceptance reduces planner-context pressure but still consumes goal tokens; use it to preserve the scarce planner context, not as a claim that total usage must fall.

The overlay changes ordering and concurrency only. It never changes phase state, lowers an evidence class, skips independent acceptance, or turns budget exhaustion into `COMPLETED`, `PAUSED` or `FAILED`.

If the goal runtime reports no remaining capacity or refuses further work, launch no worker. Preserve the last durable zforge checkpoint and let the goal runtime control continuation; exhausted budget alone does not satisfy the goal's blocked condition.

### The planner's budget is the one that cannot be reset

An agent's cost is per-phase and bounded: it reads a phase file, works, reports five lines, and its context dies with it. The planner's cost is **cumulative across the whole run** — it holds the plan, reads every report, verifies every evidence row, writes every acceptance section, promotes decisions, updates the overview and session log, and commits. Serialising agents makes the agent side cheaper and does nothing about the planner.

A long chain is therefore a planner-budget question before it is an agent-budget question, and two things follow. Delegate the evidence verification once the chain is long. Checkpoint on REPORTED rather than after acceptance, because a planner that dies mid-acceptance otherwise leaves a phase whose evidence has been claimed and not checked, with nothing on disk saying so.

### Holding the run outside the planner's context

The phase files record what happened. What is still *owed* lives only in the planner's context, and that is the part a planner death takes with it. A harness-held completion condition puts it somewhere else.

In Claude Code, `/goal <condition>` sets one: a check after each turn decides whether the condition is met, and Claude keeps working until it is. The goal is restored on `claude --resume`, and `/goal clear` ends it early. One goal is active at a time, so a newly set condition replaces the current one. It needs a trusted workspace and unrestricted hooks. In Codex the equivalent is an active goal exposed through `get_goal`, which also carries a budget — see the goal-budget overlay above.

Four rules govern the pairing:

- **The condition is the feature, not the phase.** One goal is active at a time, so a per-phase condition is replaced at every phase and cannot survive the run.
- **The condition names zforge's own bar** — every phase COMPLETED and no standing flag open — so the harness check and the phase files agree about what finished means.
- **It composes rather than duplicates.** The goal answers whether to keep working; the overview, phase files and session log answer what is accepted, recoverable or open. There is no second progress ledger, and the goal's state is never copied into zforge's files.
- **It is never set implicitly.** Invoking orchestration is not permission to set or replace a goal. Where a run would benefit from one, propose the condition and let the user set it.

What the pairing buys is a planner that can die cheaply: `--resume` restores the goal, the phase files restore the state. It does not shorten acceptance, make an evidence row accurate, or keep a phase agent alive.

## Acceptance

An agent's green report is a claim. Acceptance is the planner's independent confirmation, and it is what closes a phase.

**Checkpoint first.** The moment a report arrives, set `> Status:` to REPORTED and append the report's lines to the phase's `## Session Log`. That is one edit, and it is what makes the rest of this procedure recoverable.

1. Read the phase's `## Evidence Required` table, its `## Environment Assumptions`, and `07_harness_conventions.md` if the feature has one.
2. **Reconcile every row against its artifact** (tier 1, below).
3. **Re-execute what tier 2 selects** (below). A J row is re-checked by walking the method the row names.
4. Compare achieved class against required class for every row, **within its axis**, and settle each shortfall by materiality:

| Result | Response |
|---|---|
| achieved = required | Accept the row |
| achieved > required | Accept, and note the surplus |
| achieved < required, **material** | PAUSE the phase back to the agent, or open a standing flag in `05_progress_overview.md` with a stated *closes when* |
| achieved < required, **immaterial** | Accept the row, recording the gap, why the postcondition does not depend on it, and what would make it matter |

5. Write `## Acceptance` in the phase file: which rows were reconciled and which re-executed, the result, achieved-versus-required per row, and the reasoning behind any row accepted below its class. This section is planner-owned; the agent never writes it.
6. **Promote the load-bearing decisions** into `decision_review.md` §C as 🟡, by the criterion below. Name in `## Acceptance` which rows went up and why.
7. **Promote any harness fact** the phase learned into `07_harness_conventions.md`, so the next phase reads it instead of paying for it again.
8. Roll any material unmet class up to the overview's Standing Flags.
9. Set `> Status:` to COMPLETED and update `05_progress_overview.md`.

The achieved class is recorded as reached. A row that reached E3 against an E4 requirement reads E3 whichever outcome it takes — accepting a gap and hiding it are different acts.

A phase whose evidence table is entirely E0 and J0 has demonstrated nothing, regardless of how complete its checklist looks.

### Tier 1 — reconcile every row

Every row, every time, without running anything:

- Does the row's named artifact exist? Rows cite artifacts by their full path, under `/tmp/zforge/artifacts/{feature}/` — open the file rather than looking for it in the tree.
- Does every figure the row states appear in that artifact verbatim?
- Does the recorded output show a command that **selected nothing** — zero tests matched, zero assertions run, zero results — and exited 0?

This tier is cheap, it needs no project state, and it is where misquoted figures and false greens surface. Run it before deciding what to re-execute, because what it finds is one of the triggers.

### Tier 2 — re-execute what earns it

Re-run a row when a fact forces it:

- Tier 1 found a mismatch, or the artifact is missing or quotes nothing.
- The row names no artifact, only a claim.
- The agent flagged the row itself, in `## Open Items` or by filling achieved below required.
- The claim is about a clean or regenerated state.

Otherwise decide, and think about three things:

- **COST** — what running this takes.
- **GAIN** — which unknown it retires, priced by what being wrong about it would cost.
- **MINIMUM EFFORT** — the smallest thing that retires that same unknown.

A suite re-run against a tree acceptance has not modified retires almost no unknown, and carries its own flake exposure on top. A filtered run against the surface the phase just built retires the unknown that matters, for a fraction of the time. Both can be E4; the class does not separate them, and these three do.

Where the decision is to accept, the artifact stands and the row closes at tier 1.

**Record which check each row got** — `from-artifact` or `re-executed`. A row accepted from its artifact is honestly accepted; a row written up as though a command ran is not.

**Side effects bound what may be re-run.** A command that tears down state other rows depend on — a teardown that removes volumes, a fixture reset, anything `07_harness_conventions.md` names as destructive — is verified from its artifact with the reason stated. Re-running a clean form needs an isolated worktree the planner has provisioned first.

### Materiality, and the floor beneath it

Name what the missing class rules out — `references/evidence-scale.md` states it per class — then ask whether anything downstream in this feature relies on that being ruled out. Nothing does, and no later phase inherits the assumption: the gap is immaterial, and it is recorded rather than flagged. A judgment that takes more than a paragraph to state is material.

Two shortfalls are never immaterial:

1. **A command that selected nothing and exited 0.** It is indistinguishable from a pass and it is not one.
2. **A user-reachable surface that nothing reached the way a user reaches it.** Waiving this is how wiring and delivery defects ship.

Every other row is judged by impact rather than by category, rows touching auth, data mutation and migrations included. Two obligations attach to that judgment: where the implementation drifted from the plan, `## Acceptance` records the drift whatever the impact; and where the impact needs human attention, the row pauses or flags on its own merits.

### Which decisions get promoted

**A decision is promoted only when it reaches beyond this feature's implementation** — it contradicts or extends a design document, asserts something the domain model does not define, or hands an obligation to a later band. A decision that only binds later phases stays in the phase file, where phase agents already read it.

The ledger is an adjudication queue the user drains asynchronously. A phase routinely records ten or more decisions and most are implementation conventions — which package call, which transport, which pinned version. Promoting all of them makes the ledger a second copy of the progress folder and hands the triage to the user, which is the work the planner was there to do.

The line that settles borderline rows: **a question the user must answer** belongs in the ledger; **a question a later phase will answer** belongs in `## Open Items`, which is the mechanism that carries cross-phase obligations. An interpretation the agent flagged for a later phase to confirm is an open item, however much it reads like ledger material.

### Delegating the verification

Steps 2 and 3 are the largest recurring cost on the planner and need the least of the planner's context — a phase file and a shell. Where the chain is long or the budget is tight, delegate to the specialized acceptance role: in Codex, instruct a subagent to use `$zforge:acceptance-agent`; in Claude Code, use the plugin's `zforge:acceptance-agent` agent type.

The agent returns a per-row verdict and an overall recommendation with its rationale. Read the rationale: it comes from the party that watched the commands run, and re-deriving it from the table alone spends planner context to reach a worse-informed version of the same conclusion. Where the recommendation is sound, adopt it and say so. Where it is not, the disagreement is worth stating in `## Acceptance`.

Steps 4 through 9 stay with the planner. Adjudicating materiality, writing `## Acceptance`, and deciding what gets promoted are the parts that need the run.

A tier-1-only pass — reconciliation with no re-execution triggered — is arithmetic against committed files and runs well on a cheaper model. A pass that will re-execute anything needs one that can read a failing runtime.

## Completion bookkeeping

A feature is complete when every phase is COMPLETED **and no standing flag is open.** Closing a flag requires naming the evidence that closed it — a flag is not closed by the run ending.

On completion:

1. Final status for all phases in `05_progress_overview.md`.
2. Fill the current session's row in `session_log.md` — phases touched, summary, and any usage-limit interruptions.
3. **Graduate the unowned absences.** Read what this feature recorded about surfaces nothing reaches, and think about three things for each:

   - **CHOSEN** — which decision chose this absence? If none did, it is a gap rather than a design.
   - **OWNED** — what downstream owns building it? If nothing does, it is `UNOWNED`.
   - **WHERE** — where will the next planner look for this, and is it there?

   An `UNOWNED` absence becomes a standing flag of kind `OUTWARD` in `05_progress_overview.md`. It closes when it has been written into the document this project's planners actually read — a `CLAUDE.md`, a domain index, whatever they open when cutting the next feature — with that path cited as the closing evidence. zforge names the obligation and asks for a landing site; the destination belongs to the project.

   A phase that walks a journey finds these, states them well, and states them in a file no planner opens. The writing is rarely the problem; the routing is, and this is the moment to do it.

4. **Graduate the harness conventions.** Where `07_harness_conventions.md` exists, write the facts still true, in their simplest final form, into the project's conventions document — its `CLAUDE.md`, or the nearest doc phases actually read. A fact a later phase made obsolete does not graduate, and neither does the account of how one was learned. The feature file accumulates what the run learned; the project file states what is true of the harness now. These facts outlive the feature that paid for them.
5. **Drop the feature's artifact directory.** `/tmp/zforge/artifacts/{feature}/` has done its work: every row was reconciled against it at acceptance, and what the run needs to keep is in the rows. Anything a standing flag still depends on is quoted in `05_progress_overview.md` before the directory goes.
6. Report to the user: phases completed, evidence classes achieved against those planned, rows accepted below their class and why, open 🟡 decisions awaiting review, and any flag that had to be carried.
7. Suggest `$zforge:review` for feature `{name}` to check the implementation against the ledger.

If flags remain open, say so plainly and name them. A feature with an open flag is not finished; it is finished-except-for-a-named-gap, and the difference is the entire point of tracking them.
