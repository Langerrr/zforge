# {Feature Name} - Configuration Reference

> Last updated: {DATE}

All configuration required for this feature in one place.

---

## Environment Variables

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `{VAR_NAME}` | {Description} | `value` |

### Optional

| Variable | Description | Default |
|----------|-------------|---------|
| `{VAR_NAME}` | {Description} | `default_value` |

---

## Feature Flags / Module Config

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `{feature_enabled}` | boolean | false | Enable/disable feature |
| `{feature_limit}` | number | 10 | Max items allowed |

---

## Database

### New Tables

| Table | Purpose |
|-------|---------|
| `{TableName}` | {Description} |

### Migrations

| Migration | Description | Status |
|-----------|-------------|--------|
| `{timestamp}_{name}` | {What it does} | Applied |

---

## API Reference

See: `{path/to/api-docs}` or `http://localhost:{port}/api-docs`

---

## External Services

| Service | Purpose | Config Location |
|---------|---------|-----------------|
| {Service Name} | {Purpose} | `.env` / Config file |

---

## Local Development

```bash
# Required env vars for local dev
export VAR_NAME=value

# Or copy from example
cp .env.example .env
```

---

## Production Checklist

- [ ] All required env vars set
- [ ] Feature flags configured
- [ ] Database migrations applied
- [ ] External service credentials configured
