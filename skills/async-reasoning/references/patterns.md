# Async State Patterns

Common resolution patterns for async state timing gaps. Each pattern addresses a specific gap type. Multiple patterns can combine in a single implementation.

Examples use pseudocode — apply to the specific framework/language in use.

## Cancel-Set Pattern

**Gap**: Write confirms → cache refetch in-flight returns stale data → overwrites optimistic update.

**Mechanism**: Before setting optimistic state, cancel all pending reads for the affected data. Set the new value directly in the cache. Defer any refetch until the source of truth is likely to reflect the write.

```
on write_confirmed(key, new_value):
    cache.cancel_pending_reads(key)       # stop in-flight reads from overwriting
    cache.set(key, new_value)             # set expected value immediately
    schedule_after(delay):                # refetch later when source has indexed
        cache.invalidate(key)
```

**When to use**: Any system where a cache layer polls or refetches independently of writes.

**When NOT to use**: When the write path and read path are the same (synchronous update) — no cancel needed.

---

## Enabled Gating Pattern

**Gap**: Query fires before its dependency is available → returns empty/zero/default → result is cached → dependency arrives but stale cache persists.

**Mechanism**: Gate the query execution on its dependencies being ready. The query doesn't execute (and doesn't cache a wrong result) until prerequisites exist.

```
query(key, fetch_fn, enabled: dependency != null)
    # query does not fire until enabled is true
    # no empty/zero result is cached from a premature fetch

# Backend equivalent:
if not config.ready:
    return skip    # do not fetch, will retry when config arrives
result = fetch(config.service_url)
```

**When to use**: Any init sequence where data arrives at different times. Auth/identity flows, service discovery, config loading, wallet initialization.

---

## Write-Through Pattern

**Gap**: Write to source → return to caller → caller reads cache → cache still has old value.

**Mechanism**: Update the cache synchronously as part of the write operation, before returning. The caller never sees stale data because the cache is updated in the same operation.

```
function update(id, data):
    updated = source.write(id, data)
    cache.set(id, updated)     # cache updated before return
    return updated
```

**When to use**: When the write result is the same shape as the cached read. Common in CRUD operations.

**When NOT to use**: When the write triggers side effects that change other derived state (e.g., updating a balance changes a tier — the tier cache also needs updating).

---

## Event-Driven Invalidation Pattern

**Gap**: Timer-based polling refetches on a fixed interval → stale data persists until next poll.

**Mechanism**: Invalidate cache on a confirmation event, not on a timer. The read path updates precisely when the source of truth changes.

```
# Invalidate on event instead of polling
on event("write_confirmed", key):
    cache.invalidate(key)

# Example sources of events:
#   - transaction receipt / write acknowledgment
#   - WebSocket message
#   - database change notification
#   - message queue consumer callback
```

**When to use**: When an event signals the source of truth has changed. Replaces or supplements timer-based polling.

---

## Optimistic Update with Rollback Pattern

**Gap**: Write is in-flight → consumer shows old state → feels sluggish. But write might fail.

**Mechanism**: Immediately set the expected new state. If the write fails, roll back to the previous value.

```
previous = cache.get(key)
cache.set(key, expected_new_value)     # optimistic

try:
    await write(key, new_value)         # actual write
catch:
    cache.set(key, previous)            # rollback on failure
```

**When to use**: When the write has a high success rate and the expected result is predictable.

**When NOT to use**: When the write result is unpredictable (e.g., auction outcome, multi-party transaction) or when showing incorrect state briefly is worse than showing a loading state.

---

## Disable Affordances Pattern

**Gap**: Async operation in-flight → observer (human, agent) sees state that affords actions → acts on stale state.

**Mechanism**: During the async gap, disable the actions that stale state would afford. Re-enable only after the state is settled.

```
# Track which operation is in-flight (per-item, not global)
active_operation = null

function handle_action(item_id):
    active_operation = item_id
    try:
        await perform(item_id)
    finally:
        active_operation = null

# All action triggers check:
is_disabled = (active_operation != null)

# Backend equivalent — idempotency guard:
if lock.exists(operation_id): return "already_processing"
lock.set(operation_id, ttl=60)
try:    process(operation_id)
finally: lock.delete(operation_id)
```

**When to use**: When an observer can trigger duplicate or conflicting actions during an async gap. Purchase flows, form submissions, job scheduling, agent decision loops.

---

## Sequential Init Pattern

**Gap**: Multiple data sources initialize concurrently → dependent queries fire before prerequisites are ready → cache stores wrong results.

**Mechanism**: Establish a dependency graph. Each stage gates on its prerequisites. No query fires until its inputs are available.

```
Stage 1: load config           → provides: api_urls, feature_flags
Stage 2: init auth (needs: 1)  → provides: user_identity, tokens
Stage 3: load user (needs: 2)  → provides: permissions, preferences
Stage 4: load data (needs: 2,1)→ provides: business state

# Each stage uses enabled gating:
query("user_data", fetch_user, enabled: auth.ready)
query("features",  fetch_data, enabled: auth.ready AND config.ready)
```

**When to use**: Any application startup or session initialization with multiple async data sources. Auth → config → data loading sequences, service mesh initialization, multi-step onboarding flows.
