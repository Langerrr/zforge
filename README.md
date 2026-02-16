# zforge

Template-aware development workflow plugin for Claude Code.

## Commands

| Command | Description |
|---------|-------------|
| `/plan <name> [--spec file]` | Interactive planning — discovery, codebase exploration, architecture design, writes template files |
| `/compare <name>` | Parallel architecture comparison — spawns agents with different trade-off focuses |
| `/plan-status` | Show feature status for all plans under the current workspace |
| `/review [scope]` | Multi-reviewer code review with two-stage verification and confidence scoring |
| `/track <name>` | Show/update progress for a feature |
| `/feature-resume <name>` | Resume implementation on an existing feature |
| `/feature-orchestrate <name>` | Autonomous multi-phase execution with signal monitoring |

## Agents

| Agent | Used By | Purpose |
|-------|---------|---------|
| `code-architect` | `/compare` | Parallel architecture proposals with different trade-offs |
| `code-reviewer` | `/review`, `/feature-resume` | Confidence-scored code review (>=80 threshold) |
| `phase-agent` | `/feature-orchestrate` | Isolated phase implementation agent |

## Template Structure

`/plan` writes persistent artifacts to `docs/{feature_name}/` in the project:

```
docs/{feature_name}/
├── 00_design_spec.md              # Requirements (generated interactively or from --spec)
├── 01_context.md                  # Feature context, key decisions, architecture
├── 02_plan.md                     # Technical implementation plan with phases
├── 03_integration_summary.md      # Integration points and dependency map
├── 04_integration_plan.md         # Detailed integration steps
├── 05_progress_overview.md        # Phase status summary (planner-owned)
├── 05_progress/
│   ├── 05_00_agent_prompts_index.md  # Agent prompt registry
│   ├── 05_XX_phase_name.md       # Per-phase progress files
│   └── review.md                  # Compiled reviews (planner append-only)
├── 06_post_deployment.md          # Post-deployment checklist
├── 07_testing_overview.md         # Testing strategy overview
├── 07_testing/
│   ├── 07_01_test_plan.md         # Detailed test plan
│   ├── 07_02_test_scripts.md      # Test script specifications
│   └── 07_03_test_results.md      # Test execution results
├── 08_configuration.md            # Configuration and environment setup
├── 09_troubleshooting.md          # Issues and solutions
├── 10_refactor_spec.md            # [Refactoring] Goals, scope, what's changing
├── 11_refactor_context.md         # [Refactoring] Current-state audit
└── 12_refactor_plan.md            # [Refactoring] Migration/refactoring steps
```

## Scaling Model

| Task Size | Commands | Template Overhead |
|-----------|----------|-------------------|
| Bug fix | Planning mode + `/review` | Zero files |
| Small feature | `/plan` (light) + implement + `/review` | 3 files (00, 01, 02) |
| Medium feature | `/plan` + `/track` + `/review` | 5 files + progress dir |
| Large feature | `/plan` → `/feature-orchestrate` | Full template |

## Installation

```bash
claude --plugin-dir /path/to/zforge
```

Or add to a marketplace for team distribution.
