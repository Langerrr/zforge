# Acceptance writes the verdict

**Status:** design, for v4.4.0
**Supersedes:** the `## Acceptance` prose contract in `prompts-instead-of-mandates.md` §1 and
`acceptance-by-risk-and-judgment.md`; the planner-only ownership of `07_harness_conventions.md`
**Evidence base:** `tuurny/autoproto/docs/cutting_prototype/camera_image_geometry_spike/05_progress/05_01_*.md`
— six acceptance tables and eleven session-log rows for one three-row phase;
`tuurny/cutting-fleet/docs/002_03_recorded_workflow/session_log.md` — fifteen rows for two phases,
each a paragraph, and a feature whose owner switched acceptance off mid-run for its cost;
`/tmp/zforge/artifacts/cutting_migration/` — 11,518 files and 217 MB for one phase in progress,
and `recorded_workflow/` at 469 MB after W3, most of it pytest base-temp trees placed inside the
artifact directory; `cutting-fleet` commit `3e5e2b9` — one phase's acceptance commit touching
thirty-nine files, thirty of them documents in other features;
`tuurny/_retro_notes/cut_workflow_codex_migration.md` — five plugin changes proposed on 2026-08-24
and not yet made.

---

## The principle

Acceptance produces one verdict per row and a pointer to what holds it. Everything else it
writes today is a second copy of something already on disk.

The verification half of acceptance was cut to size in 4.2 and 4.3 and is not the cost now. The
cost is the writing that follows the verdict: a fresh narrative of the table the acceptance agent
just returned, a paragraph saying nothing was promoted, a session-log row per event rather than
per session, two overview tables that restate the phase files, and a copy of every harness fact
through the planner. A phase reopened for a small fix pays all of it again in full — the spike
phase above carries six complete acceptances for three evidence rows.

Each change below removes a copy. Where a step existed so the planner would hold something, the
thing now lives where it was produced and the planner points at it.

---

## 1. The acceptance section is the report

`## Acceptance` is the acceptance report, as returned, followed by one line of adjudication.

```
## Acceptance

<the report, verbatim — PHASE, ROWS, the table, VERDICT, RATIONALE, FLOOR, PLAN DRIFT,
 UNVERIFIABLE, MISSING FILES, HARNESS, NOTES>

ADJUDICATED: ACCEPT — 2026-09-15 — <one sentence only where the planner departs from the
recommendation, and why>
PROMOTED: D3, D7 | none
```

The planner writes nothing else here. Where the planner verifies in-session rather than
delegating, it writes the same report shape — the shape is the contract, whoever fills it.

The report's RATIONALE paragraph is where the reasoning behind a row accepted below its class
lives. It is written once, by the party that watched the check run, and it is not restated.

### Re-acceptance is a delta

A phase reopened after acceptance — a review finding, a fix, a rejected decision — is
re-accepted for the rows the change touched. The record is one line under the existing report:

```
RE-ACCEPTED: 2026-09-04 — rows 1, 3 re-verified from /tmp/zforge/artifacts/{feature}/05_01_e1.04.xml
and 05_01_e4.04.xml; row 2 unchanged
```

The acceptance agent takes the list of touched rows in its spawn message and verifies those.
A change that touches every row, or that the planner cannot bound to rows, is a new acceptance
and gets a new report beneath the old one.

---

## 2. One log row per session

A session-log row records a session, not an event. The phase file's `## Session Log` gets one
row when the agent stops — its report lines, written by the agent before it sets REPORTED —
and one when the planner accepts. `session_log.md` gets one row per session, written at the
end of the session, and carries nothing above its table.

Milestones, pauses, adjudications, resumes and repairs are not rows. Each already has a home:
`## Open Items` for the question and its resolution, `## Resume Point` for where an agent
stopped, `## Acceptance` for the verdict, `decision_review.md` for what the user must answer.

`05_progress_overview.md` loses `## Session Log (All Phases)` and `## Files Modified (All
Phases)`. No command reads either, and both restate the phase files row for row. At acceptance
the planner touches the overview at the phase's status row and the Quick Status counts, and at
Standing Flags only when one opens or closes.

---

## 3. Promotion is a lookup

### Decisions carry their reach

The phase agent knows, at the moment it records a decision, whether the decision contradicts a
design document, asserts something the domain model does not define, or hands an obligation to
a later feature. `## Decisions` gains a `Reach` column: `feature` by default, `outward` for a
decision that does. The report's DECISIONS line reads `DECISIONS: 9 (2 outward)`.

At acceptance the planner promotes the `outward` rows and names them on the `PROMOTED:` line.
It does not read the `feature` rows. Where a promoted row turns out to bind only this feature,
that is one line in `decision_review.md`'s adjudication, not a reason to read every decision on
every phase.

### The harness file is shared

`07_harness_conventions.md` is written by whoever learns the fact, at the moment of learning it:

- The **phase agent** appends a row when a command costs it a run to understand. The
  `kind: harness` decision row is retired — the harness file is the record, and a decision
  row that said "see the harness file" would be the copy this design removes.
- The **acceptance agent** appends a row for anything its HARNESS line would have reported.
  This is the one file it may write. Its HARNESS line stays in the report, now as the list of
  rows it appended, so the planner sees what changed without opening the file.
- The **planner** reads it before writing a Verification Matrix and graduates it at feature
  close. It no longer copies rows into it.

One agent holds a phase at a time under the default sequential schedule, and the file is
append-only rows, so shared ownership costs nothing there. Under a parallel schedule the file
is a collision surface like any other and is named as one in `session_log.md`'s parallelism
note.

---

## 4. An artifact is the output, not the state

An artifact is the smallest file that carries every figure its row quotes: the runner's log or
XML, the JSON a script printed, the screenshot a surface check took. It is one file per row per
run, named `{phase}_{what}.{NN}.{ext}`, and it is never a directory.

What a command *produced* — a worker's data directory, a database, a HAR, a trace archive, a
fixture tree, a test runner's base-temp directory — stays where the command put it, or goes to
a scratch path outside the artifact directory. A row that needs a reader to see such state
cites its path in place, beside the artifact that carries the figures. Copying it under
`/tmp/zforge/artifacts/` makes the tier-1 check a search across thousands of files for a number
the row could have carried in a twenty-line log.

The row quotes what the check produced: the count, the exit code, the duration, the one figure
the claim rests on. A row whose achieved cell runs to a paragraph is quoting the artifact rather
than pointing at it.

Tier 1 is unchanged — every quoted figure appears verbatim in the artifact — and this is what
makes it cheap again.

---

## 5. Acceptance discovers the environment

Before reporting a row `UNVERIFIABLE` because its command is not on the PATH, the acceptance
agent reads the applicable repository instructions — `AGENTS.md`, and `CLAUDE.md` where present,
for the project and its parents up to the workspace root — and looks for the documented
interpreter, then `.venv/bin/`, then `../.venv/bin/`. A command found by one of these is run
and the report's Command column names the path it ran under. `UNVERIFIABLE` is for a command
that none of these resolves.

---

## 6. The agent sets REPORTED; only acceptance sets COMPLETED

The phase agent's last act is to set `> Status:` to the state it is reporting — REPORTED with
DONE, PAUSED with PAUSED, FAILED with FAILED — after its report lines are in `## Session Log`.
Both are on disk before the report leaves the agent, so a planner that never receives it finds a
phase that says on disk exactly what is true of it. The planner's checkpoint edit goes away.

COMPLETED is set by acceptance and by nothing else. An agent that sets it has claimed its own
acceptance, and the planner resets the header to REPORTED and records the claim as plan drift.

Stated in both the phase-agent surfaces and the execution skill, in those words.

---

## 7. Feature directories resolve below `docs/`

Pre-flight resolves `docs/{feature_name}/` first. Where that is absent, it searches
`docs/**/{feature_name}/` for a directory of exactly that name, takes a unique match, reports the
resolved path, and uses it for the rest of the run. Two matches is an error naming both.

---

## 8. Timing is a collision surface

A broad verification gate run while a heavy implementation agent is active shares the CPU with
it, and a timing-sensitive test fails under that load without anything being wrong. Scheduling
names this beside write collisions: run broad gates from a quiet state, and re-run a
timing-shaped failure from one before classifying it.

---

## 9. Harness instruction files across hosts

A plan's `## Required Context` may name `CLAUDE.md`. Where it names the harness instruction
file, a Codex run reads `AGENTS.md` at the same path. Where it names a product artifact that
happens to be called `CLAUDE.md`, that file is read as written. The planner tells the two apart
by what the row says the file is for, and does not rename either.

---

## 10. The planner asks which models to spawn

Pre-flight asks the user, once per run, which model implements and which model accepts, and
records both in this session's `session_log.md` row. A resumed run reads the previous row and
proposes the same pair; the user confirms or changes it.

The question comes with a proposal rather than an empty field. Implementation proposes the
session's own model. Acceptance proposes a cheaper one: tier 1 is arithmetic against files, and a
pass that re-executes needs a model that can read a failing runtime, not the strongest one
available. Where the harness offers no model choice for subagents, pre-flight says so and moves
on.

The spawn message and the acceptance delegation carry the chosen model. In Claude Code that is
the `model` parameter on the Agent tool; in Codex it is the subagent's model setting. Neither
agent definition pins a model — `model: inherit` stays, and the planner passes the choice.

---

## Surfaces

Both Claude and Codex copies, for every surface that carries one.

| Change | Files |
|---|---|
| §1 Acceptance section | `skills/feature-execution/SKILL.md`, `agents/acceptance-agent.md`, `codex/skills/acceptance-agent/SKILL.md`, `templates/05_progress/05_XX_phase_template.md`, `skills/template-conventions/references/full-template.md`, `commands/feature-resume.md`, `codex/skills/feature-resume/SKILL.md` |
| §2 Session logs, overview tables | `skills/feature-execution/SKILL.md`, `templates/05_progress_overview.md`, `templates/session_log.md`, `templates/05_progress/05_XX_phase_template.md`, `agents/phase-agent.md`, `codex/skills/phase-agent/SKILL.md` |
| §3 Reach column, shared harness file | `templates/05_progress/05_XX_phase_template.md`, `templates/07_harness_conventions.md`, `agents/phase-agent.md`, `codex/skills/phase-agent/SKILL.md`, `agents/acceptance-agent.md`, `codex/skills/acceptance-agent/SKILL.md`, `skills/feature-execution/SKILL.md`, `skills/template-conventions/SKILL.md`, `skills/template-conventions/references/full-template.md` |
| §4 Artifacts | `agents/phase-agent.md`, `codex/skills/phase-agent/SKILL.md`, `templates/05_progress/05_XX_phase_template.md`, `skills/template-conventions/references/evidence-scale.md`, `skills/template-conventions/references/full-template.md` |
| §5 Environment discovery | `agents/acceptance-agent.md`, `codex/skills/acceptance-agent/SKILL.md` |
| §6 State ownership | `agents/phase-agent.md`, `codex/skills/phase-agent/SKILL.md`, `skills/feature-execution/SKILL.md`, `commands/feature-orchestrate.md`, `codex/skills/feature-orchestrate/SKILL.md`, `templates/05_progress_overview.md` |
| §7 Directory resolution | `commands/feature-orchestrate.md`, `codex/skills/feature-orchestrate/SKILL.md`, `commands/feature-resume.md`, `codex/skills/feature-resume/SKILL.md`, `commands/track.md`, `codex/skills/track/SKILL.md` |
| §8 Timing collision | `skills/feature-execution/SKILL.md` |
| §9 Instruction files | `codex/skills/feature-orchestrate/SKILL.md`, `codex/skills/feature-resume/SKILL.md` |
| §10 Model choice | `skills/feature-execution/SKILL.md`, `commands/feature-orchestrate.md`, `codex/skills/feature-orchestrate/SKILL.md`, `commands/feature-resume.md`, `codex/skills/feature-resume/SKILL.md`, `templates/session_log.md` |
| Tests | `tests/test_plugin_surfaces.py` — three assertions still name the 4.2 tier-2 heading and the pre-4.3 artifact path, and fail at HEAD; they are brought to the current contract and the acceptance-section shape is added to the both-hosts check |
| Version | `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json` → 4.4.0 |
