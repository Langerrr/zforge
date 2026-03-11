---
description: Multi-reviewer code review with confidence scoring
argument-hint: [--staged | --feature <name> | --only <reviewers> | <file-or-dir>]
allowed-tools: Read, Write, Glob, Grep, Bash(git diff:*), Bash(git log:*), Bash(git blame:*), Bash(git status:*), Bash(git rev-parse:*), Bash(${CLAUDE_PLUGIN_ROOT}/scripts/*), Bash(mkdir:*), Bash(ls:*), Bash(kill:*), Bash(date:*), Task
model: opus
---

# /review — Structured Code Review

Run a multi-reviewer code review with confidence-based filtering and independent verification. Reviewers are spawned as independent processes (no permission prompts) and signal completion via the monitor protocol.

## Determine Review Scope

Based on `$ARGUMENTS`:

- **No arguments or `--staged`**: Review staged git changes (`git diff --cached`) and unstaged changes (`git diff`). Scope is **git-based**.
- **`--feature <name>`**: Review all files listed in `docs/{name}/05_progress_overview.md` under "Files Modified" sections across all phase files. Also check `git diff` for any uncommitted changes to those files. Scope is **git-based**.
- **`<file-or-dir>`**: Review the specified file or all files in the specified directory. Scope is **not git-based**.

## Gather Context

1. Read the files to review (or their diffs).
2. Check for CLAUDE.md files — in the project root and in directories whose files are being reviewed.
3. If reviewing a feature (`--feature`), read `01_context.md` and `02_plan.md` for architectural context.

Store the file list, CLAUDE.md content, and feature docs — you will include them in reviewer prompts.

## Reviewer Selection

Four reviewers are available, selected via `--only`:

| Slug | Focus Area | Description |
|------|-----------|-------------|
| `all` | All reviewers | Run all available reviewers (default) |
| `simplicity` | Simplicity & DRY | duplication, over-engineering, dead code |
| `bugs` | Bugs & Correctness | logic errors, security, null handling, race conditions |
| `conventions` | Conventions & Architecture | CLAUDE.md violations, naming, abstractions, test coverage |
| `history` | History & Context | git blame/log regressions, churn patterns (git-based scopes only) |

**`--only <slugs>`** — comma-separated list of slugs (e.g. `--only simplicity,bugs`). Defaults to `all` if not specified. If scope is not git-based, `history` is excluded even when using `all`.

## Stage 1: Spawn Reviewers

### 1a. Set Up

Create a temp directory for this review session:
```bash
mkdir -p /tmp/zforge-review-$(date +%s)
```

Store the path as `REVIEW_DIR`.

### 1b. Write Reviewer Prompts

For each selected reviewer, write a self-contained prompt file to `$REVIEW_DIR/prompt_{focus_slug}.md`. The prompt must be fully self-contained since the spawned agent has no conversation context.

Each prompt includes:

1. **Focus assignment, confidence scoring, and output format** — read `${CLAUDE_PLUGIN_ROOT}/agents/code-reviewer.md` and extract the relevant focus area description, the "Confidence Scoring" section, and the "Output Format" section. Include these verbatim in each reviewer prompt. This keeps `code-reviewer.md` as the single source of truth.

2. **Scope info** — scope type (staged/feature/files) and the list of files to review

3. **CLAUDE.md content** — all CLAUDE.md content found (especially important for Conventions reviewer)

4. **Feature docs** (if `--feature`) — `01_context.md` and `02_plan.md` content

5. **Tool usage instructions** — tell the reviewer to use its tools (Read, Glob, Grep, Bash) to examine source code. For History & Context, instruct to run `git blame` and `git log` on modified files.

6. **Output and signal instructions**:
   ```
   When done, write your findings to: {REVIEW_DIR}/review_{focus_slug}.md
   Then append this signal at the very end of that file:
   <!-- AGENT_SIGNAL:{STATUS} T:{TIMESTAMP} PID:{PID} -->
   - STATUS: DONE if review completed, FAILED if error prevented review
   - TIMESTAMP: run `date -u +%Y-%m-%dT%H:%M:%SZ`
   - PID: run `cat {REVIEW_DIR}/review_{focus_slug}.md.pid 2>/dev/null || echo $$`
   Write ONE signal, then STOP immediately.
   ```

### 1c. Spawn

For each selected reviewer, create an empty output file first (so the monitor can detect orphaned agents even if the reviewer dies before writing), then spawn:
```bash
# Create sentinel so monitor can track this reviewer
touch "$REVIEW_DIR/review_{focus_slug}.md"

${CLAUDE_PLUGIN_ROOT}/scripts/spawn-agent.sh \
  "$(pwd)" \
  "$REVIEW_DIR/prompt_{focus_slug}.md" \
  "Read,Glob,Grep,Write,Bash(git diff:*),Bash(git log:*),Bash(git blame:*),Bash(git status:*),Bash(date:*),Bash(cat:*)" \
  "$REVIEW_DIR/review_{focus_slug}.md.pid"
```

All reviewers spawn in parallel (each spawn-agent.sh call returns immediately).

### 1d. Monitor Loop

Start the monitor watching for reviewer output files:
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/monitor.sh "$REVIEW_DIR" 15 120 "review_*.md"
```

Run this as a background task. Poll with `TaskOutput block=true timeout=120000`.

Track progress: `COMPLETED=0`, `FAILED=0`, `TOTAL={num_selected_reviewers}`.

**Signal handling:**

- **DONE**: Increment COMPLETED. If COMPLETED + FAILED == TOTAL, break. Otherwise restart monitor.
- **FAILED**: Increment FAILED. Log which reviewer failed. If COMPLETED + FAILED == TOTAL, break. Otherwise restart monitor.
- **ORPHANED**: Treat as FAILED. Log which reviewer died.
- **WORKING**: Restart monitor, keep waiting.
- **STALE**: Restart monitor, wait longer.
- **Timeout** (no monitor output in 2 minutes): Restart monitor.

### 1e. Collect Findings

After all reviewers complete (or fail):

1. Read each `$REVIEW_DIR/review_{focus_slug}.md` output file.
2. Parse structured findings (look for `### [Critical|Important]` blocks with `**Confidence**:` scores).
3. Collect all findings with confidence >= 80.
4. If a reviewer failed, note it in the final summary.

## Stage 2: Independent Verification

For each finding with confidence >= 80, the orchestrator must:

1. Read the actual code at the finding's `file:line` location using the Read tool.
2. Run `git blame` on that line range if available.

Then launch a **parallel Haiku agent** via the Task tool to verify each finding. Each Haiku verifier receives **inline in the prompt** (no tools needed):
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
- Reviewers run: {list of focus areas}
- Files reviewed: {count}
- Issues found by reviewers: {count before verification}
- Issues after verification: {count after verification}
- Filtered as false positive: {count dropped by verifiers}
- Critical issues: {count}
- Important issues: {count}
```

If reviewing a feature (`--feature`), ask if the user wants findings appended to `docs/{name}/05_progress/review.md`.

## Cleanup

After presenting results, ask the user:
"Review complete. Clean up temp files at `$REVIEW_DIR`?"

Only delete after confirmation.

## No Issues Path

If no findings survive verification, state clearly:
"{N} reviewers found {M} potential issues, but independent verification filtered all as false positives or low confidence. The code looks good."

Or if reviewers found nothing at all:
"All reviewers found no issues with confidence >= 80. The code looks good."
