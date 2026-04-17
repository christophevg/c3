# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- MIT License for public release
- CONTRIBUTING.md with contribution guidelines
- CHANGELOG.md generated from git history
- `bin/validate.py` - Validation script for skills and agents structure
- `PERSONAL.md.template` - Template for user personal configuration
- Badges in README.md (platform, license)
- Prerequisites section in README.md

### Changed

- Separated personal configuration from `CLAUDE.global.md` into `~/.claude/PERSONAL.md`
- `CLAUDE.global.md` now uses `@~/.claude/PERSONAL.md` import for personal preferences
- Added `make validate` target to Makefile
- Fixed `pyenv` skill missing frontmatter
- Updated `.gitignore` to exclude `PERSONAL.md`

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