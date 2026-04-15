# OpenAPI Ecosystem Reference

## Specification Versions

| Version | Key Features |
|---------|--------------|
| OpenAPI 3.1 | Full JSON Schema compatibility, webhooks, callback |
| OpenAPI 3.0 | `requestBody`, `components`, multiple servers |
| Swagger 2.0 | `produces`/`consumes`, `definitions`, `parameters` |

## Python Libraries

### Parsing & Validation

| Library | Purpose | PyPI |
|---------|---------|------|
| `openapi-spec-validator` | Validate specs against schema | `pip install openapi-spec-validator` |
| `prance` | Parse and resolve $refs | `pip install prance` |
| `openapi-core` | Request/response validation | `pip install openapi-core` |
| `swagger-parser` | Simple Swagger 2.0 parsing | `pip install swagger-parser` |

### Code Generation

| Library | Output | PyPI |
|---------|--------|------|
| `datamodel-code-generator` | Pydantic models | `pip install datamodel-code-generator` |
| `openapi-python-client` | Full client library | `pip install openapi-python-client` |
| `swagger-codegen` (Java) | Multiple languages | Requires Java |
| `openapi-generator` (Java) | Fork of swagger-codegen | Requires Java |

### Documentation

| Library | Purpose | Notes |
|---------|---------|-------|
| `swagger-ui` | Interactive docs | Needs JS bundling |
| `redoc` | Alternative docs UI | Static HTML output |
| `elements` | Stoplight's docs | Modern, React-based |

## Key OpenAPI 3.x Features

### Servers
```yaml
servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://staging.api.example.com/v1
    description: Staging
```

### Components
```yaml
components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
  parameters:
    UserId:
      name: user_id
      in: path
      required: true
      schema:
        type: integer
```

### Request Body
```yaml
requestBody:
  required: true
  content:
    application/json:
      schema:
        $ref: '#/components/schemas/UserCreate'
```

### Responses
```yaml
responses:
  '200':
    description: Success
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/User'
  '400':
    description: Bad request
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/Error'
```

### Security
```yaml
security:
  - BearerAuth: []
  - ApiKeyAuth: []
```

## Swagger 2.0 Differences

| Feature | OpenAPI 3.x | Swagger 2.0 |
|---------|-------------|-------------|
| Request body | `requestBody` | `in: body` parameter |
| File upload | `format: binary` | `type: file` |
| Multiple servers | `servers` array | `host` + `basePath` |
| Examples | `example` in schema | `examples` map |
| Links | `links` object | Not supported |

## JSON Schema Differences

OpenAPI 3.0 uses a subset of JSON Schema:
- No `exclusiveMinimum`/`exclusiveMaximum` (use `minimum`/`maximum`)
- No `nullable` (use `x-nullable` extension)
- No `oneOf`/`anyOf` in all tools

OpenAPI 3.1 aligns with full JSON Schema 2020-12.

## External References

- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
- [OpenAPI.Tools](https://openapi.tools/)
- [Swagger.io](https://swagger.io/specification/)
- [OpenAPI Generator](https://openapi-generator.tech/)