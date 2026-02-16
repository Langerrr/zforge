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

| Phase | Name | Dependencies | Description |
|-------|------|-------------|-------------|
| 1 | {Phase name} | None | {What this phase covers} |
| 2 | {Phase name} | Phase 1 | {What this phase covers} |
| 3 | {Phase name} | Phase 2 | {What this phase covers} |

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

## Testing Strategy

| Type | Scope | Priority |
|------|-------|----------|
| Unit | Service logic | High |
| Integration | API endpoints | High |
| E2E | Full workflows | Medium |
