# A set of coding guidelines

TODO: review and filter, I don't want all this. It's inspiration for now.

## KISS (Keep It Simple, Stupid)

* Prefer simple, minimal solutions.
* Avoid premature optimization—profile first.
* Skip unnecessary abstractions.
* Don’t use heavy libraries (e.g., ORMs, frameworks) unless needed.
* Use code reviews to enforce simplicity.

## Avoid Overengineering

* Don’t build for hypothetical futures.
* Apply the "Rule of Three" for abstraction.
* Scripts don’t need full configs or test suites.
* Balance with sufficient logging, error handling.

## App Type Scaling

* Scripts/CLI: Flat, minimal.
* Backends: Start monolithic, modularize gradually.
* APIs: Use lightweight frameworks unless complexity justifies more.
Code Style, Formatting & Linting

## Formatters

**Black: Opinionated, auto-formats code (default line length: 88).
** Use black . via pre-commit.

## Linters

* Ruff: Fast, combines Flake8, isort, pydocstyle, etc.
* Prefer over Flake8 or Pylint for most workflows.
* Configure in pyproject.toml.

## Type Checkers

* Use mypy or pyright for static analysis.
* Run with -strict in production code.

## Setup

* Use pre-commit for automated checks.
* Enforce in CI for team projects.

## Type Annotations

### Why Use

Improves clarity, tooling, and bug detection.

### Guidelines

* Annotate function signatures and public variables.
* Use | for unions (Python 3.10+), Literal, Optional, Generic, etc.
* Avoid over-typing internals unless complex.

## #Tools

* Use typing_extensions for compatibility.
* Integrate mypy into CI.

## Naming & Self-Documenting Code

* Variables: Use descriptive names (e.g., user_email, not ue).
* Functions: Use verb-noun (e.g., calculate_total()).
* Classes: Use nouns (e.g., UserService).
* Avoid nonstandard abbreviations.
* Write self-explanatory code using types and structure, not excess comments.
* Use consistent docstrings (Google/Numpy format).

## Avoid Magic Strings/Numbers

* Use Enum for fixed value sets.
* Define constants in UPPERCASE.
* Use config objects (e.g., Pydantic, dataclasses) over raw dicts.
* Use linters to detect common issues (e.g., hardcoded secrets).

## Development Practices

### Test-Driven Development (TDD)

* Write tests first → code → refactor.
* Use pytest with fixtures, parametrization.

### Other Styles

* BDD: pytest-bdd, behave.
* DDD: Isolate domain logic for complex apps.
* Functional: Use immutability, avoid side effects.

### Tools

* hypothesis: Property-based testing.
* pact: Contract testing for APIs.


## Web Framework Choices

### Summary

Simple API -->	Flask
Async API	--> FastAPI
Full-stack app -->	Django

* FastAPI: Async, typed, auto-docs. Use for modern, performant APIs.
* Flask: Lightweight, unopinionated. Great for simple services.
* Django: Feature-rich. Best for content-heavy or full-stack apps.

## Async Usage Guidelines

* Use async for I/O-bound work (DB, HTTP).
* Stick with asyncio, httpx, aiohttp.
* Avoid mixing sync/async without care.
* Handle exceptions in asyncio tasks.
* Use pytest-asyncio for testing.

## Modern Configuration Management

* Use pydantic-settings for env-based config validation.
* Store secrets in env vars; load with .env or secret managers.
* Avoid hardcoding config values.
* Prefer TOML/YAML for structured config files.

## Logging

* Use Python’s built-in logging module.
* Levels: DEBUG → INFO → WARNING → ERROR → CRITICAL.
* Avoid print() in production.
* Use structlog for structured, JSON-friendly logging.
* Log exceptions with tracebacks and contextual info.

## Package Management Best Practices

* Prefer Poetry for dependency + packaging.
* Use virtual environments (venv, pyenv, or Poetry).
* Audit with pipdeptree, pip-audit, safety.
* Lock dependencies (poetry.lock, requirements.txt).
* Separate dev/test/prod dependencies.
* Avoid unnecessary packages in small projects.

## CI/CD Integration

* Automate linting, testing, and type checking in CI.
* Use GitHub Actions, GitLab CI, or similar.
* Include security checks (bandit, safety).
* Add status badges to the repo.
* Use pre-commit for local consistency.

## Error Handling

* Catch specific exceptions; avoid bare except:.
* Define custom exceptions for domain errors.
* Include contextual info in error messages.
* Use try/except/else/finally patterns appropriately.
* Handle async task failures gracefully.

## Security Best Practices

* Never hardcode credentials or tokens.
* Sanitize all user input (API, CLI, forms).
* Use HTTPS, CSRF protection, and secure headers.
* Rate-limit endpoints to prevent abuse.
* Use proper authentication (OAuth2, JWT).
* Monitor for dependency vulnerabilities (dependabot, renovate, etc).

## i18n & l10n (Internationalization & Localization)

* Externalize user-facing strings.
* Use gettext or similar for translatable text.
* Format dates, currencies, numbers with Babel.
* Design for language fallback and right-to-left support if needed.

## Data Privacy

* Minimize use of PII; obfuscate when not needed.
* Encrypt sensitive data at rest and in transit.
* Avoid logging confidential or personal data.
* Ensure compliance with GDPR/CCPA if relevant.

## Documentation

* Use consistent docstring style (Google, NumPy, or reST).
* Document public classes/functions/modules.
* Generate docs with Sphinx or MkDocs.
* Include architecture overview and usage in README.md.
* Maintain CHANGELOG.md using SemVer and "Keep a Changelog" style.

## Team Collaboration Practices

* Use consistent Git workflow: feature branches, Conventional Commits.
* Enforce pull requests and code reviews.
* Maintain onboarding docs and setup guides.
* Use ADRs (architecture decision records) for important design decisions.

## Application-Type Specific Recommendations

### Backend Development

* Use FastAPI or Django.
* Structure code into services, repos, schemas.
* Use Docker, CI/CD, monitoring (Prometheus, Grafana).
* Type everything, test with pytest + coverage.

### Frontend with Python

* Use Streamlit, Gradio, Dash.
* Separate UI logic from backend.
* Use Playwright for UI testing.

### API Development

* Use FastAPI + Pydantic + async.
* Implement OpenAPI docs, rate limiting, auth.
* Use response models and versioned routes (e.g., /v1/).

### Code Maintenance

* Use Git with semantic versioning.
* Refactor regularly with tools like Sourcery.
* Scan dependencies (pip-audit, bandit).
* Cache frequently used data (e.g., Redis).
* For legacy code: test → type → refactor gradually.
