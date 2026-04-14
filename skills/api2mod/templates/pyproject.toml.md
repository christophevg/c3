# pyproject.toml Template

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "{{package_name}}"
version = "0.1.0"
description = "{{api_description}}"
readme = "README.md"
requires-python = ">=3.10"
license = "MIT"
authors = [
    { name = "{{author_name}}" }
]
dependencies = [
    "requests>=2.28.0",
    "aiohttp>=3.8.0",
    "prompt_toolkit>=3.0.0",
    "rich>=13.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "mypy>=1.0.0",
    "ruff>=0.0.260",
]

[project.scripts]
{{package_name}} = "{{package_name}}.__main__:main"

[tool.hatch.build.targets.wheel]
packages = ["src/{{package_name}}"]

[tool.mypy]
python_version = "3.10"
strict = true
warn_return_any = true
warn_unused_ignores = true

[tool.ruff]
line-length = 100
select = ["E", "F", "I", "N", "W"]
```

## Placeholders

| Placeholder | Source |
|-------------|--------|
| `{{package_name}}` | User input (suggested from API title) |
| `{{api_description}}` | OpenAPI `info.description` |
| `{{author_name}}` | User input or git config |

## Dependency Rationale

| Dependency | Purpose |
|------------|---------|
| `requests` | Sync HTTP client |
| `aiohttp` | Async HTTP client |
| `prompt_toolkit` | Advanced REPL input/completion |
| `rich` | Pretty output formatting |

## Notes

- Uses `hatchling` for modern PEP 517 build
- Entry point enables `{{package_name}}` command
- mypy strict mode ensures type safety
- ruff for fast linting