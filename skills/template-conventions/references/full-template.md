# Zforge Template — Full Reference

This document contains the complete template specification for zforge feature documentation.

## Complete File Structure

```
docs/{feature_name}/
├── 00_design_spec.md              # Requirements, architecture, constraints, risks
├── 01_context.md                  # Feature context, key decisions, architecture overview
├── 02_plan.md                     # Technical plan: schema, endpoints, phases, file structure
├── 03_integration_summary.md      # API types, mapping, frontend files (if frontend involved)
├── 04_integration_plan.md         # Step-by-step frontend integration guide
├── session_log.md                 # Which Claude Code sessions touched this feature
├── 05_progress_overview.md        # Phase status summary (PLANNER ONLY)
├── 05_progress/
│   ├── 05_00_agent_prompts_index.md  # Phase index and agent rules
│   ├── 05_01_{phase_name}.md         # Phase 1 progress
│   ├── 05_02_{phase_name}.md         # Phase 2 progress
│   ├── 05_XX_{phase_name}.md         # Additional phases
│   └── review.md                     # Compiled agent reviews (planner append-only)
├── 06_post_deployment.md          # Post-deployment checklist
├── 07_testing_overview.md         # Testing guidance
├── 07_testing/
│   ├── 07_01_test_plan.md         # Test files and cases to create
│   ├── 07_02_test_scripts.md      # Reusable test commands
│   └── 07_03_test_results.md      # Significant test outcomes
├── 08_configuration.md            # Env vars, feature flags, external services
├── 09_troubleshooting.md          # Issues, solutions, debug commands
├── 10_refactor_spec.md            # [Refactoring] Requirements, goals, scope
├── 11_refactor_context.md         # [Refactoring] Current-state audit and dependencies
├── 12_refactor_plan.md            # [Refactoring] Migration/refactoring steps
├── .zforge-retro/                 # Plugin eval artifacts (only if /retro invoked)
│   └── {session_id}.md            # Per-session retro: scores, findings, suggestions
└── _archive/                      # Outdated docs: {name}__{date}.md
```

## File Creation Timeline

### Created by `/plan` (at planning time)
- `00_design_spec.md` — always
- `01_context.md` — always
- `02_plan.md` — always
- `session_log.md` — always
- `05_progress_overview.md` — always
- `05_progress/05_00_agent_prompts_index.md` — always
- `05_progress/05_XX_*.md` — one per phase

### Created during implementation (as needed)
- `03_integration_summary.md` — when frontend work begins
- `04_integration_plan.md` — when frontend work begins
- `06_post_deployment.md` — at feature completion
- `07_testing_overview.md` — when testing starts
- `07_testing/*.md` — as tests are planned and run
- `08_configuration.md` — when config is established
- `09_troubleshooting.md` — as issues are discovered
- `05_progress/review.md` — as phases complete

### Created for refactoring workflows (10+)
- `10_refactor_spec.md` — refactoring requirements and scope
- `11_refactor_context.md` — current-state audit
- `12_refactor_plan.md` — migration/refactoring steps
- Further numbers (13, 14, ...) as needed

## Ownership Matrix

| File | Read | Write | Rule |
|------|------|-------|------|
| `00_design_spec.md` | All | /plan only | Agents do NOT modify unless explicitly told |
| `01_context.md` | All | Planner | Updated when decisions change |
| `02_plan.md` | All | Planner | Updated when scope changes |
| `03_integration_summary.md` | All | Planner | Created before frontend phases |
| `04_integration_plan.md` | All | Planner | Created before frontend phases |
| `05_progress_overview.md` | All | Planner ONLY | **Critical**: prevents race conditions |
| `05_00_agent_prompts_index.md` | All | Planner | Updated per phase lifecycle |
| `05_XX_*.md` | Assigned agent | Assigned agent ONLY | Each agent owns one file |
| `06_post_deployment.md` | All | Planner | Created at completion |
| `07_*` | All | Mixed | Planner creates, agents update |
| `08_configuration.md` | All | Planner | Updated as config emerges |
| `09_troubleshooting.md` | All | Planner | Extracted from agent findings |
| `05_progress/review.md` | Humans | Planner (append) | Planner appends, never reads back |
| `session_log.md` | All | Planner | Tracks which sessions touched this feature |
| `.zforge-retro/*.md` | All | /retro only | Plugin eval artifacts, created on demand |
| `10_refactor_spec.md` | All | Planner | [Refactoring] Requirements, goals, scope |
| `11_refactor_context.md` | All | Planner | [Refactoring] Current-state audit |
| `12_refactor_plan.md` | All | Planner | [Refactoring] Migration/refactoring steps |

## Phase File Sections

Each `05_progress/05_XX_*.md` file contains:

### Agent Prompt
Filled by planner or `/feature-orchestrate` before spawning. Contains:
- Context extracted from `01_context.md`
- Specific scope for this phase
- Files to read
- Commands to run (using safe-run.sh)
- Credentials if needed
- Signal instructions

### Phase Scope
Brief description of what this phase covers.

### Checklist
Actionable items with checkboxes. Agent marks as complete.

### In Progress / Completed
Tracks current and finished work.

### Blocked / Issues
Table: Issue | Step | Description | Resolution

### Files Created/Modified
Table: File | Step | Action (Create/Modify)

### Session Log
Table: Date | Session # | Steps covered | Summary.
A "session" = one agent execution. Multiple sessions per phase are normal.

### Review
Agent writes before signaling DONE:
- What was implemented
- Design decisions made
- Known limitations
- Test results

### Questions / Errors
For PAUSED and FAILED signals respectively.

## Signal Protocol

Implementation agents write exactly ONE signal at the end of their phase file, including a UTC timestamp and their shell PID:

```html
<!-- AGENT_SIGNAL:DONE T:2026-02-09T19:30:45Z PID:12345 -->      All checklist items complete
<!-- AGENT_SIGNAL:PAUSED T:2026-02-09T19:30:45Z PID:12345 -->    Needs input, question in ## Questions
<!-- AGENT_SIGNAL:FAILED T:2026-02-09T19:30:45Z PID:12345 -->    Unrecoverable error, in ## Errors
```

**Why timestamp and PID?**
- **T:** — ISO 8601 UTC timestamp (`date -u +%Y-%m-%dT%H:%M:%SZ`). The monitor ignores signals older than the stale threshold (default 5 min), preventing leftover signals from previous sessions from being picked up.
- **PID:** — Agent's shell PID (`echo $$`). The monitor cross-checks against the `.pid` file written by `spawn-agent.sh`, ensuring a signal from a stale re-spawn is not attributed to the current agent.

After writing a signal, the agent STOPS immediately. No more work.

## Naming Conventions

| Item | Convention | Example |
|------|-----------|---------|
| Feature folder | `snake_case` | `ai_assistant/`, `payment_integration/` |
| Files | Numbered prefix | `01_context.md`, `05_02_backend_api.md` |
| Phase files | `05_XX_description` | `05_01_backend_schema.md` |
| Archive | `{name}__{date}.md` | `02_plan__2026-01-15.md` |

## When to Update Which File

| Scenario | File | Who |
|----------|------|-----|
| New requirement | `00_design_spec.md` | User only |
| Architecture decision | `01_context.md` | Planner |
| Scope change | `01_context.md` + `02_plan.md` | Planner |
| Step completed | `05_XX_*.md` (own phase) | Agent |
| Phase completed | `05_progress_overview.md` | Planner |
| Phase reviewed | `05_progress/review.md` | Planner |
| Bug found | `05_XX_*.md` (Blocked/Issues) | Agent |
| Feature deferred | `06_post_deployment.md` | Planner |
| New env var | `08_configuration.md` | Planner |
| Issue solved | `09_troubleshooting.md` | Planner |
| Doc outdated | Move to `_archive/` | Planner |
