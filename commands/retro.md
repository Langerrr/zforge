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

## Run the retro

Invoke the `zforge:retro` skill. The skill owns the scope boundary, NOT-DO rules, data sources, scoring rubric, finding quality gate, and output format — this command does not duplicate them.

Apply the skill to feature `$1` and write its output to `docs/{feature_name}/.zforge-retro/{session_id}.md`.

## Report

Present a brief summary to the user:
- Overall score
- Any findings worth acting on
- If findings suggest plugin changes, mention they can be contributed as PRs to the zforge repo
