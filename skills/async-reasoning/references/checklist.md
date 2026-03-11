# Async State Checklist

Compact checklist for quick application during coding and review. For full reasoning process, see the SKILL.md analysis steps.

## Before Writing Async Code

```
[ ] Identify all state this code reads or writes
[ ] For each: where is the source of truth?
[ ] For each: what are ALL the read paths? (direct, cache, derived, rendered, observed by agent)
[ ] For each: what is the latency between write and read-back on each path?
[ ] Is there a gap? If no gap on any path → async reasoning not needed, stop here
```

## Init Order

```
[ ] What data must exist before this operation can run?
[ ] Is execution gated on dependencies? (enabled flag, conditional, await)
[ ] If the dependency isn't ready, what happens? (skip, error, return default?)
[ ] If a default/empty result is cached from a premature query, when is it evicted?
```

## Write-Read Gap

```
[ ] After the write confirms, trace ALL concurrent read paths:
    [ ] Is there a cache refetch in-flight that will return stale data?
    [ ] Is there a polling interval that will overwrite optimistic state?
    [ ] Is there derived state that computes from a mix of old and new values?
[ ] Choose resolution: cancel-set / write-through / event-driven invalidation / optimistic+rollback
```

## Observer Safety

```
[ ] Who observes this state? (processes, UI, humans, AI agents)
[ ] What action does the current state afford each observer?
[ ] During the async gap, can an observer act on stale state?
[ ] If yes: disable affordances during gap (per-item, not global)
[ ] Are duplicate/conflicting actions prevented? (idempotency guard, lock)
```

## Persistence Boundaries

```
[ ] What state survives a restart/refresh/navigation?
[ ] What does the consumer expect to survive?
[ ] Is there a mismatch between actual and expected persistence?
[ ] When state is restored from storage, is it still valid? (expired session, changed identity)
```

## Review Shortcut

When reviewing existing code, check for these red flags:

- Write operation with no cache invalidation or update strategy
- Query without `enabled` gating on async dependencies
- Global boolean for per-item operation state (e.g., `isLoading` for a list of items)
- Timer-based polling where event-driven invalidation is possible
- Optimistic update without rollback path
- State restored from storage without validation against current context
