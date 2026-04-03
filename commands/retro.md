---
description: Evaluate zforge's workflow performance on a feature — scores and findings for plugin improvement
argument-hint: <feature-name>
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(git:*), Bash(mkdir:*), Bash(ls:*)
model: opus
---

# /retro — Zforge Workflow Retrospective

Evaluate how well zforge's workflow scaffolding served a feature. Output feeds plugin improvement, not project documentation.

## Arguments

- `$1`: Feature name (snake_case or will be converted)

## Pre-flight

1. Convert feature name to snake_case.
2. Read `docs/{feature_name}/session_log.md`. If not found or empty (no entries), **stop**: "No session history to evaluate. Run /retro at the end of a working session."
3. Check current session context. If this is a fresh session with no substantial conversation about the feature (no prior tool calls touching feature files, no implementation discussion), **stop**: "Run /retro at the end of a working session, not in a fresh one. The retro needs session context to evaluate zforge's performance."
4. `mkdir -p docs/{feature_name}/.zforge-retro`

## Step 1: Gather Data

Read these sources from `docs/{feature_name}/`:

1. **`session_log.md`** — session count, which sessions touched which phases
2. **`05_progress_overview.md`** — phase structure, status
3. **All `05_progress/05_XX_*.md`** — session logs, blockers, questions, errors
4. **Template files (`00`-`09`)** — scan which sections have real content vs empty/N/A
5. **`git log`** on the feature docs directory — plan revision history, frequency of changes
6. **`git log`** on source files created/modified by this feature (from phase file "Files Created/Modified" tables) — post-completion fixes

## Step 2: Score Each Dimension

Load `${CLAUDE_PLUGIN_ROOT}/skills/retro/references/scoring.md` for the rubric.

Score each of the five dimensions (1-10):
- **Template quality** — templates matched vs mismatched the work
- **Guidance accuracy** — scaffolding supported vs hindered the LLM
- **Convergence** — session efficiency relative to feature complexity
- **Friction** — following vs fighting the workflow
- **Simplicity** — right-sized vs over-scaffolded

For each score, write a brief note explaining the rating.

**Scope check:** Before recording any observation, ask: "Is this a zforge workflow issue, or an LLM reasoning / project difficulty issue?" If the latter, discard it.

## Step 3: Identify Findings

Review the scored dimensions. For any score <= 5, or any notable observation regardless of score:

1. Identify the specific zforge artifact involved (template, convention, file structure, command)
2. Gather concrete evidence — file names, section content, session interactions
3. Draft the finding with evidence and an example from the session
4. Check the finding quality gate: can it cite specific evidence? If not, drop it.
5. Write an actionable suggestion — what specific change to zforge would address this?

If no findings meet the quality gate, that's fine. Most retros should be scores-only.

## Step 4: Write Output

Write to `docs/{feature_name}/.zforge-retro/{session_id}.md` using the format defined in the retro skill.

Include:
- Header with feature name, session ID, date, session count, overall score
- Score table with per-dimension ratings and notes
- Findings section (only if findings exist)
- Suggested Plugin Changes section (only if findings warrant commits)

## Step 5: Report

Present a brief summary to the user:
- Overall score
- Any findings worth acting on
- If findings suggest plugin changes, mention they can be contributed as PRs to the zforge repo
