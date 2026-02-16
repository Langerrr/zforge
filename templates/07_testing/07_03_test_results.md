# {Feature Name} - Test Results Log

> Last updated: {DATE}
> Overview: `../07_testing_overview.md`

---

## What to Log Here

**DO log:**
- First successful test of major features (milestone)
- Failures that required code fixes (learning)
- Edge cases discovered (documentation)
- Environment-specific issues (reference)

**DON'T log:**
- Routine passing tests
- Repeated runs during debugging
- Failures from obvious mistakes (typos, syntax)

---

## Results Log

### {DATE}

#### Phase {N}: {Phase Name}

| Test | Result | Notes |
|------|--------|-------|
| {Test description} | Pass | {First successful run after fixing X} |
| {Test description} | Fail -> Pass | {Failed due to X, fixed by Y} |

**Edge cases discovered:**
- {Description of edge case found}

**Issues found:**
- {Issue description} -> {Resolution or ticket reference}

---

## Summary by Phase

| Phase | Tests Run | Pass | Fail | Issues Found |
|-------|-----------|------|------|--------------|
| 1 | {N} | {N} | {N} | {N} |
| 2 | {N} | {N} | {N} | {N} |

---

## Known Issues

| Issue | Phase Found | Status | Notes |
|-------|-------------|--------|-------|
| {Description} | {N} | {Open | Fixed | Deferred} | {Details} |

---

## Environment Notes

| Environment | Tested | Notes |
|-------------|--------|-------|
| Local (Mac) | Yes | {Any issues} |
| Local (Linux/WSL) | Yes | {Any issues} |
| Docker | No | {Reason} |
| CI/CD | No | {Reason} |
