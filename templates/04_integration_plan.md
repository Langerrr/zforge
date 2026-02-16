# {Feature Name} - Frontend Integration Plan

> Last updated: {DATE}
> Status: Implementation Guide
> Progress: `./05_progress_overview.md`
> Summary: `./03_integration_summary.md`

---

## Overview

Step-by-step implementation guide for integrating {feature} into the frontend.

---

## Phase 1: {Phase Name}

### 1.1 {Step Name}

**File**: `src/{path}/{file}.ts`

**Action**: {Create | Modify}

**Details**:
```typescript
// Code example or description
```

**Checklist**:
- [ ] {Sub-task 1}
- [ ] {Sub-task 2}

### 1.2 {Step Name}

**File**: `src/{path}/{file}.tsx`

**Action**: Copy from `{source}` and modify

**Changes needed**:
- Replace mock data with API calls
- Update import paths
- Add error handling

---

## Phase 2: {Phase Name}

### 2.1 {Step Name}

...

---

## Phase 3: Testing

### 3.1 Test Checklist

- [ ] {Test scenario 1}
- [ ] {Test scenario 2}
- [ ] {Test scenario 3}

### 3.2 Edge Cases

- [ ] Error state: {scenario}
- [ ] Empty state: {scenario}
- [ ] Loading state: {scenario}

---

## Commands

```bash
# Start backend
cd /path/to/backend && pnpm start:dev

# Start frontend
cd /path/to/frontend && pnpm dev

# Type check
pnpm tsc --noEmit

# Lint
pnpm lint
```

---

## Test Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `123456` |
| Operator | `operator` | `123456` |

---

## Verification Checklist

After each phase:
- [ ] No TypeScript errors
- [ ] No ESLint errors
- [ ] UI matches design
- [ ] API integration works
- [ ] i18n strings present (all languages)
- [ ] Loading states implemented
- [ ] Error states implemented

---

## Notes for Implementation Agent

1. Always read source files before copying
2. Test with real backend running
3. Report blockers immediately
4. Update your phase file after each step
