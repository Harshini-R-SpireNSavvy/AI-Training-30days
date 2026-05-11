# API Contract — Acme Internal AI Gateway v1

**Base URL:** `https://ai-gateway.internal.acme.example.com/v1`  
**Protocol:** HTTPS only  
**Format:** JSON (`Content-Type: application/json`)  
**Version:** `2025-11-01` (sent via header; see below)

---

## Global conventions

### Headers (all endpoints)

| Header | Required | Description |
|--------|----------|-------------|
| `Authorization` | Yes | `Bearer <access_token>` — OAuth2 JWT issued by Acme SSO |
| `X-Acme-Tenant-Id` | Yes | UUID of the business unit (for row-level isolation in logs) |
| `X-Acme-Request-Id` | No | Client-generated UUID; if omitted, server generates one and returns it |
| `X-Acme-Api-Version` | Yes | Literal `2025-11-01` for this contract |

### Standard error envelope

All error responses use HTTP 4xx/5xx with this body:

```json
{
  "error": {
    "code": "string",
    "message": "string",
    "request_id": "uuid",
    "details": {}
  }
}
```

**`code` values (non-exhaustive):** `unauthorized`, `forbidden`, `validation_error`, `rate_limited`, `upstream_timeout`, `internal_error`.

### Rate limits

- **Default:** 120 requests per minute per `client_id` (embedded in JWT).  
- **Burst:** 30 additional requests over 10 seconds.  
- **429 response** includes `Retry-After` (seconds) as HTTP header.

---

## Endpoint 1 — `POST /completions`

**Purpose:** Synchronous text completion with optional tool hints (gateway may map to internal model routing). Does **not** persist conversation unless `session_id` is provided.

### Request schema

```json
{
  "model": "string",
  "messages": [
    {
      "role": "system | user | assistant",
      "content": "string"
    }
  ],
  "session_id": "uuid | null",
  "temperature": "number | null",
  "max_output_tokens": "integer | null"
}
```

| Field | Type | Required | Constraints |
|-------|------|------------|-------------|
| `model` | string | Yes | One of: `acme-lite-1`, `acme-pro-1` |
| `messages` | array | Yes | 1–50 items; `content` max 100_000 chars per message |
| `session_id` | uuid \| null | No | If set, server may load/save session state per policy |
| `temperature` | number \| null | No | Default `0.2`; range `0`–`1` |
| `max_output_tokens` | integer \| null | No | Default `1024`; max `8192` |

### Response schema — `200 OK`

```json
{
  "id": "uuid",
  "model": "string",
  "output": {
    "role": "assistant",
    "content": "string"
  },
  "usage": {
    "input_tokens": "integer",
    "output_tokens": "integer"
  },
  "request_id": "uuid"
}
```

### Example

**Request**

```http
POST /v1/completions HTTP/1.1
Host: ai-gateway.internal.acme.example.com
Authorization: Bearer eyJhbG...
X-Acme-Tenant-Id: 7b2c9f1a-...
X-Acme-Api-Version: 2025-11-01
Content-Type: application/json
```

```json
{
  "model": "acme-lite-1",
  "messages": [
    { "role": "system", "content": "You are a concise internal assistant." },
    { "role": "user", "content": "Summarize our expense policy for domestic travel in 3 bullets." }
  ],
  "temperature": 0.1,
  "max_output_tokens": 256
}
```

**Response**

```json
{
  "id": "c4f2a111-2222-4b5c-8d9e-001122334455",
  "model": "acme-lite-1",
  "output": {
    "role": "assistant",
    "content": "- …\n- …\n- …"
  },
  "usage": { "input_tokens": 412, "output_tokens": 118 },
  "request_id": "9f3e…"
}
```

---

## Endpoint 2 — `POST /sessions/{session_id}/messages`

**Purpose:** Append a user message to an existing server-side session and return the assistant reply. Creates audit trail rows for compliance.

**Path parameter**

| Name | Type | Description |
|------|------|-------------|
| `session_id` | uuid | Session created via `POST /sessions` (out of scope for “3 endpoints” minimum—assume session exists) or returned from completion with persistence enabled |

### Request schema

```json
{
  "content": "string",
  "metadata": {
    "client_reference": "string | null",
    "channel": "string | null"
  }
}
```

| Field | Type | Required | Constraints |
|-------|------|------------|-------------|
| `content` | string | Yes | 1–16_000 chars |
| `metadata` | object | No | Arbitrary keys ≤ 20; each key ≤ 64 chars; each value ≤ 512 chars |

### Response schema — `200 OK`

```json
{
  "message_id": "uuid",
  "session_id": "uuid",
  "assistant": {
    "content": "string",
    "citations": [
      {
        "title": "string",
        "url": "string",
        "snippet": "string"
      }
    ]
  },
  "request_id": "uuid"
}
```

`citations` may be empty if the model did not use retrieval.

### Errors specific to this route

| HTTP | `error.code` | When |
|------|----------------|------|
| 404 | `not_found` | Unknown `session_id` for tenant |
| 409 | `session_closed` | Session is read-only after retention lock |

---

## Endpoint 3 — `GET /policies/effective`

**Purpose:** Return the **effective** model/tool/retrieval policies for the calling principal (derived from JWT groups + tenant). Clients use this to configure UI and to validate feature flags before calling other services.

### Query parameters

| Name | Type | Required | Description |
|------|------|------------|-------------|
| `surface` | string | No | One of: `chat`, `batch`, `copilot`; default `chat` |

### Request

No body. Standard headers only.

### Response schema — `200 OK`

```json
{
  "tenant_id": "uuid",
  "surface": "string",
  "models_allowed": ["string"],
  "tools_allowed": ["string"],
  "retrieval_indexes": ["string"],
  "max_output_tokens_default": "integer",
  "data_residency": "string",
  "request_id": "uuid"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `data_residency` | string | e.g. `EU`, `US`, `IN` — binding for downstream calls |
| `retrieval_indexes` | array | Named corpora the principal may query |

### Example response

```json
{
  "tenant_id": "7b2c9f1a-1111-2222-3333-444455556666",
  "surface": "chat",
  "models_allowed": ["acme-lite-1"],
  "tools_allowed": ["mcp://hr-policy-search", "mcp://jira-readonly"],
  "retrieval_indexes": ["employee-handbook-v3"],
  "max_output_tokens_default": 1024,
  "data_residency": "EU",
  "request_id": "aa11bb22-ccdd-eeff-0011-223344556677"
}
```

---

## OpenAPI fragment (machine-readable summary)

The three operations above correspond to:

| Method | Path | OperationId |
|--------|------|---------------|
| POST | `/v1/completions` | `createCompletion` |
| POST | `/v1/sessions/{session_id}/messages` | `appendSessionMessage` |
| GET | `/v1/policies/effective` | `getEffectivePolicies` |

Schemas: `CompletionRequest`, `CompletionResponse`, `SessionMessageRequest`, `SessionMessageResponse`, `EffectivePoliciesResponse`, `ErrorEnvelope`.

---

## Changelog

| Version | Date | Notes |
|---------|------|--------|
| `2025-11-01` | (fictional) | Initial Day 19 training contract |
