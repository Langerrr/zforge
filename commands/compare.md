---
description: Parallel architecture comparison — spawns multiple agents with different trade-off focuses
argument-hint: <feature-name>
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(git:*), Bash(mkdir:*), Bash(ls:*), Bash(find:*), Task, AskUserQuestion
model: opus
---

# /compare — Architecture Comparison

Spawn parallel `zforge:code-architect` agents to generate competing architecture proposals with different trade-off focuses. Best for simpler features where you want to quickly evaluate 2-3 approaches side by side.

For complex multi-component features, use `/plan` instead — it does deeper single-thread architecture design with user conversation.

## Arguments

- **Feature name**: `$1` (required) — snake_case folder name

## Pre-flight

1. Convert feature name to `snake_case`.
2. Check if `docs/{feature_name}/00_design_spec.md` exists.
   - If yes: read it for requirements context.
   - If no: ask the user to run `/plan {name}` first, OR gather a brief description of the feature interactively (problem, scope, constraints) and proceed with that.
3. Explore the codebase: use Glob, Grep, Read to understand relevant patterns, conventions, tech stack, and key files the feature will touch. Summarize findings.

## Launch Architects

Launch **2-3 `zforge:code-architect` agents in parallel** using the Task tool. Each agent gets:
- The feature requirements (from design spec or gathered context)
- The codebase exploration findings
- A different trade-off focus:

**Agent 1 — Minimal Changes**: Smallest possible change. Maximum reuse of existing code. Fastest to implement.

**Agent 2 — Clean Architecture**: Best long-term maintainability. Clean abstractions and separation of concerns. May require more upfront work.

**Agent 3 — Pragmatic Balance**: Balance between speed and quality. Good enough abstractions without over-engineering.

## Synthesize

After all agents return, synthesize their proposals into a comparison:

```
## Architecture Options

### Option A: {name} — {1-line summary}
- **Approach**: {2-3 sentences}
- **Pros**: {bullets}
- **Cons**: {bullets}
- **Files to create/modify**: {count}
- **Estimated phases**: {count}

### Option B: ...

### Option C: ...

### Recommendation
{Your expert opinion on which option fits best and why}
```

Present this to the user and ask which approach they prefer (or a hybrid).

## Write Results

If the user picks an approach:

1. If `docs/{feature_name}/` doesn't exist yet, suggest running `/plan {name}` to create the full plan artifacts using the chosen approach as guidance.
2. If `docs/{feature_name}/` already exists (from a prior `/plan`), ask if they want to update `01_context.md` and `02_plan.md` with the chosen architecture. Update those files if yes.

## Cost Estimation

After completion, estimate the API cost:

| Component | Model | Agents | Est. Cost |
|-----------|-------|--------|-----------|
| Architects | Sonnet | {N} | ~${X} |
| Orchestrator | Opus | 1 | ~${X} |
| **Total** | | | **~${total}** |

Estimate: each architect uses ~input_tokens × $3/M + ~1500 output tokens × $15/M (Sonnet). Orchestrator uses ~5K input + ~2K output at Opus rates ($5/$25 per M).
