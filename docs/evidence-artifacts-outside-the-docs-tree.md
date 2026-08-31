# Evidence artifacts live outside the documentation tree

**Status:** design, for v4.2.0
**Supersedes:** the *"committed artifact"* requirement introduced in
`acceptance-by-risk-and-judgment.md` §5
**Evidence base:** `ai-video-docs/creator-platform/director-console/` — 68 artifact files,
1.4M, committed into a 7.5M prose repository over a single feature.

---

## What was missing

v4.1.0 told phases to write evidence rows from the artifacts their commands wrote, and to
commit those artifacts. It never said where an artifact goes. The nearest thing to a location
was an illustrative filename, `reports/smoke.03.json`.

Agents settled on `05_progress/artifacts/{phase}_{name}.{NN}.{ext}` inside the feature's
documentation directory, and the naming half of that was better than what the plugin
specified. The location half put raw command output — JSON traces up to 184K, ndjson, logs —
into the tree that exists to hold prose.

## The location

```
{repo whose code the command exercised}/.zforge/artifacts/{feature}/
    05_04_typecheck.01.txt
    05_10_e2e-full.01.json
```

`{feature}` names the feature — its directory under `docs/`, with any nesting flattened to `-`,
so one repo can hold artifacts for several concurrent features without collision. The file name
is `{phase}_{what-it-is}.{NN}.{ext}`; the run number is what lets a second run coexist with the
file an earlier row already quotes.

The artifact goes to the repo the command ran in, because that is where the command's output
lands without anyone constructing a path. A workspace whose documentation is a sibling
repository — the shape that produced the evidence base — needs no `../..` to make this work.

## Rows cite a path relative to the workspace root

`.zforge/artifacts/creator-platform/05_10_e2e-full.01.json` where the workspace is one repo;
`director-console/.zforge/artifacts/creator-platform/05_10_e2e-full.01.json` where it is
several. One rule covers both, it needs no syntax of its own, and it is already the root the
orchestrator runs from.

## Untracked, with a stated lifetime

`.zforge/` is gitignored, and `/zforge:plan` puts that line in each repo its phases will
touch. Completion drops `.zforge/artifacts/{feature}/`.

The requirement being retired was carrying an anti-fabrication load: a figure with nothing
behind it should be catchable. It is — at acceptance, which reads every row against its
artifact before the phase closes. That is the moment the check bites, and it does not need
the file to survive the moment. What survives is the row: its finding, its figure, and the
path the figure came from.

So the rule is now that the artifact exists when acceptance reads it, and the row was written
from it.

## What this costs

A reader who wants the full artifact of a closed feature cannot open it, and re-running the
command is the only recourse. The row's finding is what stands. `/zforge:review` checks named
artifacts while the feature is open; against a closed one it reads rows.

## Surfaces

Both `phase-agent` copies, both `acceptance-agent` copies, both `review` copies, both `plan`
copies, `feature-execution/SKILL.md`, `template-conventions/SKILL.md` with
`references/full-template.md` and `references/evidence-scale.md`,
`templates/05_progress/05_XX_phase_template.md`, and `skills/retro/references/scoring.md`.

`full-template.md` §Where artifacts live is the canonical statement; every other surface
states what its reader needs and points there.

## Unchanged

Rows are still written when their commands run, from the artifact. Artifacts are still named
per run. A figure presented as a measurement still appears verbatim in its artifact or the row
says it cannot. The two-tier acceptance bar, the materiality test and the floor are untouched.
