# The Evidence Scale

One vocabulary for how strongly a claim has been demonstrated. Declared per phase at planning time in `02_plan.md`'s Verification Matrix, inherited by each phase's `## Evidence Required` table, and confirmed by the planner at acceptance.

## The classes

| | | Rules out | Typical artifact |
|---|---|---|---|
| **E0** | Asserted | nothing | a sentence |
| **E1** | Pure logic verified | algorithm errors | unit tests over extracted logic |
| **E2** | Boundary crossed | integration mismatches | tests against a real database, a real queue, the actual HTTP layer |
| **E3** | Production runtime | runtime-environment divergence | the same code exercised in the runtime it ships to, not a stand-in |
| **E4** | Real surface | wiring and delivery defects | the built artifact executed the way a user reaches it |

The order is by **what each class rules out**, not by effort. E1 says the algorithm is right and says nothing about whether anything calls it. E4 says the thing works when reached the way it is actually reached, and says nothing about whether the algorithm is right. They are not substitutes.

## E0 is a real value

Write E0 when nothing was run. It is the honest value for a claim that rests on reading the code, and it is greppable. A phase whose evidence table is entirely E0 has demonstrated nothing, however complete its checklist looks — and that is exactly what E0 is for saying.

## What is not on the scale

**Production dependencies** — vendor credentials, live buckets, real payment providers, deploy targets. Their absence is not a weaker class of evidence, it is a *substitution*, and it belongs in `## Environment Assumptions`, which records what the substitution defers. A phase running against a local container instead of the managed service can still reach E2 or E3 against that container; what it cannot do is claim the vendor's behaviour was verified.

## Choosing a class at plan time

Ask what the phase could plausibly get wrong, then name the class that would catch it:

- Logic a human would struggle to trace → **E1**
- Two components that must agree on a contract → **E2**
- Code whose runtime differs from the test environment — different JS runtime, different container, different platform APIs → **E3**
- Anything a user or client actually loads: a page, a bundle, a CLI invocation, a deployed endpoint → **E4**

A feature with a user-facing surface whose matrix has an empty E4 column has a known hole, and naming it at plan time is the whole purpose of declaring classes before work starts.

## The gap between required and achieved

At acceptance the planner re-runs the named commands and compares.

| | |
|---|---|
| achieved = required | accept |
| achieved > required | accept, note the surplus |
| achieved < required | pause the phase, or open a standing flag with a stated *closes when* |

An unmet class never disappears by the phase ending. It becomes a standing flag in `05_progress_overview.md` and stays visible until the evidence that closes it exists.
