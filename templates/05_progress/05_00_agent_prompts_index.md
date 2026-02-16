# {Feature Name} - Agent Prompts Index

> Last updated: {DATE}
> Owner: Planner

Index of agent prompts for each phase. Each prompt lives in its progress file so agents only read their own context.

---

## Rules for Implementation Agents

1. **Read only your phase file** — don't read other phase files
2. **Update only your phase file** — checklist, session log, completed sections
3. **Do NOT update `../05_progress_overview.md`** — planner updates this to avoid race conditions
4. **Use safe-run.sh for package manager commands** — prevents concurrent conflicts across parallel agents
5. **Signal when stopping** — write exactly ONE signal at the end of your phase file, then stop:
   - `<!-- AGENT_SIGNAL:DONE T:{timestamp} PID:{pid} -->` — all tasks complete
   - `<!-- AGENT_SIGNAL:PAUSED T:{timestamp} PID:{pid} -->` — question for planner, written in `## Questions`
   - `<!-- AGENT_SIGNAL:FAILED T:{timestamp} PID:{pid} -->` — unrecoverable error, documented in `## Errors`
   - Get timestamp: `date -u +%Y-%m-%dT%H:%M:%SZ` | Get PID: `cat {your_phase_file}.pid 2>/dev/null || echo $$`

---

## Prompt Locations

| Phase | File | Status |
|-------|------|--------|
| Phase 1 | `05_01_{phase_name}.md` | Not Started |
| Phase 2 | `05_02_{phase_name}.md` | Not Started |

---

## How to Spawn an Agent

```
Read `docs/{feature_name}/05_progress/05_0X_phaseX.md` and implement the phase.
Update the checklist and session log in that file as you progress.
Do NOT update 05_progress_overview.md.
```
