# Acceptance by risk and judgment

**Status:** design, for v4.1.0
**Supersedes:** the unconditional re-execution bar in `skills/feature-execution/SKILL.md` §Acceptance
**Evidence base:** `ai-video/_retro_notes/H_why_every_phase_took_two_passes.md` — nine phases of
`wire-and-store`, six of which took two passes and one of which took five.

---

## The principle

The workflow supplies what a model lacks and stops dictating what a model does well.

A capable model is poor at recalling what a command printed forty minutes ago, at arithmetic
against numbers not in front of it, and at knowing a command's side effects. It is good at
deciding whether a gap matters and at deciding what needs re-running. Acceptance was built the
other way around: it mandated the judgment away and left the recall unaided.

Every change below moves one constraint across that line.

## What the evidence says

Nine evidence rows were refused across the tree. In eight, the code was right and the statement
about it was wrong. The dominant cost was not verification — it was that verification ran against
prose written from memory at the end of a long context.

Acceptance's independent re-run caught a zero-test false pass, a fixture that did not reproduce, a
finding that did not exist, and six misquoted figures. It earns its place, and it earns it in a
specific half: one phase's acceptance re-executed roughly 45 minutes of commands to find defects that
were almost entirely arithmetic against committed JSON. The recompute-from-artifact half found
everything.

---

## 1. Two tiers

**Tier 1 — reconciliation.** Every row, every time, no re-execution.

- Does the row's named artifact exist?
- Does every figure the row states appear in that artifact verbatim?
- Does the recorded output show a command that selected nothing — zero tests matched, zero
  assertions run, zero results — and exited 0?

**Tier 2 — re-execution.** A row is re-run when one of these holds:

- Tier 1 found a mismatch, or the artifact is missing or quotes nothing.
- The required class is **E3 or E4**. Those classes are claims about execution in a real runtime
  or through a real surface; an artifact cannot stand for them.
- The row names no artifact, only a claim.
- The phase agent flagged the row itself, or filled achieved below required.
- The claim is about a clean or regenerated state.
- The accepting party judges that a failure here would need human attention.

Otherwise the artifact stands.

Each row records how it was verified — `from-artifact` or `re-executed`. The work gets cheaper;
the record stays exact about which check was performed.

## 2. Three outcomes

| Result | Response |
|---|---|
| achieved = required | Accept |
| achieved > required | Accept, note the surplus |
| achieved < required, **material** | Pause the phase, or open a standing flag with a stated *closes when* |
| achieved < required, **immaterial** | Accept, recording the gap, why the postcondition does not depend on it, and what would make it matter |

The achieved class is recorded as reached. A row that reached E3 against an E4 requirement reads
E3 whichever outcome it takes.

**Materiality.** Name what the missing class rules out — `evidence-scale.md` states it per class —
then ask whether anything downstream in this feature relies on that being ruled out. Nothing does,
and no later phase inherits the assumption: immaterial. A judgment that takes more than a paragraph
to state is material.

**The floor.** Two shortfalls are never immaterial:

1. A command that selected nothing and exited 0. It is indistinguishable from a pass and it is not one.
2. A user-reachable surface that nothing reached the way a user reaches it.

Every other row is judged by impact rather than by category, including rows touching auth, data
mutation and migrations. Two obligations attach to that judgment: where the implementation drifted
from the plan, `## Acceptance` records the drift whatever the impact; and where the impact needs
human attention, the row pauses or flags on its own merits.

## 3. The acceptance agent recommends

The agent returns a per-row verdict and an overall recommendation with its rationale — the
reasoning the planner otherwise re-derives from a stripped table with less context than the party
that ran the check.

Adjudication stays with the planner. So do the two rules that make the agent independent: it never
fixes anything, and it never writes the phase file.

## 4. Side effects bound re-execution

A command that tears down state other rows depend on is verified from its artifact, with the reason
stated, rather than re-run. Re-running the clean form requires an isolated worktree the planner has
provisioned.

The acceptance agent reads `## Environment Assumptions` and `07_harness_conventions.md` before
running anything. The harness file is what makes this enforceable: a teardown command looks like
any other command until something says otherwise.

## 5. Evidence written as produced

Each evidence row is written **when its command runs, from the artifact that command wrote**.

- Never batched at session end, never from console scrollback.
- Artifacts named per run, so a re-run cannot overwrite the one a row quotes.
- A figure in a row appears verbatim in a committed artifact, or the row states that it cannot.
- The row carries the finding and the artifact path. How the number was obtained lives in the artifact.

This is the change with the largest expected return, and it is what makes tier 1 possible: tier 1
reconciles rows against artifacts, and only works where the artifacts exist and are quotable.

## 6. `/goal` carries the planner across deaths

An agent's cost is per-phase and bounded. The planner's is cumulative across the whole run, and it
is the budget that cannot be reset. Nothing on disk records what is still owed except the planner's
own context.

In Claude Code, `/goal <condition>` sets a completion condition; a separate check after each turn
decides whether it is met, and the goal is restored on `--resume`. One goal is active at a time.

- **The condition is the feature.** A per-phase goal is replaced at every phase and cannot survive
  the run.
- **The condition names zforge's own bar**, so the harness check and the phase files agree: every
  phase COMPLETED and no standing flag open.
- **It composes.** `/goal` answers whether to keep working; the phase files answer what is accepted.
  There is no second progress ledger.
- **It is never set implicitly.** Invoking orchestration is not permission to set or replace a goal.

What this buys is a planner that can die cheaply: `--resume` restores the goal, the phase files
restore the state.

## 7. Harness conventions

`docs/{feature}/07_harness_conventions.md` records how the code is run and observed — facts about
the test harness, not the product. Command interactions, defaults that bound nothing, teardown
steps, and the ways an observation can read as a pass.

- **Written by promotion.** A phase agent records a harness fact in its phase file; the planner
  promotes it at acceptance, so the next phase reads it rather than paying for it again.
- **Read before specs are written.** Bound into `## Required Context` for every phase whose evidence
  table names a command; read by the planner before the Verification Matrix; read by the acceptance
  agent before it re-runs anything.
- **Graduated by trim.** At completion the planner writes the facts still true, in their simplest
  final form, into the project's conventions document. A fact a later phase made obsolete does not
  graduate. The feature file accumulates what was learned; the project file states what is true.

---

## Unchanged

**A feature is complete when every phase is COMPLETED and no standing flag is open.** Fewer flags
open under §2, because an immaterial gap is recorded rather than flagged. The rule is what keeps a
material gap visible after the run ends.

**The acceptance agent never fixes and never writes the phase file.** Those are what make its
report independent.
