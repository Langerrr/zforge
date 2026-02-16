---
description: Autonomous multi-phase feature execution with signal monitoring
argument-hint: <feature-name>
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/*), Bash(rm -f *), Bash(kill:*), Bash(mkdir:*), Bash(ls:*), Bash(find:*), Task
model: opus
---

# /feature-orchestrate — Autonomous Feature Execution

Run autonomous multi-phase feature execution. Spawns isolated implementation agents for each phase, monitors progress via signals, and drives to completion.

## Arguments

- `$1`: Feature name (snake_case or will be converted)

## Pre-flight

1. Convert feature name to snake_case.
2. Read `docs/{feature_name}/05_progress_overview.md`. If not found, report error and suggest `/plan`.
3. Read `docs/{feature_name}/01_context.md` and `docs/{feature_name}/02_plan.md`.
4. Read `docs/{feature_name}/05_progress/05_00_agent_prompts_index.md`.
5. Create scratchpad directory: `mkdir -p /tmp/zforge-{feature_name}`

## Step 1: Assess Phase Readiness

For each phase in `05_progress_overview.md`:
- **COMPLETED**: Skip
- **READY**: All dependencies met (previous phases completed), can spawn
- **WAITING**: Dependencies not yet met
- **IN_PROGRESS**: Agent already running (check PID file)

## Step 2: Spawn Agents for READY Phases

For each READY phase:

1. Read the phase file (`05_progress/05_XX_*.md`)
2. If `## Agent Prompt` section is empty, fill it in based on `02_plan.md`
3. Build the full prompt:
   - Include the phase file content
   - Append orchestration rules suffix (below)
4. Write prompt to `/tmp/zforge-{feature_name}/05_XX.prompt.md`
5. Spawn: `${CLAUDE_PLUGIN_ROOT}/scripts/spawn-agent.sh <working_dir> <prompt_file>`
6. Update `05_00_agent_prompts_index.md` with "In Progress" status

**Orchestration suffix appended to every agent prompt:**
```
---
ORCHESTRATION RULES — DO NOT IGNORE:

1. You may ONLY update your assigned phase file: {phase_file_path}
2. Do NOT update 05_progress_overview.md — only the planner does that.
3. For package manager commands (install/build), use {plugin_root}/scripts/safe-run.sh <lock_name> <command> to prevent conflicts with parallel agents.
4. Before signaling DONE, write a summary in the ## Review section of your phase file.
5. When you complete ALL tasks in your checklist, write your signal at the end of your phase file, then stop.
6. When you have a question or need a decision, write it in ## Questions, then write your signal, then stop.
7. If you encounter an unrecoverable error, document it in ## Errors, then write your signal, then stop.
8. Update the checklist as you complete each item.
9. Only write ONE signal. Once you write a signal, STOP working immediately.
10. Signal format: `<!-- AGENT_SIGNAL:{STATUS} T:{TIMESTAMP} PID:{PID} -->` where:
    - STATUS is DONE, PAUSED, or FAILED
    - TIMESTAMP is ISO 8601 UTC (run: `date -u +%Y-%m-%dT%H:%M:%SZ`)
    - PID: read from `{phase_file_path}.pid` (run: `cat {phase_file_path}.pid 2>/dev/null || echo $$`)
    - Example: `<!-- AGENT_SIGNAL:DONE T:2026-02-09T19:30:45Z PID:12345 -->`
---
```

Spawn multiple independent phases in parallel if they have no dependencies on each other.

## Step 3: Monitor Loop

Start the monitor:
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/monitor.sh "docs/{feature_name}/05_progress" 30
```

Run this as a background task. Then poll for output using TaskOutput with `block=true` and `timeout=120000`.

### Signal Handling

**DONE**:
1. Read completed phase file — verify `## Review` is filled and checklist is complete
2. Clean up: `rm -f docs/{feature_name}/05_progress/05_XX_*.md.pid`
3. Update `05_progress_overview.md` — mark phase complete
4. Update `05_00_agent_prompts_index.md`
5. Append review summary to `10_review.md`
6. Check if new phases are now READY (dependencies met)
7. If yes: spawn agents for newly READY phases (go to Step 2)
8. Restart monitor

**PAUSED**:
1. Read phase file's `## Questions` section
2. Analyze question in context of the feature plan
3. If you can answer confidently: write answer in phase file, re-spawn agent
4. If unsure: ask the user, then write answer and re-spawn
5. Restart monitor

**FAILED**:
1. Read phase file's `## Errors` section
2. Report failure to user with full context
3. **STOP the orchestration loop** — user must decide next steps

**ORPHANED** (process dead, no signal):
1. Read phase file and check checklist completion
2. If mostly done: treat as DONE — verify and clean up
3. If partially done: re-spawn agent to continue
4. If nothing done: STOP — likely a systemic issue

**WORKING** (file modified recently, no signal):
1. Agent is alive and working — restart monitor and wait

**STALE** (file unchanged 5+ minutes):
1. Check if PID is still alive
2. If dead: treat as ORPHANED
3. If alive: restart monitor, wait longer

**Timeout** (no monitor output in 2 minutes):
1. Restart monitor and continue

## Step 4: Completion

When all phases are complete:
1. Update `05_progress_overview.md` with final status for all phases
2. Create `06_post_deployment.md` if it doesn't exist
3. Extract troubleshooting notes to `09_troubleshooting.md`
4. Clean up: `rm -rf /tmp/zforge-{feature_name}`
5. Remove any remaining `.pid` files
6. Report summary to user:
   - Phases completed
   - Total files created/modified (from phase files)
   - Any deferred items
   - Suggest: `/review --feature {name}` for final review
