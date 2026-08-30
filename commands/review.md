---
description: Check implementation against the feature ledger
argument-hint: [--feature name]
allowed-tools: Read, Glob, Grep, Bash(git:*), Task, Agent
---

# /review — Ledger vs. Implementation

Check what the code does against what the feature's documents say it does.

This is not a general code review. Bugs, security, performance and style belong to `/code-review` and `ce:review`, which are better at them and do not need the ledger. **This review is the one nobody else can run**, because it is the only one holding the plan, the patterns, the decisions and the evidence claims at the same time.

## Arguments

- `--feature <name>` — the feature directory to review against. Required; without a ledger there is nothing here to do.

## What to read first

1. `02_plan.md` — schema, contracts, phase decomposition, **Verification Matrix**, **Environment Assumptions**, **Invariants**
2. The core patterns doc, if the Doc Map lists one — the rules agents were told to follow
3. `decision_review.md` §A and §C — the decisions that reached beyond the implementation, and whatever the user has already adjudicated
4. Every phase file's `## Decisions` — the implementation conventions that were not promoted. This is the larger set, and it binds the code just as tightly
5. Every phase file's `## Evidence Required` and `## Acceptance`
6. `05_progress_overview.md` — open standing flags

Then read the code those documents describe.

## What to check

Four questions, each answerable against a document rather than a judgment call:

**1. Do the decisions hold in the code?**
Every 🟡 and ✅ entry in `decision_review.md`, and every row in a phase file's `## Decisions`, claims something about how the system works. Check the call sites. A decision recorded once and violated in four places is the common shape, and it is commonest among the unpromoted conventions — the ledger's rows had the user's eye on them, the phase files' rows had nobody's.

**2. Are the invariants implemented and re-checked?**
`02_plan.md` names invariants with an owner phase and a re-check phase. Verify each is actually established, and actually holds at every call site — not just the one the owning phase wrote. Anything spanning phases is verified by no single phase file, which is why it survives to here.

**3. Does the evidence match the artifacts?**
For every `## Evidence Required` row, the claimed class must have something behind it. A row claiming E4 with no browser-executed artifact, or E3 with tests that only ever ran in the wrong runtime, is a false claim in the ledger — report it as one. So is a figure presented as a measurement that appears in no committed artifact, and a row whose named artifact is not in the tree.

**A row accepted below its required class is a recorded waiver** where `## Acceptance` carries the reasoning that settled it. Check that reasoning rather than the class: does the postcondition really hold without what the missing class rules out, and has a later phase since come to depend on it? A waiver that was sound at acceptance and has been overtaken is a finding, and it opens a standing flag rather than a correction.

A **J** row is checked the same way: the method and the referent must both be named, and the walk must have a recorded result. A J2 row whose referent turns out to be the case the design was derived from is a J1 claim wearing a J2 label, because the referent supplied no resistance.

**4. Do the environment substitutions still hold?**
Each substitution in `## Environment Assumptions` deferred some verification. Check whether the deferral is still true, still recorded, and still visible as a standing flag.

## Method

Spawn parallel subagents when the surface is large — one per document-to-code axis above, each returning its findings. Give each the ledger sections it needs and the code paths those sections name.

Every finding must cite **both sides**: the document and line that states the rule, and the file and line that departs from it. A finding that cannot cite both is a code-quality opinion and belongs in a different review.

## Output

Append to `05_progress/review.md`:

| # | Finding | Document says | Code does | Phase | Severity |
|---|---------|---------------|-----------|-------|----------|

Then report to the user:

- Findings, ordered by severity
- Any decision entry that should move to ❌ as a result
- Any standing flag that should be opened — an evidence claim that did not survive checking is a flag, not just a finding

Nothing here is filtered by a confidence score. A mismatch between a document and the code either exists or it does not, and both sides are cited so the user can check in seconds.
