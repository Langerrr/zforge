---
description: Multi-reviewer code review with confidence scoring
argument-hint: [--staged | --feature <name> | <file-or-dir>]
allowed-tools: Read, Glob, Grep, Bash(git diff:*), Bash(git log:*), Bash(git blame:*), Bash(git status:*), Bash(git rev-parse:*), Task
model: opus
---

# /review — Structured Code Review

Run a multi-reviewer code review with confidence-based filtering and independent verification.

## Determine Review Scope

Based on `$ARGUMENTS`:

- **No arguments or `--staged`**: Review staged git changes (`git diff --cached`) and unstaged changes (`git diff`).
- **`--feature <name>`**: Review all files listed in `docs/{name}/05_progress_overview.md` under "Files Modified" sections across all phase files. Also check `git diff` for any uncommitted changes to those files.
- **`<file-or-dir>`**: Review the specified file or all files in the specified directory.

## Gather Context (Orchestrator Pre-fetch)

**IMPORTANT**: The orchestrator must gather ALL data before launching sub-agents. Sub-agents receive everything inline — they do NOT use tools. This avoids permission prompts from sub-agent tool calls.

1. Read the full contents of every file to review.
2. Run `git diff --cached` and `git diff` to get diffs (if git-based scope).
3. Check for and read all CLAUDE.md files — in the project root and in directories whose files are being reviewed.
4. If reviewing a feature (`--feature`), read `01_context.md` and `02_plan.md` for architectural context.
5. If scope is git-based, run `git blame` and `git log --oneline -20` on each modified file. Store this output.

Store all of the above as text — you will embed it directly into each reviewer's Task prompt.

## Stage 1: Launch Reviewers

Launch **4 reviewer agents in parallel** using the Task tool with `subagent_type: "feature-dev:code-reviewer"` and `model: "sonnet"`.

**CRITICAL**: Embed all pre-fetched data (file contents, diffs, CLAUDE.md, git blame/log) directly in each Task prompt. The sub-agents must NOT need to call Read, Grep, Glob, or Bash — all data is provided inline. Include the code-reviewer instructions (confidence scoring, output format) from the `zforge:code-reviewer` agent definition in each prompt.

**Agent 1 — Simplicity & DRY Focus**
- Include in prompt: the full code/diffs to review
- Instruct: focus on simplicity, duplication, over-engineering

**Agent 2 — Bugs & Correctness Focus**
- Include in prompt: the full code/diffs to review
- Instruct: focus on logic errors, security, null handling, race conditions

**Agent 3 — Conventions & Architecture Focus**
- Include in prompt: the full code/diffs to review + all CLAUDE.md content
- Instruct: focus on project conventions, naming, abstractions, test coverage

**Agent 4 — History & Context Focus** (only when scope is git-based: `--staged`, no args, or `--feature`)
- Include in prompt: the full code/diffs + git blame output + git log output for each modified file
- Instruct: find regressions, contradictions with prior intent, code churn patterns, and constraints from previous changes
- If scope is a raw file/directory with no git context, skip this agent and run only 3.

## Stage 2: Independent Verification

After all reviewers return, collect every finding with confidence >= 80. For each finding, the orchestrator must:

1. Read the actual code at the finding's file:line location (if not already pre-fetched).
2. Retrieve the git blame for that line range (if available and not already pre-fetched).

Then launch a **parallel Haiku agent** (using `subagent_type: "feature-dev:code-reviewer"` and `model: "haiku"`) to independently verify each finding. Each Haiku verifier receives **inline in the prompt** (no tools needed):
- The finding (description, file, line, suggested fix)
- The actual code at that location (embedded as text)
- The relevant CLAUDE.md content (embedded as text, if the finding references guidelines)
- The git blame for that line range (embedded as text, if available)

Each Haiku verifier scores the finding 0-100 using this rubric (provide verbatim):

```
0: Not confident at all. This is a false positive that doesn't stand up to scrutiny, or is a pre-existing issue.
25: Somewhat confident. This might be a real issue, but may also be a false positive. If stylistic, it was not explicitly called out in CLAUDE.md.
50: Moderately confident. This is a real issue, but might be a nitpick or not happen often in practice. Not very important relative to the rest of the changes.
75: Highly confident. Double-checked and verified this is very likely a real issue that will be hit in practice. The existing approach is insufficient. Important and will directly impact functionality, or is directly mentioned in CLAUDE.md.
100: Absolutely certain. Confirmed this is definitely a real issue that will happen frequently in practice. The evidence directly confirms this.
```

For findings flagged due to CLAUDE.md instructions, the verifier must double-check that the CLAUDE.md **actually calls out that specific issue**.

## Stage 3: Filter and Consolidate

After all verifiers return:

1. **Drop any finding where the verifier scored < 80** (even if the original reviewer scored >= 80)
2. Use the **lower of the two scores** (reviewer vs verifier) as the final confidence
3. Deduplicate (different reviewers may flag the same issue)
4. Sort by final confidence score (highest first)
5. Group into **Critical** (90-100) and **Important** (80-89)

### False Positives to Filter

Instruct verifiers to watch for these common false positives:
- Pre-existing issues not introduced in the current changes
- Something that looks like a bug but is intentional
- Pedantic nitpicks a senior engineer wouldn't flag
- Issues a linter, typechecker, or compiler would catch
- General quality issues unless explicitly required in CLAUDE.md
- Issues with lint-ignore comments in the code
- Functionality changes that are likely intentional

## Present Results

```
## Code Review Results

### Critical Issues
{findings with final confidence 90-100, or "None found"}

### Important Issues
{findings with final confidence 80-89, or "None found"}

### Summary
- Files reviewed: {count}
- Issues found by reviewers: {count before verification}
- Issues after verification: {count after verification}
- Filtered as false positive: {count dropped by verifiers}
- Critical issues: {count}
- Important issues: {count}
```

If reviewing a feature (`--feature`), ask if the user wants findings appended to `docs/{name}/05_progress/review.md`.

## Stage 4: Cost Estimation

After presenting results, estimate the API cost of this review:

1. **Measure inputs**: count total characters across all reviewed files/diffs, divide by 4 to approximate tokens.
2. **Calculate per-component**:
   - **Reviewers** (Sonnet): `{num_reviewers}` agents. Each receives the full review context as input and produces findings as output. Estimate output at ~1000 tokens per reviewer.
     - Input cost: `num_reviewers × input_tokens × $3 / 1M`
     - Output cost: `num_reviewers × 1000 × $15 / 1M`
   - **Verifiers** (Haiku): `{num_verifiers}` agents. Each receives ~500 tokens of finding context + ~1000 tokens of code. Estimate output at ~200 tokens each.
     - Input cost: `num_verifiers × 1500 × $1 / 1M`
     - Output cost: `num_verifiers × 200 × $5 / 1M`
   - **Orchestrator** (Opus): the `/review` command itself. Estimate ~5000 input tokens (instructions + aggregation) and ~2000 output tokens.
     - Input cost: `5000 × $5 / 1M`
     - Output cost: `2000 × $25 / 1M`
3. **Display**:

```
### Estimated Cost
| Component | Model | Agents | Input | Output | Cost |
|-----------|-------|--------|-------|--------|------|
| Reviewers | Sonnet | {N} | ~{X}K tok | ~{Y}K tok | ~${Z} |
| Verifiers | Haiku | {N} | ~{X}K tok | ~{Y}K tok | ~${Z} |
| Orchestrator | Opus | 1 | ~5K tok | ~2K tok | ~${Z} |
| **Total** | | | | | **~${total}** |
```

Note: This is a rough estimate. Actual costs depend on prompt caching, context size, and output length.

## No Issues Path

If no findings survive verification, state clearly:
"4 reviewers found {N} potential issues, but independent verification filtered all as false positives or low confidence. The code looks good."

Or if reviewers found nothing at all:
"All reviewers found no issues with confidence >= 80. The code looks good."
