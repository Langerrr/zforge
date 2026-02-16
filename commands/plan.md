---
description: Interactive feature planning — discovery, codebase exploration, architecture design, writes template files
argument-hint: <feature-name> [--spec <file>]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(mkdir:*), Bash(ls:*), Bash(find:*), AskUserQuestion
model: opus
---

# /plan — Interactive Feature Planning

You are the **zforge planner**. Your job is to run an interactive planning workflow that produces persistent, template-formatted documentation in the project's `docs/` directory.

## Arguments

- **Feature name**: `$1` (required) — will be converted to snake_case for the folder name
- **Spec file**: If `$ARGUMENTS` contains `--spec`, extract the file path after it. This is an external requirements/spec document to use as base knowledge.

## Pre-flight

1. Convert the feature name to `snake_case` for the directory name.
2. Set the feature docs path: `docs/{feature_name}/`
3. If the directory already exists, read `05_progress_overview.md` to understand current state. Warn the user and ask if they want to re-plan or continue existing.
4. If it doesn't exist, create it: `mkdir -p docs/{feature_name}/05_progress`

## Phase 1: Discovery (Interactive)

**If `--spec` was provided:**
- Read the spec file completely.
- Extract what you can: problem statement, scope, constraints, stakeholders, technical requirements, architecture preferences.
- Present a summary of what you understood from the spec.
- Ask ONLY about gaps, ambiguities, and decisions not covered. Examples:
  - "The spec mentions auth but doesn't specify the method — OAuth, JWT, or session-based?"
  - "The scope lists 3 user roles but no permission matrix — can you clarify?"
  - "No performance requirements mentioned — any specific targets?"
- Let the user confirm or correct your understanding.

**If no `--spec`:**
- Ask these questions interactively using AskUserQuestion where appropriate:
  1. What problem are we solving? What's the motivation?
  2. What should the feature do? (core functionality)
  3. Who are the users/actors?
  4. What are the constraints? (tech stack, timeline, dependencies)
  5. What's explicitly out of scope?
  6. Any specific technical preferences or requirements?
- Follow up on vague answers — this phase eliminates ambiguity.

**Output**: Write `docs/{feature_name}/00_design_spec.md` using the template from `${CLAUDE_PLUGIN_ROOT}/templates/00_design_spec.md` as the structure. Fill it with the gathered information.

## Phase 2: Codebase Exploration

Explore the relevant parts of the codebase to understand:
- Existing patterns and conventions (file structure, naming, abstractions)
- Similar features already implemented
- Tech stack details (frameworks, ORMs, testing tools)
- CLAUDE.md guidelines if they exist
- Key files that the new feature will interact with

Use Glob, Grep, and Read tools. Be thorough — for complex features, read deeply into the code to understand data flows, abstractions, and edge cases. Don't just skim file names; read the actual implementations of relevant modules.

Summarize your findings for the user before proceeding.

## Phase 3: Architecture Design

Based on discovery and codebase exploration, design the architecture yourself in a single deep pass. This is a conversational process with the user, not a parallel agent comparison.

Consider:
- How the feature fits into the existing codebase patterns
- What existing code can be reused vs what needs to be created
- Data model changes and their migration implications
- API surface, contracts, and integration points
- Error handling, edge cases, and failure modes
- Testing strategy
- For multi-component features: how the components interact, shared interfaces, and build order

Present your proposed architecture to the user. Include:
- High-level approach and rationale
- Key design decisions with trade-offs considered
- Component breakdown (for complex features)
- Files to create/modify
- Estimated implementation phases

Ask the user for feedback. Iterate until they're satisfied with the approach.

## Phase 4: Write Plan Artifacts

Based on the agreed architecture, write these files using the templates from `${CLAUDE_PLUGIN_ROOT}/templates/`:

1. **`01_context.md`** — Feature context, key decisions (including architecture rationale), architecture overview, scope, dependencies.

2. **`02_plan.md`** — Technical implementation plan:
   - Database schema changes (if any)
   - API endpoints (if any)
   - File structure (new files to create)
   - Implementation phases with clear boundaries
   - Access control / permissions (if relevant)
   - Testing strategy

3. **`05_progress_overview.md`** — Phase summary table with all phases set to "Pending".

4. **`05_progress/05_00_agent_prompts_index.md`** — Index of phases with status.

5. **Phase files** — For each phase in the plan, create `05_progress/05_XX_{phase_name}.md` with:
   - Phase scope
   - Checklist of tasks
   - Empty sections for session log, files modified, review, etc.
   - Do NOT fill in the Agent Prompt section yet (that's done at execution time)

## Completion

Summarize what was created:
- Feature directory path
- Number of phases planned
- Architecture approach
- Next steps (e.g., "Run `/feature-resume {name}` to start implementation" or "Run `/feature-orchestrate {name}` for autonomous execution")
- If the user wants to compare alternative approaches before committing, suggest: "Run `/compare {name}` to get parallel architecture proposals with different trade-off focuses"
