# zforge

The durable state, contract and evidence layer for multi-session feature work in Claude Code.

zforge carries what must be true before a phase closes, what evidence proves it, what was decided along the way, and what is still open. It does not carry methodology — discovery belongs to `superpowers:brainstorming`, test discipline to `superpowers:test-driven-development`, debugging rigour to `superpowers:systematic-debugging` and `ce:debug`, general code review to `/code-review` and `ce:review`. zforge names those where they apply and owns none of them.

## Commands

| Command | Description |
|---------|-------------|
| `/zforge:plan <name> [--spec file]` | Resolve a completeness contract, then write the artifact tree |
| `/zforge:feature-orchestrate <name>` | Autonomous multi-phase execution with evidence-based acceptance |
| `/zforge:feature-resume <name>` | Interactive implementation with check-ins between phases |
| `/zforge:review --feature <name>` | Check the implementation against the feature's own ledger |
| `/zforge:debug` | Route a concrete failure through the right debugging methodology |
| `/zforge:track <name>` | Progress, standing flags, and decisions awaiting review |
| `/zforge:plan-status` | Feature status across the workspace |
| `/zforge:retro <name>` | Score zforge's own performance on a completed feature |

## How it works

**Planning stops when a contract is full**, not when the model runs out of questions. `/plan` resolves sixteen items — intent, ground, shape, handoff — attempting each from the codebase, the docs, and what you have already said before it asks you anything. Where the attempt succeeds it proposes rather than asks, because correcting a proposal costs you recognition while answering a question costs you generation.

**Phases declare their acceptance bar before they run.** `02_plan.md` carries a Verification Matrix: for every phase, which classes of evidence its gate will and will not cover. A column that is empty across every phase with a user-facing surface is a hole you can see at planning time rather than after the last phase.

**Acceptance means re-running the commands.** An agent's green report is a claim; the planner independently re-runs the phase's evidence commands and compares the class achieved against the class required. Where it falls short, a standing flag opens with a stated *closes when*, and the feature is not complete while any flag is open.

**Decisions do not block.** Agents decide, record, and keep moving; every decision lands in `decision_review.md` as 🟡 for you to approve or reject whenever you choose. Blocking is reserved for five named pause triggers.

**Interrupted work is resumed, not restarted.** A phase agent killed by a usage limit is resumed from its own transcript with a mandatory re-orientation against disk — `git status`, re-run the tests, diff the checklist against what exists — because its memory of what it wrote is less reliable than the working tree.

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

| Task | Commands | Overhead |
|------|----------|----------|
| Bug fix | `/zforge:debug` | No files |
| Small feature | `/zforge:plan` + implement | `00`, `01`, `02` |
| Medium feature | `/zforge:plan` → `/zforge:feature-resume` → `/zforge:review` | Full core set |
| Large feature | `/zforge:plan` → `/zforge:feature-orchestrate` → `/zforge:review` | Core set + per-phase evidence |

A phase that genuinely only needs unit tests declares E1, closes on a one-line re-run, and gets no ceremony. The matrix is what lets cheap phases stay cheap.

## Skills

| Skill | Purpose |
|-------|---------|
| `template-conventions` | Structure, ownership, evidence scale, naming — the source of truth |
| `feature-execution` | Phase state, spawning, recovery, scheduling, acceptance |
| `async-reasoning` | Designing state layers over async data flows |
| `retro` | Scoring zforge's own workflow performance |

## Installation

```bash
git clone https://github.com/Langerrr/zforge.git
claude --plugin-dir ./zforge
```
