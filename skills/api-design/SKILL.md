---
name: api-design
description: |
  HTTP/REST API design reference: HTTP method semantics, status codes,
  RFC 7807 error format, resource modeling, state machines, time-based
  and event resources, pagination, filtering, idempotency, versioning,
  OAuth/JWT patterns, OpenAPI 3.1 structure. Use when designing or
  reviewing APIs — standard preparation for api-architect work, or
  standalone for any API design question.
type: knowledge
---

# API Design Reference

Reference material for applying API design doctrine (the doctrine itself —
RESTful-over-RPC, simplicity, owner-proposal default — lives with the
api-architect persona). Load this before producing or reviewing API designs.

## HTTP Methods

| Method | Safe | Idempotent | Cacheable | Use Case |
|--------|------|------------|-----------|----------|
| GET | Yes | Yes | Yes | Retrieve resources (no request body) |
| POST | No | No | No | Create resources, non-idempotent actions |
| PUT | No | Yes | No | Full resource replacement (upsert) |
| PATCH | No | No* | No | Partial resource update |
| DELETE | No | Yes | No | Remove resources |

*PATCH is not idempotent by default; retries may have different results.

## RPC Anti-Patterns (never emit; flag on sight)

```yaml
# ❌ Action-based URLs              # ✅ Noun-based resources
POST /createUser                   POST /users
POST /updateUser                   PATCH /users/{id}
POST /deleteUser                   DELETE /users/{id}
POST /getUser                      GET  /users/{id}
POST /loginUser                    POST /auth/login
POST /searchProducts               GET  /products?q=term

# ❌ Single endpoint + action param        # ❌ Method tunneling
POST /api {"action": "createUser"}         POST /users?method=DELETE

# ❌ Verbs as endpoints                     # ✅ State transitions as subresource
POST /activateSession                      POST /sessions/{id}/actions/activate
POST /cancelOrder                          POST /orders/{id}/actions/cancel

# ❌ Procedure calls                        # ✅ Implicit behavior
POST /calculateTotal                       computed on resource creation
POST /formatName                           client-side / derived
```

## Status Codes

**Success (2xx)**

| Code | Name | Use When |
|------|------|----------|
| 200 | OK | Successful GET, PUT, PATCH, DELETE |
| 201 | Created | Resource created (POST) |
| 202 | Accepted | Request accepted for async processing |
| 204 | No Content | Successful request, empty response (DELETE, some PUT/PATCH) |

**Client errors (4xx)**

| Code | Name | Use When |
|------|------|----------|
| 400 | Bad Request | Malformed request syntax |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Authenticated but not authorized |
| 404 | Not Found | Resource does not exist |
| 409 | Conflict | Request conflicts with current state |
| 422 | Unprocessable Entity | Validation errors |
| 429 | Too Many Requests | Rate limit exceeded |

**Server errors (5xx)**

| Code | Name | Use When |
|------|------|----------|
| 500 | Internal Server Error | Unexpected server error |
| 502 | Bad Gateway | Upstream service failure |
| 503 | Service Unavailable | Service temporarily unavailable |

## Error Format — RFC 7807 Problem Details

```json
{
  "type": "https://api.example.com/errors/insufficient-credit",
  "title": "Insufficient Credit",
  "status": 402,
  "detail": "Your current balance is 30, but the request requires 50.",
  "instance": "/transactions/abc123"
}
```

Required: `type` (URI), `title`, `status` (must match response status).
Optional: `detail`, `instance`, extension fields (e.g. `balance`).

## Resource Relationships

**Nested resources** when: child has no independent identity, access is
always parent-scoped, parent authorization applies, simplicity wins.

**Separate resources** when: child exists independently or across multiple
parents, different access/pagination needs.

```yaml
# Nested: events only exist within a session
POST /sessions/{id}/events
GET  /sessions/{id}/events          # never GET /events with session filter

# Separate: independently addressable
POST /events       (session_id in body)
GET  /events/{id}
```

**Query expansion** for frequently co-needed resources:

```yaml
GET /sessions/{id}?expand=events
# Default to NOT expanding; limit depth to prevent N+1; document options.
```

## State Machines

Model discrete states and allowed transitions explicitly:

```
Session: created → active → ended
         created → cancelled
         active  → cancelled
```

Transitions as endpoints (clarity) or PATCH with state field (simplicity):

```yaml
POST /sessions/{id}/actions/start        # created → active
PATCH /sessions/{id} {"state": "ended"}
```

**409 vs 422:** `409 Conflict` — valid request, conflicts with current
resource state (e.g. transitioning twice); `422 Unprocessable Entity` —
validation failure of format/content.

Document state-dependent operations per state (what is valid when the
resource is created/active/ended — including backfill and immutability
rules) rather than leaving them implicit.

## Time-Based Resources

- Store both absolute times and computed durations:
  `started_at`, `ended_at`, `duration_seconds`.
- Overlap queries via range parameters:
  `GET /sessions?started_at[gte]=...&ended_at[lte]=...`
- Some state derives from time rather than explicit status:
  both timestamps set → ended; start set only → active.

## Event / Append-Only Resources

Audit logs and event streams are immutable: POST to append, GET to read,
never PUT/PATCH/DELETE.

```yaml
POST /sessions/{id}/events        # append only; 409 when inactive (strict mode)
GET  /events/{id}                 # read; no modification
```

Backfill policy (pick one, document it):
- Strict: only during active state (409 otherwise)
- Validated: accept with timestamp in-range check (422 outside)
- Open: any time (offline-friendly)

Ordering via monotonic sequence numbers, not timestamps:

```yaml
GET /sessions/{id}/events?since_sequence=41
```

## Pagination

**Cursor-based** (default choice): stable under inserts, constant-time at
depth, best for feeds and real-time data.

```yaml
GET /items?limit=20&cursor=<opaque>
→ {"data": [...], "pagination": {"next_cursor": "...", "has_more": true}}
```

**Offset-based** (admin dashboards, arbitrary page access, when totals are
needed): `GET /items?offset=0&limit=20` — include total, accept the
skipped-row cost under concurrent writes.

Nested collections reuse the same scheme. Limit max page size.

## Filtering, Sorting, Field Selection

```yaml
GET /items?status=active                # equality
GET /items?created_at[gte]=2024-01-01   # comparison
GET /items?status[in]=active,pending    # set membership
GET /items?q=term                       # full-text
GET /events?session_id=x                # relationship filter
GET /items?sort=-created_at,status      # sort, "-" = descending
GET /items?fields=id,name               # partial response
```

## Idempotency Keys

For risky POSTs that clients may retry:

```yaml
# request
Idempotency-Key: <uuid-v4>
# retry response carries the same key plus
X-Idempotency-Replayed: true
```

Store keys for at least 24–48 hours; return the original response on replay.

## Versioning

| Strategy | Pattern | Trade-off |
|----------|---------|-----------|
| URL path (default) | `/api/v1/items` | clear, cacheable, breaks URLs on major bumps |
| Header | `Accept: application/vnd.api+json;version=2` | clean URLs, less discoverable |

Lifecycle: Active → Deprecated (sunset date announced) → removed.

```yaml
Deprecation: true
Sunset: Sat, 31 Dec 2024 23:59:59 GMT
Link: </api/v2/items>; rel="successor-version"
```

## Authentication & Authorization

**OAuth 2.0 flows (RFC 9700):**

| Flow | Use Case |
|------|----------|
| Authorization Code + PKCE | single-page apps, mobile apps |
| Client Credentials | server-to-server, service accounts |
| Device Authorization | limited-input devices |

Deprecated: implicit grant, resource-owner password credentials.

**JWT (RFC 8725):** strong keys (256+ bit HMAC / 2048+ RSA); validate
`iss`, `aud`, `exp`, `nbf`, `iat`; support `kid` rotation; keep payloads
minimal; never store secrets in tokens.

**Authorization patterns:** scope-based (`Authorization: Bearer <jwt>` with
`["read:items", "write:items"]` scopes); role-based (`X-User-Roles`); or
resource-based (`X-User-Id` + server-side ownership checks).

## OpenAPI 3.1 Skeleton

```yaml
openapi: 3.1.0
info:
  title: API Title
  version: 1.0.0
servers:
  - url: https://api.example.com/v1
tags:
  - name: Items
paths:
  /items:
    get:
      tags: [Items]
      summary: List items
      operationId: listItems
      parameters:
        - $ref: '#/components/parameters/PaginationLimit'
      responses:
        '200':
          $ref: '#/components/responses/ItemList'
components:
  schemas:
    Item:
      type: object
      required: [id, name]
      properties:
        id: { type: string, format: uuid }
        name: { type: string, maxLength: 255 }
  parameters:
    PaginationLimit:
      name: limit
      in: query
      schema: { type: integer, minimum: 1, default: 20 }
  responses:
    ItemList:
      description: Item list
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ItemListResponse'
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
security:
  - BearerAuth: []
```

## Related

- api-architect — persona owning the design doctrine this reference serves
- `python` — implementation standards once the contract is built