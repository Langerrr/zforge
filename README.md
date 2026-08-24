# zforge

The durable state, contract and evidence layer for multi-session feature work in Claude Code and Codex.

zforge carries what must be true before a phase closes, what evidence proves it, what was decided along the way, and what is still open. It does not carry methodology — discovery belongs to `superpowers:brainstorming`, test discipline to `superpowers:test-driven-development`, debugging rigour to `superpowers:systematic-debugging` and `compound-engineering:ce-debug`, and general code review to the host's code review plus `compound-engineering:ce-review`. zforge names those where they apply and owns none of them.

## Workflows

| Workflow | Claude Code | Codex | Description |
|----------|-------------|-------|-------------|
| Plan | `/zforge:plan <name> [--spec file] [--kind ...]` | `$zforge:plan` or “Use zforge to plan…” | Resolve a completeness contract, then write the artifact tree |
| Orchestrate | `/zforge:feature-orchestrate <name>` | `$zforge:feature-orchestrate` | Autonomous multi-phase execution with evidence-based acceptance |
| Resume | `/zforge:feature-resume <name>` | `$zforge:feature-resume` | Interactive implementation with check-ins between phases |
| Review | `/zforge:review --feature <name>` | `$zforge:review` | Check the implementation against the feature's own ledger |
| Debug | `/zforge:debug` | `$zforge:debug` | Route a concrete failure through the right debugging methodology |
| Track | `/zforge:track <name>` | `$zforge:track` | Progress, standing flags, and decisions awaiting review |
| Status | `/zforge:plan-status` | `$zforge:plan-status` | Feature status across the workspace |
| Retro | `/zforge:retro <name>` | `$zforge:retro` | Score zforge's own performance on a completed feature |

## How it works

**Planning stops when a contract is full**, not when the model runs out of questions. `/plan` resolves seventeen items — intent, ground, shape, handoff — attempting each from the codebase, the docs, and what you have already said before it asks you anything. Where the attempt succeeds it proposes rather than asks, because correcting a proposal costs you recognition while answering a question costs you generation.

**The contract also stops the files.** `--kind requirements` puts only intent and ground on the contract and terminates at a specification; `--kind implementation` puts all four groups on it and terminates at a phase tree. A group that is off the contract asks nothing and writes nothing, so a product-definition session cannot drift into producing a phase graph for work nobody has scoped.

**Phases declare their acceptance bar before they run.** `02_plan.md` carries a Verification Matrix on two axes: **E0–E4** for what will be executed, **J0–J2** for what will be judged — a claim no test runner settles, checked by a stated method against a named referent. A column that is empty across every phase with a user-facing surface is a hole you can see at planning time rather than after the last phase.

**Acceptance means re-running the commands.** An agent's green report is a claim; the planner independently re-runs the phase's evidence commands, re-walks its judgement methods, and compares achieved against required. Where it falls short, a standing flag opens with a stated *closes when*, and the feature is not complete while any flag is open. On a long chain the re-run is delegated to `zforge:acceptance-agent`, because it needs a phase file and a shell rather than the run's accumulated context.

**Decisions do not block, and only the load-bearing ones surface.** Agents decide, record, and keep moving. At acceptance the planner promotes to `decision_review.md` only the decisions reaching beyond the feature's implementation — the rest stay in their phase file. The ledger is a queue you drain, not an index of everything decided. Blocking is reserved for five named pause triggers.

**Interrupted work is resumed, not restarted.** A phase agent killed by a usage limit is resumed from its own transcript with a mandatory re-orientation against disk — `git status`, re-run the tests, diff the checklist against what exists — because its memory of what it wrote is less reliable than the working tree. Agents are told up front to stop cleanly at ~95% of budget, flushing a `## Resume Point` first, which turns the expensive recovery into a cheap one.

**A reported phase is not an accepted phase.** `REPORTED` is its own state: the work is on disk and the evidence has not been re-run. It is written the moment a report arrives, so a planner that dies mid-acceptance leaves a phase that says on disk exactly what is true of it.

## Artifact tree

`/zforge:plan` writes to `docs/{feature_name}/`:

```
docs/{feature_name}/
├── 00_design_spec.md          # Problem, actors, boundary, acceptance vocabulary
├── 01_context.md              # Doc Map, decisions, open questions with owner + method
├── 02_plan.md                 # Phases, Verification Matrix, env assumptions, invariants
├── discussion.md              # Reasoning captured while thinking, not after
├── decision_review.md         # Decisions awaiting review (🟡 → ✅/❌)
├── session_log.md             # Sessions, and how each ended
├── 05_progress_overview.md    # Phase status + standing flags (planner-owned)
└── 05_progress/
    └── 05_XX_{phase}.md       # Contract, evidence, decisions, work log
```

Documents beyond this set are named for what they are, numbered in whatever slot is free, and registered in the Doc Map.

## Scaling

| Task | Claude Code | Codex | Overhead |
|------|-------------|-------|----------|
| Bug fix | `/zforge:debug` | `$zforge:debug` | No files |
| Small feature | `/zforge:plan` + implement | `$zforge:plan` + implement | `00`, `01`, `02` |
| Medium feature | `/zforge:plan` → `/zforge:feature-resume` → `/zforge:review` | `$zforge:plan` → `$zforge:feature-resume` → `$zforge:review` | Full core set |
| Large feature | `/zforge:plan` → `/zforge:feature-orchestrate` → `/zforge:review` | `$zforge:plan` → `$zforge:feature-orchestrate` → `$zforge:review` | Core set + per-phase evidence |

A phase that genuinely only needs unit tests declares E1, closes on a one-line re-run, and gets no ceremony. The matrix is what lets cheap phases stay cheap.

## Skills

| Skill | Purpose |
|-------|---------|
| `template-conventions` | Structure, ownership, evidence scale, naming — the source of truth |
| `feature-execution` | Phase state, spawning, recovery, scheduling, acceptance |
| `async-reasoning` | Designing state layers over async data flows |
| `retro` | Scoring zforge's own workflow performance |
| `plan`, `feature-orchestrate`, `feature-resume` | Codex-native planning and implementation entry points |
| `review`, `track`, `plan-status`, `debug` | Codex-native review, reporting, and debugging entry points |
| `phase-agent`, `acceptance-agent` | Specialized instructions loaded by Codex subagents |

## Specialized agents

| Agent | Purpose |
|-------|---------|
| `zforge:phase-agent` | Implements one phase from its phase file, records decisions and evidence, stops cleanly on budget |
| `zforge:acceptance-agent` | Re-runs a phase's evidence in a clean shell and returns an achieved-class table. Fixes nothing, accepts nothing |

Claude Code loads these from `agents/`. Codex loads the corresponding skills in `skills/` when the orchestration workflow delegates a phase or an acceptance check.

## Installation

### Claude Code

```bash
git clone https://github.com/Langerrr/zforge.git
claude --plugin-dir ./zforge
```

### Codex

The repository includes `.codex-plugin/plugin.json` and a local marketplace definition. Add the repository as a marketplace, install the plugin, then start a new Codex thread so the skills are discovered:

```bash
git clone https://github.com/Langerrr/zforge.git
codex plugin marketplace add /absolute/path/to/zforge
codex plugin add zforge@zforge-local
```

In the Codex app, select `@zforge`; in the CLI or a prompt, invoke a workflow explicitly (for example `$zforge:feature-resume`) or ask naturally: “Use zforge to resume implementation of `<feature>`.”

`superpowers` and `compound-engineering` remain complementary dependencies for discovery, test discipline, debugging, and general review. Install their Codex-compatible plugins when you want those routed workflows available; zforge itself continues to own only durable state, contracts, evidence, and phase execution.
