---
description: Resume implementation on an existing feature
argument-hint: <feature-name>
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion
model: opus
---

# /feature-resume — Resume Feature Implementation

Resume work on an existing feature plan. This runs within the current session using Task tool sub-agents.

## Arguments

- `$1`: Feature name (snake_case or will be converted)

## Process

### 1. Load Feature State

1. Convert feature name to snake_case.
2. Read `docs/{feature_name}/05_progress_overview.md`. If not found, report error.
3. Read `docs/{feature_name}/01_context.md` and `docs/{feature_name}/02_plan.md` for full context.
4. Scan all phase files in `docs/{feature_name}/05_progress/` to determine current state.

### 2. Identify Next Work

Classify each phase:
- **COMPLETED**: Checklist fully done, DONE signal present or verified
- **IN_PROGRESS**: Partially done, no signal (was interrupted)
- **PAUSED**: Has `<!-- AGENT_SIGNAL:PAUSED -->` signal — needs a question answered
- **FAILED**: Has `<!-- AGENT_SIGNAL:FAILED -->` signal — needs error resolved
- **PENDING**: Not started, checklist empty

Priority order:
1. **PAUSED** phases — answer the question first, then resume
2. **FAILED** phases — assess error, decide whether to retry or skip
3. **IN_PROGRESS** phases — continue where it left off
4. **PENDING** phases — start the next one in order

### 3. Handle PAUSED/FAILED

**If PAUSED:**
- Read the `## Questions` section from the phase file
- Present the question to the user
- Write the answer into the phase file
- Clear the PAUSED signal

**If FAILED:**
- Read the `## Errors` section from the phase file
- Present the error to the user
- Ask: fix and retry, skip this phase, or stop?
- Clear the FAILED signal if retrying

### 4. Execute Phase

For the next phase to work on:

1. Read the phase file completely.
2. Read all relevant source files referenced in `01_context.md`, `02_plan.md`, and the phase's checklist.
3. Implement the checklist items one by one.
4. After each significant step:
   - Mark the checklist item as done in the phase file
   - Update the session log
   - Update the files created/modified table
5. When the phase is complete:
   - Write the `## Review` section
   - Update `05_progress_overview.md` with completion status
   - Ask the user: continue to next phase, run `/review`, or stop?

### 5. Between Phases

After completing a phase:
- If the next phase involves a different domain (e.g., switching from backend to frontend), create `03_integration_summary.md` and `04_integration_plan.md` if they don't exist.
- Fill in the `## Agent Prompt` section of the next phase file if empty.
- Ask the user before proceeding to the next phase.

### 6. Completion

When all phases are done:
- Update `05_progress_overview.md` with final status
- Create `06_post_deployment.md` if it doesn't exist
- Extract any issues to `09_troubleshooting.md`
- Suggest running `/review --feature {name}` for a final review
