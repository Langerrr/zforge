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

## The artifact is what carries the class

A class is claimed by a row and held by an artifact. Three rules keep the two attached:

- **Write the row when the command runs, from the artifact the command wrote.** Not at session end, and not from console output. Console output is gone by the time anyone checks, and a row written from memory at the end of a long context is a claim about a claim.
- **Name artifacts per run.** A second run that overwrites the file a row quotes leaves the row quoting a measurement nobody can open. Where a command is run twice, the two artifacts have two names.
- **A figure presented as a measurement appears verbatim in its artifact**, or the row says it cannot. This is the check acceptance runs first, and it is the cheapest one available.

The row carries the finding and the artifact path. How the number was obtained belongs in the artifact.

Artifacts are written outside every repository, to `/tmp/zforge/artifacts/{feature}/`, and cited by their full path. The directory is dropped when the feature closes: an artifact exists to be read at acceptance, which is also the moment a figure with nothing behind it is caught. After that the row is the record. `full-template.md` §Where artifacts live has the naming and the paths.

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

At acceptance every row is reconciled against its artifact, and what a fact forces or judgment selects is re-executed. A J row is re-checked the way an E row is: the method is on the page, so another party can walk it. `feature-execution` §Acceptance carries the tiers and what decides between them.

| | |
|---|---|
| achieved = required | accept |
| achieved > required | accept, note the surplus |
| achieved < required, material | pause the phase, or open a standing flag with a stated *closes when* |
| achieved < required, immaterial | accept, recording the gap, why the postcondition does not depend on it, and what would make it matter |

Classes compare **within an axis only**. E3 is not more than J2, and neither stands in for the other.

**Materiality is read off the scale.** Each class states what it rules out. Name what the missing class would have ruled out, then ask whether anything downstream in this feature relies on that being ruled out. Nothing does, and no later phase inherits the assumption: the gap is immaterial. A judgment that takes more than a paragraph to state is material.

Worked: a phase whose postcondition is a transport encoding, required at E4 and reached at E3, was exercised in its shipping runtime but not through the surface a user reaches. E4 rules out wiring and delivery defects. Where the surface is another phase's postcondition and this phase's encoding is what the later phase consumes, nothing here depends on the wiring being ruled out, and the row is accepted at E3 with that reasoning written down.

Two shortfalls are never immaterial: a command that **selected nothing and exited 0**, which reads exactly like a pass, and a **user-reachable surface that nothing reached the way a user reaches it**. Every other row is judged by impact rather than by category.

The achieved class is recorded as reached, whichever outcome the row takes. A material unmet class becomes a standing flag in `05_progress_overview.md` and stays visible until the evidence that closes it exists. An immaterial one is recorded in `## Acceptance` with the reasoning that settled it, where the next reader can disagree with it.
