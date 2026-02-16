# {Feature Name} - Post-Deployment Checklist

> Created: {DATE}
> Status: Pending deployment verification

---

## Post-Deployment Testing

### Smoke Tests

| Test | Expected | Status |
|------|----------|--------|
| {Feature} loads | Page renders without error | [ ] |
| {Action} works | {Expected result} | [ ] |

### Error Handling

| Scenario | Expected Behavior | Status |
|----------|-------------------|--------|
| API unavailable | Show error message | [ ] |
| Invalid input | Show validation error | [ ] |
| Unauthorized | Redirect to login | [ ] |

### Performance

| Test | Acceptance Criteria | Status |
|------|---------------------|--------|
| Page load time | < 3 seconds | [ ] |
| Large dataset | No lag with 100+ items | [ ] |

---

## Deferred Features

| Feature | Reason | Future Phase |
|---------|--------|--------------|
| {Feature 1} | {Reason} | {Phase/Version} |
| {Feature 2} | {Reason} | {Phase/Version} |

---

## Environment Configuration

Ensure these are configured in production:

```bash
# Required
{ENV_VAR_1}=xxx
{ENV_VAR_2}=xxx

# Optional
{ENV_VAR_3}=xxx
```

---

## Deployment Verification

1. **Health Check**
   ```bash
   curl http://{backend-url}/health
   ```

2. **Feature Smoke Test**
   - [ ] Login as admin
   - [ ] Navigate to {feature}
   - [ ] Perform basic CRUD operations

---

## Rollback Plan

If critical issues found:
1. {Rollback step 1}
2. {Rollback step 2}

---

## Sign-off

| Role | Name | Date | Status |
|------|------|------|--------|
| Development | | | [ ] |
| QA | | | [ ] |
| Product | | | [ ] |
