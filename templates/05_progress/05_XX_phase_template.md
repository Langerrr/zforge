# {Feature Name} - Phase {N}: {Phase Name}

> Last updated: {DATE}
> Status: PENDING
> Depends on: {phases, or None}
> Overview: `../05_progress_overview.md`

<!-- Status is one of: PENDING · READY · WAITING · RUNNING · REPORTED · PAUSED ·
     INTERRUPTED · FAILED · COMPLETED. The agent sets REPORTED, PAUSED or FAILED as its
     last act before it reports — the work is on disk, the verification is not.
     COMPLETED is set by acceptance and by nothing else. -->

---

## Agent Prompt

<!-- Authoritative. This is the only copy — the spawn message points here, it does not restate this.
     Written by the planner. State what this phase covers, its postcondition (what must be
     demonstrably true when it closes), and its surface (which files it may touch). -->

```
{What to build, what must be true at the end, which files are in scope}
```

---

## Required Context

<!-- Planner fills this. The agent reads these before starting the checklist — this table is
     what makes it write structurally correct code rather than merely checklist-complete code,
     so a phase that skips it tends to pass its own checklist and fail review.
     Bind specific sections, not whole documents. -->

| File | Sections | Why |
|------|----------|-----|

---

## Evidence Required

<!-- Inherited from the Verification Matrix in 02_plan.md — not reinvented here.
     Required is set by the planner before the phase runs. Achieved and Artifact are filled
     by the agent. See skills/template-conventions/references/evidence-scale.md

     Classes come from two axes. E0-E4 for what was executed: the row names a command.
     J0-J2 for what was judged: the row names a method and the referent it is walked
     against. A claim that is both a working surface and a readable one takes a row on
     each. Classes compare within an axis only — E3 is not more than J2.

     Fill a row when its command runs, from the artifact that command wrote — not at the
     end of the phase and not from console scrollback. Every figure presented as a
     measurement appears verbatim in that artifact, or the row says it cannot.

     An absence you record names what chose it, or says that nothing did. "There is no
     endpoint" carries no finding. "There is no endpoint, and decision A120 is why" and
     "there is no endpoint and no decision names one" are opposite findings, and only the
     second is owed to anyone.

     Artifacts go to /tmp/zforge/artifacts/{feature}/ — outside every repository, never into
     this docs tree. An artifact is the smallest file that carries the figures its row quotes —
     a log, an XML report, a JSON, a screenshot — one per row per run and never a directory.
     State the command produced stays where the command put it and is cited in place.
     Name artifacts {phase}_{what-it-is}.{NN}.{ext} so a second run cannot overwrite the file
     an earlier row quotes, and cite each by its full path:
     /tmp/zforge/artifacts/creator-platform/05_04_e2e.01.json

     The achieved cell carries the count, the exit code, the duration, the one figure the claim
     rests on — not a paragraph. -->

| Claim | Required | Command / method | Achieved | Artifact |
|-------|----------|------------------|----------|----------|

---

## Environment Assumptions

<!-- What this phase needs that may not exist here, and what standing in for it defers. -->

| Assumed by plan | Actual here | Substitution | What it defers |
|-----------------|-------------|--------------|----------------|

---

## Checklist

- [ ] {N}.1 {Step name}
- [ ] {N}.2 {Step name}
- [ ] {N}.3 {Step name}

---

## Decisions

<!-- Recorded as they are made, not reconstructed at the end.
     Rationale states why, never who. If no reason was stated, write "not stated".

     Reach is `feature` by default, or `outward` for a decision that contradicts or extends a
     design document, asserts something the domain model does not define, or hands an
     obligation to a later feature. The planner promotes the `outward` rows to
     decision_review.md at acceptance and does not re-read the rest.

     A fact about how this project is run and observed is not a decision: it goes straight
     into 07_harness_conventions.md, at the moment it is learned. -->

| # | Reach | Decision | Why | Alternative rejected | Impact |
|---|-------|----------|-----|---------------------|--------|

---

## Open Items

<!-- Anything needing the planner or the user: a question, an error, a blocker, an evidence gap.
     Resolved items stay, with their resolution. -->

| # | Kind | What | Raised at | Status / Resolution |
|---|------|------|-----------|---------------------|

---

## Files Created/Modified

| File | Step | Action |
|------|------|--------|

---

## Session Log

<!-- One row per run of this phase, written when the agent stops — its report lines — and one
     when the planner accepts. Milestones, pauses and repairs are not rows: the question is in
     Open Items, the stopping point in Resume Point, the verdict in Acceptance. -->

| Date | Session | Steps | Summary |
|------|---------|-------|---------|

---

## Resume Point

<!-- Written by the agent only when it stops before the phase is finished — a pause
     trigger, or the budget-stop clause at ~95% of usage. Three things: what is done,
     what is half-done, and the next concrete action.

     The resuming agent treats this as a hypothesis and the working tree as the fact,
     then deletes this section once it passes the point named here. A phase that closes
     with a Resume Point still in it did not finish. -->

---

## Acceptance

<!-- PLANNER-OWNED. The agent does not write here.
     The acceptance report, verbatim — PHASE, ROWS, the per-row table with its Method column,
     VERDICT, RATIONALE, FLOOR, PLAN DRIFT, UNVERIFIABLE, MISSING FILES, HARNESS, NOTES — then
     two lines and nothing else:

       ADJUDICATED: ACCEPT | ACCEPT-WITH-NOTES | PAUSE | FLAG — {date} — <one sentence, only
       where the planner departs from the recommendation, and why>
       PROMOTED: D3, D7 | none

     The report's RATIONALE is where a row accepted below its class carries the reasoning that
     settled it — what the missing class would have ruled out, why the postcondition does not
     depend on it, what would make it matter. The achieved class is recorded as reached either way.

     A phase reopened after acceptance gets one line under the report, for the rows the change
     touched:

       RE-ACCEPTED: {date} — rows 1, 3 re-verified from <artifact paths>; row 2 unchanged -->
