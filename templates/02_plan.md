# {Feature Name} - Technical Plan

> Last updated: {DATE}
> Status: Planning
> Context: `./01_context.md`

---

## Overview

{Brief summary of the technical approach}

---

## Database Schema

### New Tables

```sql
-- {Table description}
CREATE TABLE "{TableName}" (
    "id" SERIAL PRIMARY KEY,
    -- fields
    "createdAt" TIMESTAMP DEFAULT NOW(),
    "updatedAt" TIMESTAMP DEFAULT NOW()
);
```

### Schema Changes

| Table | Change | Migration |
|-------|--------|-----------|
| {Table} | {Add column / Modify / etc.} | {migration name} |

---

## API Endpoints

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | /{resource} | List all | {Role} |
| POST | /{resource} | Create new | {Role} |
| GET | /{resource}/:id | Get by ID | {Role} |
| PATCH | /{resource}/:id | Update | {Role} |
| DELETE | /{resource}/:id | Delete | {Role} |

---

## File Structure

### New Files

```
src/
├── {module}/
│   ├── {module}.controller.ts
│   ├── {module}.service.ts
│   ├── {module}.module.ts
│   ├── dto/
│   │   ├── create-{module}.dto.ts
│   │   └── update-{module}.dto.ts
│   └── entities/
│       └── {module}.entity.ts
```

---

## Implementation Phases

Dependency edges are plan facts. **Scheduling is not** — whether two phases with disjoint edges actually run in parallel is a runtime call made by the orchestrator against the collision surface and the token budget.

| Phase | Name | Depends on | Collision surface | Description |
|-------|------|-----------|-------------------|-------------|
| 1 | {Phase name} | None | {generated files, lockfiles, migrations, shared modules} | {What this phase covers} |
| 2 | {Phase name} | 1 | | {What this phase covers} |
| 3 | {Phase name} | 2 | | {What this phase covers} |

---

## Verification Matrix

What each phase's gate will and will not cover, declared before any of it runs. Each phase's `## Evidence Required` table inherits its row from here. See `skills/template-conventions/references/evidence-scale.md`.

Where `07_harness_conventions.md` exists, read it before filling this in. It says which of this project's commands interact, which tear down state, and which can report a pass without checking anything — and a matrix built without those facts declares classes the harness cannot actually deliver.

Mark each cell `✓` (will cover), `—` (will not), `n/a` (does not apply), or **`gap`** (should be covered and will not be — this opens a standing flag at the phase that first needs it).

Two axes, two tables, because they are not comparable. **E** is what will be executed; **J** is what will be judged. Classes rank within an axis only.

### E — execution

| Phase | E1 pure logic | E2 boundary | E3 prod runtime | E4 real surface |
|-------|---------------|-------------|-----------------|-----------------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

### J — judgement

Fill this for any phase carrying a claim no test runner settles — a vocabulary the actor must find learnable, a format that must generalise, a boundary that must be in the right place. Name the method in the phase's evidence row; this table only declares the class it will reach.

| Phase | J1 method stated and walked | J2 named referent | The claim being judged |
|-------|------------------------------|-------------------|------------------------|
| 1 | | | |
| 2 | | | |
| 3 | | | |

A phase with no judgement-shaped claim leaves its row `n/a` and that is a complete answer.

**Read the columns, not the rows.** A column that is empty across every phase with a user-facing surface is a hole in the whole feature, and this table exists to make that visible now rather than after the last phase. An empty E4 column is a wiring hole. An empty J column under a spec whose acceptance came from the user's own vocabulary is the same hole one level up.

---

## Environment Assumptions

What the plan assumes exists, what is actually here, and what standing in for it defers.

| # | Assumed | Actual | Substitution | What it defers | Phases affected |
|---|---------|--------|--------------|----------------|-----------------|
| S1 | {managed service, credential, vendor token} | {what exists locally} | {what will be used instead} | {which verification this postpones, and to when} | |

A substitution with no deferral stated is a substitution nobody will remember to undo.

---

## Invariants

Rules that must hold across phases. Each needs an owner phase that establishes it and a **re-check phase** — the last phase touching any of its call sites.

| # | Invariant | Established by | Re-checked by | How it is checked |
|---|-----------|---------------|---------------|-------------------|
| I1 | | Phase {N} | Phase {M} | |

An invariant with no re-check phase is verified by nobody: the phase file is both the unit of work and the unit of verification, so anything spanning phases falls between them.

---

## Access Control

| Role | Permissions |
|------|------------|
| {Role} | {What they can do} |

---

## Configuration

| Variable | Purpose | Default |
|----------|---------|---------|
| {VAR} | {Purpose} | {Default} |

---

## Frontend State Management

> Include this section when the feature has a frontend with async data sources (APIs, blockchain, WebSocket, etc.) and no UI mockup is provided. Remove if not applicable.

### Data Sources & Latency

| Source | Write → Read Latency | UI During Gap | Invalidation Strategy |
|--------|----------------------|---------------|----------------------|
| {API/chain/cache} | {ms/s/blocks} | {loading/optimistic/disabled} | {poll/refetch/cancel-set/event} |

### Persistence Strategy

| State | Storage | Survives Refresh | Notes |
|-------|---------|-----------------|-------|
| {state name} | {memory/sessionStorage/localStorage/server/URL} | {yes/no} | {why} |

### Initialization Order

```
1. {First available} — {what depends on it}
2. {Second} — {gated by what}
3. {Queries enabled after dependencies ready}
```

### User Action Constraints

| Action | Disabled When | Shows During | Enabled After |
|--------|--------------|--------------|---------------|
| {button/action} | {condition} | {loading state} | {confirmation event} |

---

## Testing Strategy

| Type | Scope | Priority |
|------|-------|----------|
| Unit | Service logic | High |
| Integration | API endpoints | High |
| E2E | Full workflows | Medium |
