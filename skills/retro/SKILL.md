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
- Phase scaffolding and signal protocol
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

1. **`session_log.md`** — Session count, convergence pattern, which sessions touched which phases
2. **`05_progress_overview.md`** — Phase structure, completion status
3. **`05_progress/05_XX_*.md`** — Phase files: session logs, blockers, questions, errors sections
4. **Template files (`00`-`09`)** — Which sections were filled vs empty/N/A
5. **`git log` on feature docs** — How much the plan changed after initial creation
6. **`git log` on source files** — Post-completion fix commits touching files this feature created

## Scoring

Five dimensions, each scored 1-10. Consult `references/scoring.md` for the detailed rubric:

| Dimension | What it measures |
|-----------|-----------------|
| Template quality | Did templates match the work's shape? |
| Guidance accuracy | Did scaffolding support the LLM's work? |
| Convergence | Session efficiency relative to complexity? |
| Friction | How much fighting the workflow? |
| Simplicity | Did zforge add unnecessary ceremony? |

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
