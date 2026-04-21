# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

*Nothing yet*

## [1.1.4] - 2026-04-21

### Fixed

- Email MCP server config now treats empty environment variables as `None`
  - Pydantic `env_parse_none_str=""` setting converts empty strings to None
  - Fixes validation errors when optional env vars are set but empty
- Email MCP SEARCH now handles iCloud's non-standard response format
  - iCloud returns "SEARCH completed (took X ms)" instead of message IDs when empty
  - Correctly returns empty list instead of parsing status message as IDs

## [1.1.3] - 2026-04-20

### Fixed

- Email MCP server now uses `uv run` for automatic dependency management
  - Workaround for Claude Code bug where `cwd` field in `.mcp.json` is ignored
  - Dependencies are automatically installed from `pyproject.toml`
  - Updated documentation to require `uv` as a prerequisite

## [1.1.2] - 2026-04-20

### Fixed

- Email MCP server failed to start due to incorrect module invocation
  - Created `__main__.py` entry point for `python -m email_mcp`
  - Fixed `cwd` path in `.mcp.json` (was `email`, should be `email/src`)
  - Fixed module invocation (was `email_mcp.server`, should be `email_mcp`)
  - Added dependency installation instructions to READMEs

## [1.1.1] - 2026-04-20

### Fixed

- Removed invalid `mcpServers` section from `plugin.json` that caused validation errors during plugin installation (MCP configuration belongs in `.mcp.json`)

## [1.1.0] - 2026-04-20

### Added

- **Email MCP Server** - MCP server for email exchange via IMAP/SMTP
  - 9 MCP tools: `list_accounts`, `list_folders`, `search_emails`, `get_email`, `download_attachment`, `send_email`, `reply_email`, `move_email`, `delete_email`
  - IMAP client with `aioimaplib` for async email operations
  - SMTP client with `aiosmtplib` for async email sending
  - Recipient whitelist support for restricting email recipients
  - Security features: rate limiting, audit logging, TLS 1.2 minimum, path traversal protection
  - Configuration via environment variables (supports single account, multiple accounts via JSON, OAuth2)
  - Foundational test suite for configuration, rate limiting, path traversal, and whitelist

### Changed

- Updated plugin.json with MCP server metadata
- Added `.mcp.json` for MCP server configuration

## [1.0.1] - 2026-04-20

### Added

- Git safety protocol in `commit` skill (no config changes, no hook skipping, no amending, no force push)
- HEREDOC syntax for commit messages in `commit` skill
- Repository style checking in `commit` skill
- Pre-commit hook failure handling guidance in `commit` skill
- Bash tool to `assistant` agent for shell command support

### Fixed

- Attribution footer in commits (now reads from `settings.json`)

### Changed

- Re-enabled statusline in settings
- Updated plugin configuration for C3 activation

## [1.0.0] - 2026-04-20

### Added

- MIT License for public release
- CONTRIBUTING.md with contribution guidelines
- CHANGELOG.md generated from git history
- `bin/validate.py` - Validation script for skills and agents structure
- `bin/version.py` - Version management script for bumping versions and preparing releases
- `PERSONAL.md.template` - Template for user personal configuration
- Badges in README.md (platform, license)
- Prerequisites section in README.md
- `mcp-server` skill - Guide for designing and building MCP servers (FastMCP, security, deployment)
- `plugin-development` skill - Guide for creating Claude Code plugins (structure, manifest, distribution)
- Personal Assistant skills: `pa`, `pa-inbox`, `pa-outbox`, `pa-session` - Workflow for processing unstructured input
- `assistant` agent - Personal assistant agent for inbox processing
- `.claude-plugin/plugin.json` - Plugin manifest for Claude Code plugin distribution
- `.claude/skills/release/` - Project-level skill for version management (not part of plugin)
- Plugin installation method via marketplace (`claude plugin install c3@christophe.vg`)
- Makefile targets for version management (`version-current`, `version-bump-*`, `release-*`, `tag`)
- `make local` target for testing with `--plugin-dir ./`

### Changed

- Transformed C3 from symlink installation to Claude Code plugin
- Removed symlink-based installation from Makefile (use `--plugin-dir` for local testing)
- Updated README.md to focus on plugin installation with local development workflow
- Added skill evolution cycle diagram to README
- Added plugin security disclaimer to README
- Updated `settings.json` to use narrower permissions (removed `Bash(python:*)`)
- Plugin is distributed via GitHub through the christophe.vg marketplace

## [0.1.0] - 2026-04-17

### Added

- **Agents** (10 specialized agents)
  - `functional-analyst` - Requirements extraction and task planning
  - `researcher` - Comprehensive research with provenance tracking
  - `api-architect` - API design and architecture
  - `ui-ux-designer` - User experience and interface design
  - `python-developer` - Python implementation following conventions
  - `code-reviewer` - Code quality and best practices review
  - `testing-engineer` - Test planning and coverage analysis
  - `security-engineer` - Security vulnerability assessment
  - `end-user-documenter` - Documentation generation
  - `knowledge-agent` - Knowledge base querying and evolution

- **Skills** (33 skills across categories)
  - Project Management: `project`, `project-feature`, `project-manage`, `project-status`
  - Domain Expertise: `python`, `pymongo`, `baseweb`, `fire`, `textual`, `rich`
  - Development: `develop-skill`, `develop-agent`
  - Utility: `commit`, `bug-fixing`, `git-activity-report`, `git-scripting`, `naming`, `analysis-integration`, `lessons-learned`, `plan-review`, `documentation`, `markdown-to-pdf`, `readme`, `transcribe-session`, `api2mod`, `spec2mod`, `start-baseweb-project`, `vue-form-generator`, `vuetify-v1`, `vuetify-v2`, `ollama`, `pyenv`, `pypi-publish`

- **Infrastructure**
  - `bin/statusline.py` - Claude Code status line display
  - `settings.json` - Claude Code configuration
  - `Makefile` - Installation and management targets
  - `CLAUDE.md` - Project guidance for Claude
  - `CLAUDE.global.md` - Global user instructions

### Features from Development History

#### 2026-04-17
- Enhanced `ollama` skill with image generation, web search, and API documentation
- Added `pypi-publish` skill for PyPI package publishing
- Added `readme` skill for README maintenance
- Added `knowledge-agent` for KB querying and evolution

#### 2026-04-16
- Reorganized project management into dispatcher pattern
- Enhanced `develop-skill` with context detection workflow
- Added `git-activity-report`, `naming`, `pyenv` skills
- Added `spec2mod` skill for OpenAPI to Python module generation
- Simplified `api2mod` to orchestrator role

#### 2026-04-14
- Added `develop-agent` and `develop-skill` for creating new skills/agents
- Enhanced `project-manage` workflow with diagrams and security review
- Added AskUserQuestion guidance and import organization patterns

#### 2026-04-13
- Added Eira identity and naming documentation
- Enhanced `researcher` with completeness audit

#### 2026-04-11
- Added `ollama`, `rich`, `textual` domain skills
- Added `documentation` skill for Sphinx/readthedocs
- Added `git-scripting` skill for safe git operations

#### 2026-04-06
- Split Vuetify skill into v1 and v2 variants
- Restructured `baseweb` skill with patterns and templates
- Enhanced `api-architect` with invocation triggers

#### 2026-04-02
- Added `markdown-to-pdf` skill
- Enhanced `lessons-learned` with improved review process

#### 2026-03-29
- Added `transcribe-session` skill
- Enhanced `lessons-learned` scope
- Added statusline improvements

#### 2026-03-26
- Initial import of C3 (Christophe's Coding Crew)
- Added `code-reviewer` to workflow
- Added TODO.md template
- Added CLAUDE.md and README.md
- Created initial skill and agent structure

#### 2026-03-25
- Initial project creation