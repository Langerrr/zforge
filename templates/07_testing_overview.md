# {Feature Name} - Testing Overview

> Last updated: {DATE}
> Status: {Not Started | In Progress | Complete}

---

## Purpose

This folder tracks all testing activities:
- **What tests to create** (test files, test cases)
- **Reusable scripts** (ad-hoc commands worth keeping)
- **Test results** (significant outcomes, not every run)

---

## File Guide

| File | Purpose | Who Updates |
|------|---------|-------------|
| `07_testing/07_01_test_plan.md` | List of test files to create and test cases to cover | Planner (initial), Agent (adds discovered cases) |
| `07_testing/07_02_test_scripts.md` | Reusable test commands and scripts | Agent (captures useful ad-hoc scripts) |
| `07_testing/07_03_test_results.md` | Log of significant test outcomes | Agent (logs notable results) |

---

## For Implementation Agents

### When to Update Test Plan
- When you identify a new test case that should be covered
- When you create a test file
- When a planned test is no longer needed (mark as skipped with reason)

### When to Capture Scripts
**DO capture:**
- Multi-step test sequences (login -> create -> verify)
- Scripts with specific test data that's useful
- Complex curl/API commands
- Database queries for verification

**DON'T capture:**
- One-off typo fixes
- Simple single commands (e.g., `pnpm test`)
- Scripts with hardcoded IDs that won't work again

### When to Log Results
**DO log:**
- First successful test of a major feature
- Test failures that required code fixes
- Edge cases discovered during testing
- Performance issues found
- Cross-browser/environment differences

**DON'T log:**
- Every routine test pass
- Repeated runs of the same test
- Tests during active debugging (log final result only)
- Obvious failures during development (e.g., syntax errors)

---

## Quick Reference

```
# Run unit tests
pnpm test

# Run specific test file
pnpm test -- {file.spec.ts}

# Run e2e tests
pnpm test:e2e
```

---

## Test Coverage Summary

| Type | Planned | Created | Passing |
|------|---------|---------|---------|
| Unit | {N} | {N} | {N} |
| Integration | {N} | {N} | {N} |
| E2E | {N} | {N} | {N} |
| Manual | {N} | - | {N} |
