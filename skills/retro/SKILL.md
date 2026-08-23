---
name: retro
description: >
  This skill should be used when the user asks to "retro", "evaluate zforge",
  "review plugin performance", "score this session", or wants to assess how well
  zforge's workflow served a feature. Evaluates zforge's workflow scaffolding,
  not the project's technical decisions or LLM reasoning quality.
---

# Zforge Retro

Evaluate zforge's workflow performance on a feature. The output is for improving the zforge plugin itself — not for project documentation or tracking.

## Scope Boundary

Zforge is a **workflow plugin**, not a thinking framework. Retro judges:
- Templates, file structure, conventions
- Phase scaffolding, the report and recovery contracts
- Whether declared evidence was honoured, checked and carried
- Workflow ceremony and simplicity

Retro does **NOT** judge:
- Architectural or design decisions (superpowers territory)
- Code quality or correctness (review territory)
- LLM reasoning quality (model capability, not plugin)
- Whether the right feature was built (human's job)

The question is always: **"Did zforge's workflow help or get in the way?"**

## NOT DO Rules

- **Do not run in a fresh session.** If the current session has no substantial conversation about the feature (no tool calls touching feature files, no implementation work), refuse. Retro requires session context to evaluate.
- **Do not run if `session_log.md` has no entries.** No session history means nothing to evaluate.
- **Do not suggest zforge should make thinking decisions.** If a finding starts drifting into "zforge should have caught this design flaw" — that's out of scope. Drop it.
- **Do not produce findings without concrete evidence.** Every finding needs specific files, sections, quotes, or examples. Vague observations are not findings.
- **Do not aggregate across features.** Each retro evaluates one feature's experience. Cross-feature analysis is done by humans through PRs to the zforge repo.

## Data Sources

Read these from `docs/{feature_name}/`:

1. **`decision_review.md` §B** — process notes written live during the run. **Read this first.** It is contemporaneous, where everything else is reconstruction, and a run that improvised something is a template gap recorded at the moment it was felt
2. **`session_log.md`** — Session count, convergence pattern, how each session ended. A usage-limit interruption is a scheduling signal; a clean `USAGE_LIMIT_95` stop with a `## Resume Point` on disk is the budget clause working
3. **`05_progress_overview.md`** — Phase structure, completion status, standing flags and whether any were carried or dropped
4. **`05_progress/05_XX_*.md`** — Evidence tables (required versus achieved, on both axes), decisions, open items, acceptance sections. Each `## Acceptance` names which decisions were promoted and which stayed: compare that against `decision_review.md` §C to see whether the ledger stayed an adjudication queue or became a second copy of the progress folder
5. **`02_plan.md`** — the Verification Matrix, compared against what the phases actually achieved
6. **Template files** — which sections were filled with real content versus empty or "N/A"
7. **`git log` on feature docs** — how much the plan changed after creation
8. **`git log` on source files** — post-completion fix commits touching files this feature created, and which evidence class would have caught each

## Scoring

Six dimensions, each scored 1-10. Consult `references/scoring.md` for the detailed rubric:

| Dimension | What it measures |
|-----------|-----------------|
| Template quality | Did templates match the work's shape? |
| Guidance accuracy | Did scaffolding support the LLM's work? |
| Convergence | Session efficiency relative to complexity? |
| Friction | How much fighting the workflow? |
| Simplicity | Did zforge add unnecessary ceremony? |
| Evidence quality | Did the evidence track reality, or only itself? |

The first five can all score well on a run whose artifacts are internally consistent and disconnected from what the software does. Evidence quality is the one that catches that, so score it independently rather than inferring it from the others.

Overall score can override the average if one dimension dominates.

## Output

Write to `docs/{feature_name}/.zforge-retro/{session_id}.md`:

```markdown
# Retro — {feature_name} — {session_id}
Date: {date}
Sessions so far: {count from session_log.md}
Overall score: {X}/10

## Scores
| Dimension | Score | Notes |
|-----------|-------|-------|
| Template quality | X/10 | ... |
| Guidance accuracy | X/10 | ... |
| Convergence | X/10 | ... |
| Friction | X/10 | ... |
| Simplicity | X/10 | ... |
| Evidence quality | X/10 | ... |

## Findings
{only if something is worth noting — omit section if nothing notable}

### [Dimension] Finding title
**Score impact:** What this affected
**Evidence:**
- Specific files, sections, or conventions involved
- What happened with concrete details
**Example from session:**
> Direct quote or specific interaction that demonstrates the issue
**Suggestion:** Specific, actionable change to zforge (file, template, command)

## Suggested Plugin Changes
{only if findings warrant a commit — omit section otherwise}
```

Most retros should be short — just scores with brief notes. Findings and suggested changes only when something is genuinely worth a plugin improvement.

## Additional Resources

### Reference Files
- **`references/scoring.md`** — Detailed rubric with score meanings, per-dimension criteria, scope boundaries, and finding quality gate
