---
name: project-migrate
description: |
  Use this skill when migrating existing Python projects to the uv-based standard. Migrates pyproject.toml, Makefile, GitHub Actions, ReadTheDocs, and removes legacy files. Examples: "migrate project to uv", "update project to new standard", "modernize Python project setup", "add uv support to old project", "bring project up to standard", "setup uv for existing project", "convert legacy setup to uv".
type: knowledge
---

# Python Project Migration to uv

Migrate existing Python projects to the uv-based standard. Every step
preserves the full reference content of the target state; the `python-project`
knowledge skill is the normative standard — this skill sequences the
migration and validates it.

## Triggering

- "migrate project to uv", "update project to new standard", "modernize
  Python project setup", "add uv support to old project", "bring project
  up to standard", "convert legacy setup to uv"
- legacy setup present: setup.py / setup.cfg, requirements*.txt, tox.ini,
  .coveragerc, or pyenv-only pinning

# Inputs

A Python project not yet on the uv standard, checked out locally.

# Migration checklist (verify all)

| File | Check |
|------|-------|
| `pyproject.toml` | hatchling backend, uv tool config, separate docs extra |
| `Makefile` | uv targets, `-include ~/.yoker/Makefile` |
| `.python-version` | uv-format pinned dev version |
| `.readthedocs.yaml` | Python 3.12, pip install with the `docs` extra |
| `.github/workflows/test.yaml` | multi-OS, uv-based CI, 4 jobs |
| `README.md` | project root, not `.github/` |
| `requirements*.txt`, `setup.py`, `setup.cfg`, `tox.ini`, `.coveragerc` | removed — content migrated to pyproject.toml |

## Migration steps

### 1 — pyproject.toml

Restructure to the canonical uv standard (full template in `c3:python-project`;
section order there is authoritative): `[build-system]` (hatchling) →
`[project]` → optional-dependencies with **dev and docs as separate
extras** → `[project.urls]`/`[project.scripts]` → hatch build config →
pytest/mypy/ruff/coverage tool config → tox with the `commands_pre`
workaround.

Hatch wheel-packaging pitfall: never combine `sources` and a `src/`
prefixed `packages` (empty wheel). Use `packages = ["package_name"]` with
`sources = ["src"]`, or drop `sources` and keep the `src/` prefix.

### 2 — Makefile

Adopt the standard target set (`env-dev`, `env-run`, `install-pythons`,
`test`, `test-cov`, `test-all`, `format`, `lint`, `typecheck`, `check`,
`run`, `docs`, `docs-view`, `build`, `publish`, `clean`, `clean-all`,
`help`) with `uv` everywhere and `-include ~/.yoker/Makefile` at the top.
`check` order: format → lint → typecheck → test. `docs` runs
`sphinx-build -M html . _build` directly — never `make html` (needs a
docs/Makefile that doesn't exist).

### 3 — .python-version

Pin the development Python (3.12), uv format.

### 4 — .readthedocs.yaml

Python 3.12, sphinx config path, and `extra_requirements: - docs` — never
`dev` (installs too much) and never a separate requirements file.

### 5 — GitHub Actions (`.github/workflows/test.yaml`)

Four jobs: `test` (matrix: ubuntu/macos/windows × 3.10/3.11/3.12,
`astral-sh/setup-uv@v5`, `uv sync --frozen --all-extras`, pytest),
`lint` (ruff check + format --check), `typecheck` (mypy), `build`
(needs the other three, `uv build`). A missing job means that aspect is
unverified in CI — all four are required.

### 6 — Legacy-file removal

Remove `requirements*.txt`, `setup.py`/`setup.cfg`, `tox.ini`,
`.coveragerc`, and any `.github/README.md` after moving it to root.

### 7 — Verify

From a clean slate: `rm -rf .venv && uv sync --all-extras`, then
`make check` (format, lint, typecheck, test), `make build`, `make docs`.
Per-file greps (docs-extra separation, RTD extra, Makefile target-set,
workflow jobs) in the tables above are the verification surface.

Common failures: tox missing interpreters → `make install-pythons` first;
tox-uv `ModuleNotFoundError` → `commands_pre` workaround; `command not
found` in CI → `uv sync --frozen --all-extras`; coverage misses →
`--cov=package_name`, not `--cov=src`.

## Post-migration

1. Commit the migration (`migrate: update project to uv-based standard`).
2. TODO.md: remove the completed migration task (canonical — no Done
   section).
3. Push and confirm the Actions run is green.
4. Optional cleanup: remove pyenv-era files; the standard is uv-only now.

# Deliverables

- A migrated project passing `make check`, `make build`, `make docs`, with
  CI green on the pushed commit.

# Related

- `c3:python-project` — the reference standard being migrated to
- `c3:python`, `c3:readme` — code and README conventions
- `c3:commit` — commit discipline for the migration commit

# Never

- Mix docs dependencies into the dev extra.
- Ship with conflicting hatch `sources`/`packages` build config.
- Skip the clean-slate verification (`rm -rf .venv` → full sync → gates).