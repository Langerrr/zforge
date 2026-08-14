# {Feature Name} - Context

> Last updated: {DATE}
> Status: Planning
> Design Spec: `./00_design_spec.md`

---

## Summary

{1-2 paragraph overview of the feature}

---

## Doc Map

Every document in this feature directory, and which phases are bound by it. Agents read what their phase's `## Required Context` binds; this table is where that binding is chosen from.

| File | Purpose | Binding for |
|------|---------|-------------|
| `00_design_spec.md` | Requirements, architecture, acceptance | all |
| `02_plan.md` | Technical plan, verification matrix, invariants | all |
| `decision_review.md` | Decisions awaiting review | planner |
| `discussion.md` | Reasoning behind the decisions | planner |

Documents beyond the fixed `00`–`02` and `05` set are **named for what they are** and numbered by creation order in whatever slot is free. The name carries the identity; the number only sorts.

---

## Key Decisions

### {Decision Title}
**Decision:** {What was decided}
**Rationale:** {Why — the reasoning, not the source. If no reason was given, write "not stated"}
**Source:** {Where it came from, if worth recording}
**Alternatives Considered:** {What was rejected, and why}

<!-- Rationale states why, never who. A decision whose reasoning lives only in a transcript
     is one compaction away from being gone, and "user-directed" reads as filled when it is not. -->

---

## Architecture Overview

{How the feature fits into the existing system, key integration points}

---

## Scope

### Included
- {What's in scope}

### Excluded
- {What's out of scope}

---

## Open Questions

A question that gates a phase needs an **owner**, a **method** and a **date** before phase files can be written. A question with no method is either not actually blocking, or it is not yet a question.

| # | Question | Blocks | Owner | Method — how it gets answered | By when |
|---|----------|--------|-------|-------------------------------|---------|
| Q1 | | {phase, or nothing} | | | |

---

## Dependencies

| Dependency | Type | Status |
|------------|------|--------|
| {Service/Library} | {Runtime/Build/External} | {Available/Needs setup} |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| {DATE} | Initial context created | /zforge:plan |
