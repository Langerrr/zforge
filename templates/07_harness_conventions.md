# Harness Conventions — {Feature Name}

> Last updated: {DATE}
> Owner: Planner — promoted from phase `## Decisions` rows marked `kind: harness`

How this project's code is **run and observed**. Facts about the harness, not about the product:
which commands interact, which tear down state, which defaults bound nothing, and which ways an
observation can read as a pass without having checked anything.

Bound into `## Required Context` for every phase whose `## Evidence Required` table names a command.
Read by the planner before writing the Verification Matrix, and by the acceptance agent before it
re-runs anything.

Each row states what is true and what to do about it. A row arrives when a phase pays for it once,
and it is here so no later phase pays for it again.

---

## Commands

<!-- Interactions, side effects, and false greens. The third column is what a phase should do
     differently, stated as an instruction rather than as a warning. -->

| Command | What is true | Write specs accordingly |
|---------|--------------|-------------------------|

<!-- Worked examples of the row shape:

| `pnpm test` | Probes are written and deleted mid-run, so a concurrent `tsc` fails TS6053. Not independent of `typecheck` or `lint` | Run the three serially. A matrix row treating them as independent is wrong |
| `pnpm image:smoke` | Ends in `down()` → `docker rm --force --volumes` | Destroys the corpus. Order it last, and let no other row depend on container state |
| `pnpm test -t <name>` | A filter matching nothing exits 0 | Assert the selected count. Exit code alone cannot tell a pass from an empty selection |

-->

## Test harness

<!-- Framework defaults and lifecycle facts — what runs before what, what inherits what,
     and where an exception is swallowed. -->

| What is true | Write specs accordingly |
|--------------|-------------------------|

<!-- Worked examples:

| `use.actionTimeout` defaults to `0` — no bound. A `click()` on an absent control waits out the whole test timeout | Set an explicit `actionTimeout`. A hung run means a missing control, not a slow one |
| `page.addInitScript` runs before `document.documentElement` necessarily exists, and an init script's exception does not fail the navigation | Guard the observe target. A watch reporting nothing and a watch that never ran read identically |
| `browser.newContext()` inherits the project's `use` options | Name the storage state explicitly, or a second context arrives holding the suite's session |

-->

## Destructive steps

<!-- Commands the acceptance agent must not re-run outside an isolated worktree.
     This is the list that makes the side-effect guard enforceable — a teardown looks like
     any other command until it is named here. -->

| Command | What it destroys | Which rows depend on it |
|---------|------------------|-------------------------|

---

## Graduation

At feature completion the planner writes the facts **still true**, in their simplest final form,
into the project's conventions document. A fact a later phase made obsolete does not graduate, and
neither does the account of how one was learned.

This file accumulates what the run learned. The project file states what is true of the harness now.
