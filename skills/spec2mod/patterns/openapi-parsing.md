# OpenAPI/Swagger Parsing Patterns

## Overview

OpenAPI (formerly Swagger) is the most common API specification format. This pattern covers parsing strategies.

## Format Detection

### OpenAPI 3.x (JSON)
```python
import json

def detect_openapi_json(content: dict) -> bool:
    return "openapi" in content and content["openapi"].startswith("3.")
```

### OpenAPI 3.x (YAML)
```python
import yaml

def detect_openapi_yaml(content: dict) -> bool:
    return "openapi" in content and content["openapi"].startswith("3.")
```

### Swagger 2.0
```python
def detect_swagger(content: dict) -> bool:
    return "swagger" in content and content["swagger"] == "2.0"
```

## Key Structures

### Info Object
```yaml
info:
  title: Pet Store API
  version: 1.0.0
  description: A sample Pet Store Server
```

Extract for package name suggestion: `title.lower().replace(" ", "").replace("-", "")`

### Paths Object
```yaml
paths:
  /pets:
    get:
      summary: List all pets
      operationId: listPets
      parameters: [...]
      responses:
        '200':
          description: A paged array of pets
```

Use `operationId` for method names, or generate from path + method.

### Security Schemes
```yaml
components:
  securitySchemes:
    ApiKeyAuth:
      type: apiKey
      in: header
      name: X-API-Key
    BearerAuth:
      type: http
      scheme: bearer
```

Map to authentication handlers in generated code.

## Parsing Libraries

| Library | Use Case |
|---------|----------|
| `openapi-spec-validator` | Validate spec before parsing |
| `prance` | Parse and resolve $refs |
| `datamodel-code-generator` | Generate Pydantic models |
| `openapi-parser` | Simple parsing to Python objects |

## Recommended Approach

```python
from openapi_spec_validator import validate
from prance import ResolvingParser

def parse_openapi(file_path: str) -> dict:
    # Validate first
    with open(file_path) as f:
        spec = json.load(f)
    validate(spec)
    
    # Resolve $refs
    parser = ResolvingParser(file_path)
    return parser.specification
```

## Handling $refs

OpenAPI specs use JSON References (`$ref`) to avoid repetition. Always resolve before processing:

```yaml
components:
  schemas:
    Pet:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string

paths:
  /pets:
    get:
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Pet'
```

After resolution, the schema is inline in the response.

## Parameter Extraction

```python
def extract_parameters(path_item: dict) -> list[Parameter]:
    params = []
    for param in path_item.get("parameters", []):
        params.append(Parameter(
            name=param["name"],
            location=param["in"],  # path, query, header, cookie
            required=param.get("required", False),
            schema=param.get("schema", {}),
            description=param.get("description", "")
        ))
    return params
```

## Response Schema Extraction

```python
def extract_response_schema(operation: dict) -> dict | None:
    for code, response in operation.get("responses", {}).items():
        if code.startswith("2"):  # Success codes
            content = response.get("content", {})
            for media_type, media in content.items():
                if "schema" in media:
                    return media["schema"]
    return None
```

## OpenAPI 3.x vs Swagger 2.0 Differences

| Feature | OpenAPI 3.x | Swagger 2.0 |
|---------|-------------|-------------|
| Body param | `requestBody` object | `in: body` parameter |
| File upload | `type: string, format: binary` | `type: file` |
| Responses | `content` map with media types | `produces` + `schema` |
| Security | `securitySchemes` in `components` | `securityDefinitions` |

## Best Practices

1. **Validate before parsing** - Catch errors early
2. **Resolve $refs** - Work with a flat structure
3. **Handle both versions** - Support OpenAPI 3.x and Swagger 2.0
4. **Preserve descriptions** - Use for docstrings
5. **Extract examples** - Include in generated docs