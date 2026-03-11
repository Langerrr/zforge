---
name: Async State Reasoning
description: This skill should be used when implementing or designing code with async data flows — "state management design", "async data flow", "stale data", "cache invalidation", "optimistic update", "init order", "race condition", "write then read", "data not updating", "cache not refreshing", "UI shows old data after save", "value doesn't update", "empty data on first load". Also applicable when working with caching layers, event-driven systems, or any code where write and read paths have different latencies. Covers frontend, backend, and infrastructure.
---

# Async State Reasoning

When analyzing any state-changing operation in an async system, enumerate ALL concurrent timelines — not just the write path. Sequential chain-of-thought naturally traces one execution path at a time and misses the concurrent read paths that may return stale data, the initialization paths that haven't completed yet, and the observer actions triggered by intermediate state.

## When to Apply

Apply when any of these conditions exist:
- A write operation is followed by a read on a different path (API, cache, RPC, database)
- Multiple data sources initialize at different times
- State is derived from async sources and must stay consistent
- An observer (process, human, AI agent) can act on intermediate or stale state
- Data crosses a persistence boundary (memory ↔ storage ↔ network)

## Core Analysis: Timeline Enumeration

After any state-changing operation, enumerate ALL concurrent timelines — not just the write path:

```
WRITE: Operation X changes state S
  Timeline 1 (write path): X confirms → S is updated at source
  Timeline 2 (cache read path): Query Q is polling/refetching → may return stale S
  Timeline 3 (derived state): Component C derives D from S → D is stale until S propagates
  Timeline 4 (observer): Actor A sees rendered/exposed S → acts on stale value

Enumerate as many timelines as exist — four shown here as common cases.

GAP: Between "write confirmed" and "all read paths return new value"
  → What happens in this gap on each timeline?
  → What can an observer do during this gap?
  → What irreversible action might be taken based on stale state?
```

**If there is no gap on any path (fully synchronous, single-threaded, no cache), async reasoning is not needed. Stop here.**

## Analysis Steps

### 1. Data Flow Mapping

For each piece of state involved:
- Where is the **source of truth**? (database, blockchain, server, local state)
- What are all the **read paths**? (direct query, cache, derived state, rendered UI, agent observation)
- What is the **latency** between write-at-source and read-back on each path?
- Is there an intermediate layer (cache, CDN, replica) that can serve stale data?

### 2. Init Order Analysis

Map the dependency graph of data initialization:
- What data must be available before dependent operations can run?
- What happens if a query fires before its dependency is ready? (returns empty/zero/undefined?)
- Is there a gating mechanism? (`enabled` flags, conditional rendering, await chains)
- What is cached from a failed-early query? Can stale "empty" results persist?

### 3. Concurrent Timeline Trace

After the write operation, trace forward on EVERY read timeline simultaneously:
- Does any read path have an in-flight request that will return stale data?
- Does any cache layer have a refetch scheduled that will overwrite optimistic state?
- Does any observer see intermediate state and act on it?
- Does any derived state compute from a mix of old and new values?

### 4. Persistence Boundary Check

When state crosses a persistence boundary:
- What consistency guarantee exists? (strong, eventual, none)
- What survives a restart/refresh/navigation? What doesn't?
- What does the consumer (user, agent, downstream service) **expect** to survive?
- Is there a mismatch between actual and expected persistence?

### 5. Resolution Strategy

For each gap identified, choose a resolution:
- **Cancel-set**: Cancel pending reads before writing optimistic state (prevents stale overwrite)
- **Gated initialization**: Disable dependent operations until prerequisites are ready
- **Event-driven invalidation**: Invalidate on confirmation events, not timers
- **Optimistic with rollback**: Set expected state immediately, rollback if write fails
- **Write-through**: Update cache synchronously with write, skip refetch
- **Disable affordances**: Prevent observer actions during the gap (disable buttons, queue agent actions)

See `references/patterns.md` for detailed pattern descriptions.

## Integration with Planning

During `/plan` Phase 3 (Architecture Design), apply steps 1-4 to each async data source identified. Capture the decisions in the plan's state management section. Without explicit decisions at planning time, these become ad-hoc implementation choices that produce bugs.

## Integration with Implementation

During coding, apply when writing:
- Cache read/write logic (any caching library)
- Optimistic update handlers
- Initialization hooks or setup sequences
- State that multiple components or services consume
- Event handlers that trigger state transitions

## Integration with Review

During code review, check:
- Is every write followed by a read on the same state? Trace the read path — is it the same path as the write, or a different one with its own latency?
- Are queries gated on their dependencies, or can they fire before data is ready?
- Can an observer (human clicking a button, agent reading a status) act during an async gap?

## Additional Resources

### Reference Files

- **`references/patterns.md`** — Detailed async state patterns with examples and when to apply each
- **`references/checklist.md`** — Compact checklist format for quick application during coding and review
