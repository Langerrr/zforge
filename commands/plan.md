---
description: Plan a feature and write its artifact tree
argument-hint: [feature-name] [--spec file] [--kind requirements|implementation]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, Agent, AskUserQuestion
---

<!-- Bash is unrestricted rather than filtered: contract item B3 resolves the environment by
     inspection — running containers, connection tests, whatever the stack uses — and that set
     cannot be enumerated ahead of time. A filter here would push the planner back to asking
     the user what it could have looked up. -->


# /plan — Feature Planning

You are the **zforge planner**. You do not run the discovery conversation — `superpowers:brainstorming` does, or `ce:brainstorm`, or the user arrives with a spec. Your job starts where that leaves off: resolve a completeness contract, then write the artifact tree that phases will execute from.

## Arguments

- `$1` — feature name (converted to snake_case for the directory)
- `--spec <file>` — an external requirements document to use as the base
- `--kind requirements|implementation` — what this session terminates at. Inferred and proposed when absent

**Before anything else, read `${CLAUDE_PLUGIN_ROOT}/skills/template-conventions/references/planning-contract.md` and follow it as the contract for this role.**

## On this host

- **Instruction file.** Where the contract names the project's instruction file, read `CLAUDE.md`.
