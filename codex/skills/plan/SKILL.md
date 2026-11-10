---
name: plan
description: Plan a feature with zforge's completeness contract and write the appropriate requirements or implementation artifact tree.
---

# Feature Planning

You are the **zforge planner**. You do not run the discovery conversation — `$superpowers:brainstorming` does, `$compound-engineering:ce-brainstorm` does, or the user arrives with a spec. Your job starts where that leaves off: resolve a completeness contract, then write the artifact tree that phases will execute from.

## Arguments

- `$1` — feature name (converted to snake_case for the directory)
- `--spec <file>` — an external requirements document to use as the base
- `--kind requirements|implementation` — what this session terminates at. Inferred and proposed when absent

**Before anything else, read `../../../skills/template-conventions/references/planning-contract.md`, resolved relative to this `SKILL.md`, and follow it as the contract for this role.**

## On this host

- **Instruction file.** Where the contract names the project's instruction file, read the applicable repository instructions: `AGENTS.md`, and `CLAUDE.md` when present.
- **Discovery.** `$compound-engineering:ce-brainstorm` is also compatible with the brainstorming gate in Pre-flight step 4 when that is the installed discovery workflow.
