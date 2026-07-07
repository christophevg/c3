# C3 - Christophe’s Agentic Collective

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)][python]
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)][uv]
[![License](https://img.shields.io/github/license/christophevg/c3.svg)][license]
[![Agentic](https://img.shields.io/badge/workflow-agentic-blueviolet?style=flat-square)](https://christophe.vg/about/Agentic-Workflow)

> C3, short for Christophe Agentic Collective, is a personal collective of agents and skills designed for agentic coding and various other purposes. It originated as Christophe’s Coding Crew, which is how the name C3 came to be. Over time, it has undergone significant evolution and has now become known as Christophe’s Agentic Collective. The C3 name has remained consistent throughout its journey. 😉

> [!CAUTION]
> **Before installing any plugin**: Plugins can execute arbitrary commands on your machine. Always review a plugin's code before installing it.

> [!WARNING]  
> This is **my personal collective**. It is in constant flux. I try to keep the plugin version stable and usable, but **YMMV** 😇

## Philosophy

My agentic workflow is built on a simple belief: **create small automation steps, use them, and iteratively improve**. Each skill and agent emerged from real needs, was refined through use, and continues to evolve.

### The Skill Evolution Cycle

```mermaid
flowchart LR
    A[Idea] --> B(["/develop-skill"])
    A --> C(["/develop-agent"])
    B --> D[skills/]
    C --> E[agents/]
    D --> F["claude --plugin-dir ./"]
    E --> F
    F --> G[Use in Sessions]
    G --> H(["/lessons-learned"])
    H --> I[Auto-Improve]
    I --> J{Stable?}
    J -->|No| G
    J -->|Yes| K[Push to GitHub]
```

- **Create**: Use `/develop-skill` or `/develop-agent` to design new skills/agents
- **Test locally**: `claude --plugin-dir ./` loads skills/agents from current directory
- **Use/Refine loop**: Use in sessions, run `/lessons-learned` to capture improvements
- **Distribute**: Push to GitHub when stable

---

## Installation

### As a Plugin (End Users)

Install from the christophe.vg marketplace:

```bash
# Add the marketplace
claude plugin marketplace add christophevg/marketplace

# Install C3
claude plugin install c3@christophe.vg
```

Skills and agents are namespaced (e.g., `/c3:python`, `/c3:commit`).

### Local Development

To develop or test the latest version locally:

```bash
# Clone the repository
git clone https://github.com/christophevg/c3.git
cd c3

# Use in Claude Code session
claude --plugin-dir ./
```

This loads all skills and agents from the current directory into your Claude Code session.

> [!NOTE]
> For project-specific Makefile integration, you can still use `make install` to copy `Makefile.claude` to `~/.claude/`. This provides utility targets for working with Claude Code (e.g., `make` runs Claude Code using Ollama). However, for local development of C3 itself, `--plugin-dir` is the recommended approach.

---

## Skills (54)

Skills provide focused guidance for specific technologies and workflows.

### Plugin & MCP Development (2)

| Skill | Description |
|-------|-------------|
| `/mcp-server` | Guide for designing and building MCP servers (FastMCP, security, deployment). |
| `/plugin-development` | Guide for creating Claude Code plugins (structure, manifest, distribution). |

### Project Management (10)

| Skill | Description |
|-------|-------------|
| `/project` | Dispatcher for project management skills. |
| `/project-feature` | Capture and scope new features with MBI support. |
| `/project-manage` | Full implementation workflow (Phases 0–5) with specialized agents. |
| `/project-review` | Shared review cycle (functional → domain → quality → docs → `make check`). Sub-skill of project-manage. |
| `/project-handle-pr` | PR feedback iteration with review re-entry before push. Sub-skill of project-manage. |
| `/project-post-merge` | Sequenced post-merge cleanup (switch to main before TODO edits). Sub-skill of project-manage. |
| `/project-status` | Generate STATUS.md with executive summary, metrics, dependencies, blockers, risks. |
| `/project-todo-refine` | Iteratively refine TODO.md topics by reviewing state, scope, and priority. |
| `/project-migrate` | Migrate projects between versions or frameworks. |
| `/website-manage` | Manage content websites with conversational workflow. No PRs, no agents. |

### Planning & Prioritization (3)

| Skill | Description |
|-------|-------------|
| `/plan` | Structured feature planning with PLAN.md templates. |
| `/wsjf` | Interactive WSJF (Weighted Shortest Job First) scoring for prioritization. |
| `/bug-hunting` | Systematic debugging with patterns, templates, and integration guides. |

### Personal Assistant (4)

| Skill | Description |
|-------|-------------|
| `/pa` | Main dispatcher for personal assistant workflow. |
| `/pa-inbox` | Process inbox files into actionable TODOs. |
| `/pa-session` | Manage session state for workflow continuity. |
| `/pa-outbox` | Generate formatted replies and manage archive. |

### Domain Expertise (9)

| Skill | Description |
|-------|-------------|
| `/python` | Python coding standards, tight code philosophy, and testing patterns. |
| `/pymongo` | MongoDB/PyMongo patterns and security. |
| `/baseweb` | Baseweb/Vue/Vuetify best practices. |
| `/fire` | Python Fire CLI patterns. |
| `/textual` | Textual TUI framework. |
| `/rich` | Rich console output. |
| `/vuetify-v1` | Vuetify 1.5 components in legacy Baseweb projects. |
| `/vuetify-v2` | Vuetify V2 components in Baseweb projects. |
| `/vuetify-v3` | Vuetify V3 components with comprehensive patterns and migration guide from V2. |

### Development (2)

| Skill | Description |
|-------|-------------|
| `/develop-skill` | Create and refine Claude Code skills. |
| `/develop-agent` | Develop Claude Code agents. |

### Utility (21)

| Skill | Description |
|-------|-------------|
| `/commit` | Git commits with atomic commits and conventional format. |
| `/bug-fixing` | Systematic bug fixing with TDD. |
| `/git-activity-report` | Human-readable git activity summaries. |
| `/git-scripting` | Safe git command usage in scripts. |
| `/naming` | Choose names for projects, products, agents. |
| `/analysis-integration` | Integrate findings from multiple agents. |
| `/lessons-learned` | Review session to improve skills/agents. |
| `/documentation` | Sphinx/readthedocs setup. |
| `/markdown-to-pdf` | Convert Markdown to PDF with TOC. |
| `/readme` | Create and maintain README files. |
| `/transcribe-session` | Curated session transcripts. |
| `/api2mod` | Convert API docs to Python modules. |
| `/spec2mod` | Generate Python from OpenAPI specs. |
| `/vue-form-generator` | Schema-based Vue.js forms. |
| `/ollama` | Python ollama library for LLM integration. |
| `/pyenv` | Manage Python versions. |
| `/pypi-publish` | Publish packages to PyPI. |
| `/mcp-tools` | Work with MCP tools: discovery, naming, sub-agent config. |
| `/release` | Release workflow and version management. |
| `/github` | GitHub operations and PR management. |
| `/research` | Comprehensive research with provenance tracking and source citations. |

### Framework-Specific (6)

| Skill | Description |
|-------|-------------|
| `/vue` | Vue.js framework patterns. |
| `/vuetify-v4` | Vuetify V4 components and patterns. |
| `/quart-webapp` | Quart web application patterns. |
| `/python-project` | Python project setup with uv. |
| `/copy-writer` | Content writing and copy editing. |
| `/prepare-for-exam` | Interactive study material generation. |

---

## Agents (16)

| Agent | Description |
|-------|-------------|
| `assistant` | Personal assistant for inbox processing and workflow coordination. |
| `project-manager` | Project workflow orchestration with multi-task execution. |
| `git-manager` | Git operations via c3:commit skill. |
| `functional-analyst` | Requirements extraction, task planning, and MBI intake. |
| `business-analyst` | Business requirements documents and stakeholder analysis. |
| `researcher` | Comprehensive research with provenance tracking. |
| `api-architect` | API design and architecture. |
| `ui-ux-designer` | User experience and interface design. |
| `python-developer` | Python implementation with tight code philosophy. |
| `code-reviewer` | Code quality review with tight code checklist. |
| `testing-engineer` | Test planning and coverage with tight tests philosophy. |
| `security-engineer` | Security vulnerability assessment. |
| `end-user-documenter` | End-user documentation generation. |
| `knowledge-agent` | Knowledge base querying and evolution. |
| `bug-fixer` | Bug fixing workflow with TDD approach. |
| `release-manager` | Release workflow and GitHub operations. |

---

## MCP Servers (1)

The plugin includes MCP servers that provide tools for Claude Code.

| Server | Tools | Description |
|--------|-------|-------------|
| `email` | 9 tools | Email exchange via IMAP/SMTP with security hardening |

### Email MCP Server

Tools: `list_accounts`, `list_folders`, `search_emails`, `get_email`, `download_attachment`, `send_email`, `reply_email`, `move_email`, `delete_email`

**Prerequisites**: [uv](https://docs.astral.sh/uv/) must be installed. The server uses `uv run` to automatically manage dependencies.

Configuration via environment variables:
```bash
export EMAIL_IMAP_HOST=imap.gmail.com
export EMAIL_SMTP_HOST=smtp.gmail.com
export EMAIL_USERNAME=your-email@gmail.com
export EMAIL_PASSWORD=your-app-password
```

Optional recipient whitelist:
```bash
export EMAIL_RECIPIENT_DOMAINS=example.com,company.org
```

---

## Project Management Workflow

The `/project` skill dispatcher handles one-off operations, while the `project-manager` agent orchestrates multi-task sessions with progress tracking and memory persistence.

```mermaid
flowchart TB
    subgraph Phase0["Phase 0: Session Start & Triage"]
        A["User Request"] --> B{"Task Type?"}
        B -->|Bug| C["c3:bug-fixer"]
        B -->|Dependency| D["c3:researcher"]
        B -->|Feature| E["Issue Triage"]
        D --> E
        E --> G{"Project State?"}
        G -->|"Open PR w/ feedback"| HP["c3:project-handle-pr (Phase 6)"]
        G -->|"Merged branch"| PM["c3:project-post-merge (Phase 7)"]
        G -->|"Clean / open issues"| I["Phase 1 / Issue Triage"]
    end

    subgraph Phase1["Phase 1: Analysis (conditional)"]
        I --> J{"State?"}
        J -->|"New Project"| K["Phase 1A: Initial Analysis"]
        J -->|"Incomplete Setup"| L["Phase 1B: Review"]
        J -->|"Ready for Work"| M["Phase 2: Task Selection"]
        K --> N["functional-analyst"]
        L --> N
        N -->|Optional| O["c3:researcher"]
        O --> N
        N -->|"functional.md + TODO.md + PLAN.md"| M
    end

    subgraph Phase2["Phase 2: Task Selection"]
        M --> Q{"Unsorted items / MBIs?"}
        Q -->|Yes| R["Sort / Analyze / Skip"]
        Q -->|No| S["Priority: Active MBI > Fixes > Backlog"]
        R -->|Sort| N
        R -->|Skip| S
        S --> SV{"Already implemented?"}
        SV -->|Yes| S
        SV -->|No| T["Propose Next Task (AskUser)"]
        T -->|Approved| SC{"Scope?"}
    end

    subgraph Phase3["Phase 3: Cross-Domain Review (parallel)"]
        SC -->|Backend| U["api-architect"]
        SC -->|Frontend| V["ui-ux-designer"]
        SC -->|"Full Stack"| U
        SC -->|"Full Stack"| V
        SC -->|Security| W["security-engineer"]
    end

    subgraph Phase4["Phase 4: Consensus"]
        U --> X["Consensus report"]
        V --> X
        W --> X
        X --> CA{"All approve?"}
        CA -->|No| X
        CA -->|Yes| BR["Phase 5: Implementation"]
    end

    subgraph Phase5["Phase 5: Implementation"]
        BR --> FB["Feature branch + commit analysis docs + draft PR"]
        FB --> PL["Post plan as PR comment"]
        PL --> GATE{"Plan Approval Gate (BLOCKING)"}
        GATE -->|Changes| PL
        GATE -->|Rejected| CLOSE["Close PR + issue"]
        GATE -->|Approved| SK["Check domain skills"]
        SK --> Z["python-developer implements (incremental)"]
        C -->|"scoped (no plan gate)"| RV
        Z --> RV["c3:project-review (Stage a-f)"]
        RV -->|rejected| Z
        RV -->|approved| MK["make check gate + summary"]
        MK --> CP["Commit, push, PR, CI (fix until green)"]
        CP --> RD["Mark ready, assign, request owner review"]
        RD --> PAUSE["PAUSE - do not poll"]
    end

    subgraph Phase6["Phase 6: PR Iteration - c3:project-handle-pr"]
        PAUSE --> FBC{"Owner comments?"}
        FBC -->|No| WAIT["Report & wait"]
        FBC -->|Yes| FA["functional-analyst interprets vs task"]
        FA --> DEV["python-developer implements change"]
        DEV --> RV2["c3:project-review (scoped re-run)"]
        RV2 -->|rejected| DEV
        RV2 -->|approved| PUSH["Commit, push, comment on PR"]
        PUSH --> APP{"Owner approves?"}
        APP -->|"More changes"| FBC
        APP -->|Approved| MERGE["Wait for owner to merge"]
    end

    subgraph Phase7["Phase 7: Post-Merge - c3:project-post-merge"]
        MERGE --> SW["Switch to main + pull (BEFORE TODO edits)"]
        SW --> TD["functional-analyst: mark task done in TODO.md"]
        TD --> CM["Commit TODO.md"]
        CM --> CL["Clean up issue labels / close"]
        CL --> NX{"Release or next task?"}
        NX -->|Release| REL["c3:release"]
        NX -->|Next| M
    end
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

[MIT](LICENSE)

[python]: https://python.org/
[uv]: https://docs.astral.sh/uv/
[license]: LICENSE
