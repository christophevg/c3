---
name: api2mod
description: Convert API documentation into Python modules. Orchestrates doc2spec and spec2mod skills. Use when user mentions api2mod, converting API to module, or wants to generate a Python client from API docs or specs.
---

# api2mod

Orchestrator skill that converts API documentation into Python packages. Delegates to specialized sub-skills based on input format.

## Architecture

```
api2mod (orchestrator)
    │
    ├─→ doc2spec: API docs (HTML, PDF, wiki) → OpenAPI spec
    │
    └─→ spec2mod: OpenAPI/Swagger/Postman spec → Python module
```

## When to Use This Skill

Use this skill when:
- User asks to convert API documentation to Python module
- User wants to generate a client library from OpenAPI/Swagger
- User mentions "api2mod"
- User provides an API spec file or documentation URL

## Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                     api2mod (orchestrator)                   │
├─────────────────────────────────────────────────────────────┤
│  1. Detect input format                                       │
│  2. Route to appropriate sub-skill                           │
│  3. Coordinate execution                                      │
│  4. Verify output                                            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
         ┌────────────────────────────────────────┐
         │         Format Detection               │
         ├────────────────────────────────────────┤
         │  OpenAPI YAML/JSON  →  spec2mod        │
         │  Swagger JSON       →  spec2mod        │
         │  Postman Collection →  spec2mod        │
         │  Insomnia Export    →  spec2mod        │
         │  HTML/PDF/Wiki Docs →  doc2spec → spec2mod │
         └────────────────────────────────────────┘
```

## Step 1: Gather Requirements

Ask the user for:
1. **API documentation source** - File path or URL to API docs/spec
2. **Package name** - Suggest sensible default from API title
3. **Output location** - Default to current directory

## Step 2: Detect Format and Route

Detect the API documentation format and delegate accordingly:

### OpenAPI/Swagger/Postman/Insomnia → Use spec2mod

If the input is a structured API specification:

| Format | Detection |
|--------|-----------|
| OpenAPI JSON | `"openapi"` key in JSON |
| OpenAPI YAML | `openapi:` at root |
| Swagger JSON | `"swagger"` key with version |
| Postman | `"info"` with `"_postman_id"` |
| Insomnia | `"_type": "export"` |

**Action**: Call `spec2mod` skill with the spec file and output location.

```
Use Skill tool:
  skill: "spec2mod"
  args: "<spec_file> --output <output_dir>"
```

### HTML/PDF/Wiki Documentation → Use doc2spec then spec2mod

If the input is unstructured API documentation:

| Format | Examples |
|--------|----------|
| HTML docs | Confluence, ReadTheDocs, API reference pages |
| PDF | API documentation PDFs |
| Wiki | Atlassian wiki, GitHub wiki |

**Action**:
1. Call `doc2spec` to convert docs to OpenAPI spec
2. Then call `spec2mod` with the generated spec

```
Use Skill tool:
  skill: "doc2spec"
  args: "<docs_url_or_file> --output <temp_spec.yaml>"

Then:
  skill: "spec2mod"
  args: "<temp_spec.yaml> --output <output_dir>"
```

## Step 3: Verify Output

After the sub-skill completes, verify:
1. Package structure is correct
2. Client can be imported
3. REPL runs without errors

## Example Usage

### From OpenAPI Spec

```
User: api2mod ~/myapi/openapi.yaml --output ./myapi-client

Agent:
1. Detects OpenAPI YAML format
2. Calls spec2mod with the spec file
3. spec2mod generates the Python package
```

### From API Documentation URL

```
User: api2mod https://api.example.com/docs --output ./example-client

Agent:
1. Detects HTML documentation format
2. Calls doc2spec to extract OpenAPI spec
3. Calls spec2mod with the generated spec
4. Generates Python package
```

## Related Skills

| Skill | Responsibility |
|-------|----------------|
| `doc2spec` | Convert unstructured docs to OpenAPI spec |
| `spec2mod` | Generate Python module from OpenAPI spec |
| `api-architect` | Design APIs (opposite direction) |