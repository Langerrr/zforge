# The Evidence Scale

One vocabulary for how strongly a claim has been demonstrated. Declared per phase at planning time in `02_plan.md`'s Verification Matrix, inherited by each phase's `## Evidence Required` table, and confirmed by the planner at acceptance.

The scale has two axes, because claims fail in two different ways. **E** measures what was *executed*. **J** measures what was *judged*. A claim takes a class on the axis that matches how it can be wrong; some claims take one on each.

## E — execution

| | | Rules out | Typical artifact |
|---|---|---|---|
| **E0** | Asserted | nothing | a sentence |
| **E1** | Pure logic verified | algorithm errors | unit tests over extracted logic |
| **E2** | Boundary crossed | integration mismatches | tests against a real database, a real queue, the actual HTTP layer |
| **E3** | Production runtime | runtime-environment divergence | the same code exercised in the runtime it ships to, not a stand-in |
| **E4** | Real surface | wiring and delivery defects | the built artifact executed the way a user reaches it |

The order is by **what each class rules out**, not by effort. E1 says the algorithm is right and says nothing about whether anything calls it. E4 says the thing works when reached the way it is actually reached, and says nothing about whether the algorithm is right. They are not substitutes.

## J — judgement

| | | Rules out | Typical artifact |
|---|---|---|---|
| **J0** | Asserted | nothing | a sentence |
| **J1** | Method stated and applied | unstated reasoning | the method written down, walked, and its result recorded |
| **J2** | Checked against a named referent | reading one's own design charitably | the exemplar, journey, rubric or competing product the claim was tested against, named |

A J class is what a design document, a requirements document or an interface claim can honestly hold. *"The creator never has to learn the model"* is not a proposition any test runner settles, and it is not merely asserted either — walking a named journey and listing every noun the creator had to understand is a real check with a real result, and it can fail.

**J2 needs a referent that was not built for the claim.** Encoding two exemplars neither of which was designed for the format is J2; encoding the one exemplar the format was derived from is J1. The referent is what supplies the resistance.

## The zero classes are written separately

E0 and J0 both mean nothing was done. Which one is written says **what kind of check is missing** — E0 is a claim that should have been run and was not, J0 is a claim that should have been judged and was not. Both are greppable, and they call for different work.

A phase whose evidence table is entirely E0 and J0 has demonstrated nothing, however complete its checklist looks, and that is exactly what the zero classes are for saying.

## Which axis a claim takes

The split is not *design versus implementation*. It is **execution-shaped versus judgement-shaped**, and design work lands on both sides:

| Claim | Axis |
|---|---|
| A transport encoding survives the Worker runtime | **E3** |
| An open-source editor embeds in the page and loads | **E4** |
| A vocabulary is learnable by the actor who meets it first | **J** |
| A format generalises past the case that produced it | **J2** |
| A boundary is drawn in the right place | **J** |

Where a claim is both — a surface that must work *and* must read correctly to the person using it — declare a class on each axis and let acceptance check both.

## What is not on either scale

**Production dependencies** — vendor credentials, live buckets, real payment providers, deploy targets. Their absence is not a weaker class of evidence, it is a *substitution*, and it belongs in `## Environment Assumptions`, which records what the substitution defers. A phase running against a local container instead of the managed service can still reach E2 or E3 against that container; what it cannot do is claim the vendor's behaviour was verified.

## Choosing a class at plan time

Ask what the phase could plausibly get wrong, then name the class that would catch it.

Execution-shaped:

- Logic a human would struggle to trace → **E1**
- Two components that must agree on a contract → **E2**
- Code whose runtime differs from the test environment — different JS runtime, different container, different platform APIs → **E3**
- Anything a user or client actually loads: a page, a bundle, a CLI invocation, a deployed endpoint → **E4**

Judgement-shaped:

- A claim about what someone will understand, expect or reach for → **J1** with the walk named, **J2** where there is a journey or exemplar to walk it against
- A claim that a design generalises → **J2**, against a case it was not derived from
- A claim that this is the right boundary, name or model → **J1** at least: write the method, not the conclusion

A feature with a user-facing surface whose matrix has an empty E4 column has a known hole. A feature whose acceptance vocabulary came from the user verbatim and whose matrix has an empty J column has the same hole one level up. Naming either at plan time is the whole purpose of declaring classes before work starts.

## The gap between required and achieved

At acceptance the planner re-runs the named commands and re-applies the named methods. A J row is re-checked the way an E row is: the method is on the page, so another party can walk it.

| | |
|---|---|
| achieved = required | accept |
| achieved > required | accept, note the surplus |
| achieved < required | pause the phase, or open a standing flag with a stated *closes when* |

Classes compare **within an axis only**. E3 is not more than J2, and neither stands in for the other.

An unmet class never disappears by the phase ending. It becomes a standing flag in `05_progress_overview.md` and stays visible until the evidence that closes it exists.
