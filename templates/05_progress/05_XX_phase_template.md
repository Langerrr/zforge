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
     demonstrably true when it closes), and its surface (which files it may touch).
     One contract per phase file: scope added after acceptance goes in a new phase file that depends on this one. -->

```
{What to build, what must be true at the end, which files are in scope}
```

---

## Required Context

<!-- Planner fills this. The agent reads these before starting the checklist — this table is
     what makes it write structurally correct code rather than merely checklist-complete code,
     so a phase that skips it tends to pass its own checklist and fail review.
     Bind specific sections, not whole documents. A skill the phase must run is a row too:
     name it under File, and say under Why when it runs. -->

| File | Sections | Why |
|------|----------|-----|

---

## Evidence Required

<!-- Inherited from the Verification Matrix in 02_plan.md — not reinvented here.
     Required is set by the planner before the phase runs. Achieved and Artifact are filled
     by the agent, each row when its command runs. An E row names a command; a J row names a
     method and the referent it is walked against.

     The classes: skills/template-conventions/references/evidence-scale.md
     How a row and its artifact are written:
     skills/feature-execution/references/phase-contract.md §Evidence

     An absence you record names what chose it, or says that nothing did. "There is no
     endpoint" carries no finding. "There is no endpoint, and decision A120 is why" and
     "there is no endpoint and no decision names one" are opposite findings, and only the
     second is owed to anyone.

     Artifact paths read /tmp/zforge/artifacts/{feature}/{phase}_{what-it-is}.{NN}.{ext}
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

<!-- Recorded as they are made, not reconstructed at the end. Reach is `feature` or `outward`.
     What each means, and what goes to 07_harness_conventions.md instead of here:
     skills/feature-execution/references/phase-contract.md §Decisions and §Harness facts -->

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
     when the planner accepts. -->

| Date | Session | Steps | Summary |
|------|---------|-------|---------|

---

## Resume Point

<!-- Written by the agent only when it stops before the phase is finished: what is done,
     what is half-done, and the next concrete action. The resuming agent deletes it once it
     passes the point named here; a phase that closes with one still in it did not finish. -->

---

## Acceptance

<!-- PLANNER-OWNED. The agent does not write here.
     The acceptance report, verbatim, then two lines and nothing else:

       ADJUDICATED: ACCEPT | ACCEPT-WITH-NOTES | PAUSE | FLAG — {date} — <one sentence, only
       where the planner departs from the recommendation, and why>
       PROMOTED: D3, D7 | none

     A phase reopened after acceptance gets one line under the report, for the rows the change
     touched:

       RE-ACCEPTED: {date} — rows 1, 3 re-verified from <artifact paths>; row 2 unchanged -->
