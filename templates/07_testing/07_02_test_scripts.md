# {Feature Name} - Test Scripts

> Last updated: {DATE}
> Overview: `../07_testing_overview.md`

Reusable scripts and commands captured during testing.

---

## Authentication

```bash
# Login as admin and get token
curl -X POST http://localhost:3002/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"club_admin","password":"123456"}' \
  | jq -r '.access_token'

# Store token in variable
TOKEN=$(curl -s -X POST http://localhost:3002/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"club_admin","password":"123456"}' \
  | jq -r '.access_token')
```

---

## {Resource} CRUD

### Create

```bash
curl -X POST http://localhost:3002/{resource} \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "field1": "value1",
    "field2": "value2"
  }'
```

### Read

```bash
# List all
curl -X GET "http://localhost:3002/{resource}" \
  -H "Authorization: Bearer $TOKEN"

# Get by ID
curl -X GET "http://localhost:3002/{resource}/1" \
  -H "Authorization: Bearer $TOKEN"
```

### Update

```bash
curl -X PATCH http://localhost:3002/{resource}/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "field1": "updated_value"
  }'
```

### Delete

```bash
curl -X DELETE http://localhost:3002/{resource}/1 \
  -H "Authorization: Bearer $TOKEN"
```

---

## Database Verification

```bash
# Check record in database
docker exec {container} psql -U {user} -d {db} -c \
  "SELECT * FROM \"{Table}\" WHERE id = 1;"

# Count records
docker exec {container} psql -U {user} -d {db} -c \
  "SELECT COUNT(*) FROM \"{Table}\";"
```

---

## Complex Test Sequences

### {Sequence Name}

```bash
# Step 1: {Description}
{command}

# Step 2: {Description}
{command}

# Step 3: Verify
{command}
```

---

## Notes

- {Any important notes about these scripts}
- {Environment-specific considerations}
