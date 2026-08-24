---
name: debug
description: Route a concrete reproducible failure through the installed debugging skills; not for open-ended exploration.
---

# Debugging Router

A concrete failure — a broken test, a reproducible bug, a failing deploy. This skill owns no debugging opinion of its own; it names which methodology applies and in what order, because the failure mode is applying one of them and skipping the rest.

Not for open-ended exploration ("this feels wrong"). That is `$compound-engineering:ce-ideate` territory.

## Sequence

**1. `$superpowers:systematic-debugging` — start here when installed.**
Investigation discipline comes before any fix, including when the cause seems obvious. When Superpowers is unavailable, use the host's equivalent systematic-debugging workflow; do not skip the investigation step.

**2. `$compound-engineering:ce-debug` — add when installed.**
Its hypothesis-and-prediction gate goes *before* any code change: state what you believe is wrong and what you expect to see if you are right, then check. Without Compound Engineering, apply that same hypothesis-and-prediction gate directly. A fix applied without a failed prediction is a guess that happened to be typed confidently.

**3. `$zforge:async-reasoning` — add when the failure involves timing.**
Async state, race conditions, cache invalidation, init order, stale reads, write-then-read gaps within one component.

**4. `$distributed-architect:dist-debug` — add when that compatible plugin is installed and the failure crosses a boundary.**
Cross-service, cross-process, distributed races. Backward tracing from the symptom to the boundary where the cause lives. Check the project's topology file first if it has one.

## While debugging a planned feature

If the failure is in a feature with a zforge directory, the ledger is evidence:

- `decision_review.md` may already contain the decision that caused this.
- An open standing flag may already name this defect class — a bug in the gap a flag describes is a flag being discharged the expensive way.
- The phase's `## Evidence Required` shows what was never verified, which is usually where to look first.

## After the fix

Record it where it will be found again:

- In a feature phase — `## Decisions` and `## Open Items`, so acceptance sees it.
- Worth remembering beyond this feature — `$compound-engineering:ce-compound` writes it to `docs/solutions/` so the next occurrence is a search rather than a re-investigation.

A fix with no test that fails without it is not finished.
