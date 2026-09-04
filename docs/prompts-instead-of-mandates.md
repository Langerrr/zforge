# Prompts instead of mandates

**Status:** design, for v4.3.0
**Supersedes:** the class-keyed re-execution trigger in `acceptance-by-risk-and-judgment.md` §1,
and the artifact location in `evidence-artifacts-outside-the-docs-tree.md`
**Evidence base:** `ai-video/_retro_notes/I_findings_that_reach_no_plan.md` — five journey steps
found, owned and lost across three features; `ai-video/_retro_notes/J_the_tier_split_and_the_full_suite.md`
— ~43 min of command time per phase, most of it a suite run twice;
`tuurny/tmp/resume-2026-09-04-06.md` — 2h18m of post-closure work, 61% of the session.

---

## The principle

The workflow names the thought and leaves the answer to the model.

A model decides well at the point of decision and skips the decision entirely when a step
already answers it. The three costs measured above each trace to a step that supplied an answer
where a question belonged: acceptance re-ran the widest available command because a class column
said to, a phase recorded twelve unowned absences because nothing asked who owned them, and a
closed feature was reopened for two hours because closure had no act of its own.

Each change below removes an answer and puts the question in its place. A question holds its
value as the model improves. A threshold decays.

---

## 1. Acceptance decides what to re-run

Tier 2's trigger list mixes two kinds of entry. Some are facts an accepting party can read off
the phase file in a second — the artifact is missing, the agent flagged the row. One is a
category judgment made at plan time by someone who did not know what the command would cost:
`the required class is E3 or E4`.

Tier 2 keeps the facts and replaces the category.

### The new tier 2

```
Re-run a row when a fact forces it:

  - Tier 1 found a mismatch, or the artifact is missing or quotes nothing.
  - The row names no artifact, only a claim.
  - The agent flagged the row itself, in ## Open Items or by filling achieved below required.
  - The claim is about a clean or regenerated state.

Otherwise decide, and think about three things:

  COST            what running this takes
  GAIN            which unknown it retires, priced by what being wrong about it costs
  MINIMUM EFFORT  the smallest thing that retires that same unknown
```

`A failure in this row would need human attention` folds into GAIN — that is what pricing an
unknown by the cost of being wrong about it means.

### What the three words settle

A ten-minute browser suite re-run against a tree acceptance has not modified retires almost no
unknown, and costs the run its own flake exposure on top. A one-minute filtered run against the
surface the phase built retires the unknown that matters — whether the thing works through a
real surface — for a fifteenth of the time. Both are E4. The class never separated them.

MINIMUM EFFORT is the entry that reaches every future tree: it asks for the smallest invocation
that still crosses the claim, whatever the phase file happened to record as the command.

### Two dependent lines

- Delegation guidance currently reads *"A pass that will re-execute E3 or E4 rows needs one that
  can read a failing runtime."* The class reference goes; the condition becomes re-execution
  itself.
- The floor beneath materiality is unchanged. A command that selected nothing and exited 0, and
  a user-reachable surface nothing reached, stay never-immaterial. Those are the two unknowns
  whose price is always high, and they are already stated as such.

### What belongs to the project

The evidence base attributes part of its arithmetic to *surplus* full-suite rows in the phase
tables — rows whose claim is that nothing else moved. zforge's phase template carries no such
concept: its evidence table is `| Claim | Required | Command / method | Achieved | Artifact |`,
and the Verification Matrix declares classes only. Those rows are the project's, and so is
their removal. Under the new tier 2 they cost their artifact and nothing more.

---

## 2. Absences graduate outward

A phase that walks a journey finds surfaces nothing reaches. Recording one is a finding about
the product, and the phase file is where the recording happens and where a planner cutting the
next feature never looks.

### At the moment of writing

An absence a phase records names what chose it, or says that nothing did. *"There is no
endpoint"* carries no finding. *"There is no endpoint, and decision A120 is why"* and *"there is
no endpoint and no decision names one"* are opposite findings, and only the second is owed to
anyone.

This is one line of guidance in the phase template. It needs no section and no table.

### At feature close

Completion bookkeeping gains a step, ordered before the harness graduation, that reads what the
feature recorded and thinks about three things per absence:

```
CHOSEN   which decision chose this absence?  none -> it is a gap
OWNED    what downstream owns building it?   nothing -> UNOWNED
WHERE    where will the next planner look for this, and is it there?
```

An `UNOWNED` absence becomes a standing flag of kind `OUTWARD`. It closes the way a harness fact
graduates: written into the document the project's own planners read, with that path cited. The
existing bar — *a feature is complete when every phase is COMPLETED and no standing flag is
open* — holds unchanged, and `OUTWARD` needs no exception to it.

zforge names the obligation and demands a landing site. The destination belongs to the project.

### The Standing Flags table

```
| # | Opened | Unmet | Kind | Risk if it stays open | Closes when | Status |
```

`Kind` is `inward` or `OUTWARD`. An inward flag closes on evidence from this feature; an
`OUTWARD` flag closes on a cited destination.

### At the next plan

`/zforge:plan` thinks `UNOWNED` before proposing a phase decomposition: *what does a user need
here that no feature owns — including this one?*

It reaches the prior features' `OUTWARD` flags when `WHERE` put them somewhere a planner reads.
When it does not reach them, `WHERE` was answered wrongly, and the miss is visible at the moment
a planner is deciding what to build.

---

## 3. zforge owns its commits

zforge closes a feature with an uncommitted working tree and no commit step. The commit is then
owned by whatever runs next, and what runs next arrives with its own review, repair and
re-verification loop attached. The two hours measured in the evidence base began four minutes
after terminal closure, from a workflow that treated the commit as its trigger.

zforge makes the commit itself.

### Per phase, at acceptance

The commit is the last act of accepting a phase, after `> Status:` becomes COMPLETED. Every
commit in the history is accepted work: a phase that is rejected or re-run leaves none to
unwind, and the planner already owns the COMPLETED transition and `05_progress_overview.md`.

A phase can be three hours of work. It gets its own commit rather than a share of a
ten-phase diff.

### At closure, the finish marker

Code has landed per phase, so the closing commit carries bookkeeping: final overview status, the
`session_log.md` row, the graduated absences, the graduated harness facts. It is small, and it
is unmistakably the end of the feature — which is what makes any later review or fix commit
separable from it.

### Plain git

The commit is made with `git` directly, never by invoking a commit skill or command —
`commit`, `commit-push-pr`, or any equivalent. Delegating the commit hands the terminal moment
back to another workflow, which is the hole this closes.

### No push

The closing commit is not pushed. A push gate can be a sixteen-minute suite, and a red gate
reopens the feature with nobody present to decide. The completion report names the push and
`/zforge:review` as what is available next, each with its cost, as decisions the user makes.

---

## 4. Artifacts live outside every repo

```
/tmp/zforge/artifacts/{feature}/
    05_04_typecheck.01.txt
    05_10_e2e-full.01.json
```

`{feature}` names the feature — its directory under `docs/`, with any nesting flattened to `-`.
The file name is `{phase}_{what-it-is}.{NN}.{ext}`; the run number lets a second run coexist with
the file an earlier row already quotes. Rows cite the full path.

The location is the same for every repo a feature touches, so the citation rule is one absolute
root. Retention belongs to the operating system.

### What this removes

- `/zforge:plan`'s step that writes a `.zforge/` line into each repo its phases will touch.
- The `.zforge/` directory itself, and the safeguard that kept it out of a commit.
- The reasoning that placed an artifact in *the repo whose code the command exercised*.
- The two-shape citation rule — `.zforge/artifacts/…` for a single-repo workspace,
  `director-console/.zforge/artifacts/…` for a workspace of several.

### The exposure, and its price

An artifact is written by a phase and read by that phase's acceptance, which follows it closely.
The reader that can arrive later is `/zforge:review`, and its contract already reads rows against
a closed feature. Where a restart removes an open phase's artifacts before acceptance runs, tier
1 finds them missing and the rows re-execute — one phase's commands, at a frequency the run can
absorb.

---

## Surfaces

Both Claude and Codex copies, for every surface that carries one.

| Change | Files |
|---|---|
| Tier 2 | `skills/feature-execution/SKILL.md`, `agents/acceptance-agent.md`, `codex/skills/acceptance-agent/SKILL.md` |
| Absences | `skills/feature-execution/SKILL.md`, `templates/05_progress_overview.md`, `templates/05_progress/05_XX_phase_template.md`, `commands/plan.md`, `codex/skills/plan/SKILL.md`, `skills/template-conventions/SKILL.md`, `skills/template-conventions/references/full-template.md` |
| Commits | `skills/feature-execution/SKILL.md`, `commands/feature-orchestrate.md`, `codex/skills/feature-orchestrate/SKILL.md`, `commands/feature-resume.md`, `codex/skills/feature-resume/SKILL.md` |
| Artifacts | seventeen files name `.zforge` and each is edited: `README.md`, `agents/acceptance-agent.md`, `agents/phase-agent.md`, `codex/skills/acceptance-agent/SKILL.md`, `codex/skills/phase-agent/SKILL.md`, `codex/skills/plan/SKILL.md`, `codex/skills/review/SKILL.md`, `commands/plan.md`, `commands/retro.md`, `commands/review.md`, `skills/feature-execution/SKILL.md`, `skills/retro/SKILL.md`, `skills/retro/references/scoring.md`, `skills/template-conventions/SKILL.md`, `skills/template-conventions/references/evidence-scale.md`, `skills/template-conventions/references/full-template.md`, `templates/05_progress/05_XX_phase_template.md`. `docs/evidence-artifacts-outside-the-docs-tree.md` names it too and is left as written — a superseded document is the record of what was decided, not a file to correct. |
| Version | `.claude-plugin/plugin.json` → 4.3.0 |
