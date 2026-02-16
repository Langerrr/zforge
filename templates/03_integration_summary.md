# {Feature Name} - Frontend Integration Summary

> Last updated: {DATE}
> Status: {Planning | Ready for Implementation}
> Backend Plan: `./02_plan.md`

---

## Overview

| Item | Value |
|------|-------|
| Target App | `{app-name}` |
| Stack | React + TypeScript + {UI Library} |
| API Base URL | `http://localhost:{port}` |

---

## TypeScript Types

### {Resource} Types

```typescript
// Response type from API
export interface {Resource} {
  id: string;
  field1: string;
  field2: string | null;
  createdAt: string;
  updatedAt: string;
}

// Request DTOs
export interface Create{Resource}Dto {
  field1: string;
  field2?: string;
}

export interface Update{Resource}Dto {
  field1?: string;
  field2?: string;
}

// Query params
export interface Query{Resource}Params {
  page?: number;
  limit?: number;
  search?: string;
}
```

---

## API Mapping

### {Resource} CRUD

| UI Action | Method | Endpoint | Service Method |
|-----------|--------|----------|----------------|
| Load list | GET | `/{resource}` | `listResources(params)` |
| Get detail | GET | `/{resource}/:id` | `getResource(id)` |
| Create | POST | `/{resource}` | `createResource(dto)` |
| Update | PATCH | `/{resource}/:id` | `updateResource(id, dto)` |
| Delete | DELETE | `/{resource}/:id` | `deleteResource(id)` |

---

## Files to Create

### Services

```
src/services/
└── {resource}.service.ts
```

### Pages

```
src/pages/{Role}/{Feature}/
├── index.ts
├── {Feature}Page.tsx
├── {Feature}List.tsx
├── {Feature}Detail.tsx
└── {Feature}Form.tsx
```

### Components

```
src/components/{feature}/
├── {Resource}Card.tsx
└── {Resource}Modal.tsx
```

---

## i18n Keys

Add to `src/i18n/locales/{en,zh,ja}.json`:

```json
{
  "{feature}": {
    "title": "{Feature Title}",
    "create": "Create {Resource}",
    "edit": "Edit {Resource}",
    "delete": "Delete {Resource}",
    "confirmDelete": "Are you sure you want to delete this {resource}?",
    "fields": {
      "field1": "Field 1",
      "field2": "Field 2"
    }
  }
}
```

---

## Navigation

Add menu item to `{Layout}.tsx`:

```typescript
{
  path: '/{feature}',
  label: t('{feature}.title'),
  icon: {IconComponent},
  roles: ['ADMIN']
}
```
