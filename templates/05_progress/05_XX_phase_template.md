# {Feature Name} - Phase {N}: {Phase Name}

> Last updated: {DATE}
> Status: PENDING
> Depends on: {phases, or None}
> Overview: `../05_progress_overview.md`

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
     Required is set by the planner before the phase runs. Achieved is filled by the agent
     with the class actually reached. See skills/template-conventions/references/evidence-scale.md -->

| Claim | Required | Command / artifact | Achieved |
|-------|----------|--------------------|----------|

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
     Rationale states why, never who. If no reason was stated, write "not stated". -->

| # | Decision | Why | Alternative rejected | Impact |
|---|----------|-----|---------------------|--------|

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

| Date | Session | Steps | Summary |
|------|---------|-------|---------|

---

## Acceptance

<!-- PLANNER-OWNED. The agent does not write here.
     Written after independently re-running the commands in ## Evidence Required:
     what was re-run, the result, and achieved-versus-required per row. -->
