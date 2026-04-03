# Retro Scoring Rubric

## Score Scale

| Score | Meaning |
|-------|---------|
| 8-10 | Helped — workflow was smooth, templates fit the work |
| 5-7 | Neutral — didn't help or hurt, some irrelevant parts |
| 3-4 | Friction — had to work around the workflow |
| 1-2 | Actively harmful — workflow misled or blocked progress |

## Dimensions

### Template Quality (1-10)

Evaluate whether zforge's templates matched the shape of the work.

**Look for:**
- Sections filled with real content vs "N/A" or left empty
- Sections the user had to create ad-hoc that the template didn't provide
- Template structure that matched vs mismatched the feature's concerns

**High score:** All template sections were relevant and filled with useful content.
**Low score:** Multiple sections were skipped, filled with "N/A", or missing sections had to be improvised.

### Guidance Accuracy (1-10)

Evaluate whether zforge's workflow scaffolding gave the LLM a good structure to work in.

**Look for:**
- Phase file format — did it capture what agents actually needed?
- Signal protocol — did it work correctly?
- Template conventions — were ownership rules respected and useful?
- Agent prompt structure — did it provide enough context for agents?

**Scope boundary:** Phase ordering, architectural decisions, and plan quality are LLM reasoning issues, NOT zforge issues. If the LLM sequenced phases badly or made poor architectural choices, that is out of scope. Only evaluate whether zforge's scaffolding supported or hindered the LLM's work.

**High score:** The scaffolding gave agents clear boundaries and the right information.
**Low score:** Agents struggled because the file structure, signal protocol, or conventions were unclear or insufficient.

### Convergence (1-10)

Evaluate session efficiency relative to feature complexity.

**Look for (from session_log.md):**
- Total session count — reasonable for the feature's complexity?
- Fix sessions — sessions that reworked something a previous session "completed"
- Were fix sessions caused by workflow gaps or by genuine problem difficulty?

**Scope boundary:** Hard problems take many sessions — that's not zforge's fault. Only count sessions where the workflow itself caused rework (e.g., a template gap forced revisiting earlier work, or a missing convention led to inconsistent output that needed correction).

**High score:** Session count was proportional to feature complexity; no rework caused by workflow gaps.
**Low score:** Multiple sessions spent fixing issues that better workflow scaffolding would have prevented.

### Friction (1-10)

Evaluate how much the user had to fight or work around zforge's workflow.

**Look for:**
- Skipped zforge steps or templates
- Manual overrides of conventions
- User corrections to zforge's workflow guidance
- Workarounds for template limitations

**High score:** The user followed the workflow naturally without fighting it.
**Low score:** The user repeatedly skipped steps, overrode conventions, or had to manually work around limitations.

### Simplicity (1-10)

Evaluate whether zforge added unnecessary ceremony for this feature.

**Look for:**
- Templates/phases that existed but served no purpose
- Boilerplate sections that added no value
- Could the same outcome have been achieved with fewer zforge artifacts?
- Was the feature over-scaffolded relative to its actual complexity?

**Scope boundary:** Zforge is a workflow plugin, not a thinking framework. It should stay out of the way. If the retro finds that zforge should have "caught" an architectural mistake or "suggested" a better approach, that is out of scope — that's superpowers territory.

**High score:** Every zforge artifact pulled its weight; no unnecessary ceremony.
**Low score:** Significant over-scaffolding; artifacts created that nobody used.

## Overall Score

The overall score is a weighted average of the five dimensions, but override the average if one dimension dominates the experience. For example:
- Simplicity scores 2/10 (massive over-scaffolding) should not average out to 7 just because other dimensions were fine
- Friction scores 2/10 (constantly fighting the workflow) overshadows neutral scores in other dimensions

## Finding Quality Gate

A finding must include concrete evidence from the session to be reported. Required:
- Which specific template, file, section, or convention is involved
- What happened — with direct quotes or examples from the session interaction
- Why this is a zforge issue, not an LLM reasoning issue

If a finding cannot cite specific evidence, drop it. Vague observations are not findings.
