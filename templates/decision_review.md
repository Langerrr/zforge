# {Feature Name} — Decision Review

> Last updated: {DATE}
> Owner: Planner (appends) · User (adjudicates)

Decisions made without blocking the run, recorded here for review whenever the user chooses.

**Lifecycle:** every entry opens 🟡 awaiting review. The user marks ✅ approved or ❌ rework. A ❌ entry becomes a rework item in the phase it affects.

**Supersession:** a later entry may supersede an earlier one by reference (`Supersedes: P2.8`). The earlier entry stays; the record is the point.

**Rationale states why, never who.** Where the reason was not stated, write `not stated` rather than naming a source — an unfilled reason should look unfilled.

---

## §A Planner Decisions

Run-level decisions: architecture calls made during planning, degraded-mode substitutions, scheduling judgments, scope changes accepted mid-run.

| # | Status | Decision | Why | Alternative rejected | Impact |
|---|--------|----------|-----|---------------------|--------|
| D1 | 🟡 | | | | |

---

## §B Process Notes

Observations about the workflow itself, appended live during the run — friction, workarounds, anything improvised because the template had no home for it. This is `/zforge:retro`'s primary input, and it is written while the memory is intact rather than reconstructed afterwards.

| # | Phase | Observation | What was done instead |
|---|-------|-------------|----------------------|
| O1 | | | |

---

## §C Phase Decisions

Promoted from each phase file's `## Decisions` table at acceptance.

**A decision is promoted only when it reaches beyond the feature's implementation** — it contradicts or extends a design document, asserts something the domain model does not define, or hands an obligation to a later band. A decision that only binds later phases stays in the phase file, where phase agents already read it.

This table is an adjudication queue, not an index of everything decided. A phase routinely records ten or more decisions and most are implementation conventions — which package call, which transport, which pinned version. A row here is one **the user has to answer**. A question a *later phase* will answer belongs in that phase's `## Open Items`, which is what carries cross-phase obligations.

Each phase's `## Acceptance` names which of its rows came up here and why, so the phase file records what was promoted and what stayed.

### Phase {N} — {Phase Name}

| # | Status | Decision | Why | Alternative rejected | Impact |
|---|--------|----------|-----|---------------------|--------|
| P{N}.1 | 🟡 | | | | |
