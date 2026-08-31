---
name: release
description: |
  Standardize release preparation and publishing workflow. Use when preparing a release, publishing to PyPI, or release-manager starts release process. Handles version bump decisions, changelog updates, CI verification, tagging, GitHub release, and PyPI upload. Two owner gates: version decision and final pre-PyPI confirmation.
type: workflow
---

# Release

Standardized release workflow for Python packages, from version decision to
PyPI publication. Two standing owner gates; everything between them runs
autonomously.

## Triggering

- owner asks to "prepare release" or "publish"
- release-manager starts the release process
- post-merge, ready to release

# Inputs

A repository at release readiness (PR merged, CI green), the owner's
version decision (Gate 1), and — before upload — the owner's final
confirmation (Gate 2).

## Owner gates (authoritative)

1. **Version decision** — propose the semver bump with commit-based
   evidence; the owner decides the target version. Do not start file
   changes before approval.
2. **Final confirmation before PyPI upload** — after CI green, build and
   verification, present the state (version, changelog entry, tag, wheel
   contents) and wait for explicit approval. PyPI publishes are
   irreversible; no upload without it.

Everything from changelog through GitHub release runs autonomously once
the version is approved. A4: CI green is the **authoritative** quality
gate — local checks prepare, CI decides; a local `make check` pass never
substitutes for a pending CI run.

## Workflow

### 1 — Determine the bump

Read `version` from `pyproject.toml`; list commits since the last tag via
the `git` tool (`git(operation="log", args={ref: "vX.Y.Z..HEAD", oneline:
true})`). Decision rules: `feat:` present → minor; only `fix:` → patch;
breaking API → major; unclear → ask (that IS gate 1 if no version
decision was given).

### 2 — Update version artifacts

- `pyproject.toml` `version`
- any `__version__` in `src/**/__init__.py`
- `CHANGELOG.md` release section (Added / Fixed / Changed), extracted
  from commits since the last tag
- Verify sync: both locations match exactly; `uv.lock` self-updates.

### 3 — Pre-publish checks (local)

`uv sync --all-extras`; `make test`, `make lint`, `make typecheck` —
all green before committing. Fix failures, don't route around them.

### 4 — Commit and push

Version files + changelog in one commit:
`chore: bump version to X.Y.Z` (attribution line per `c3:commit`), push;

### 5 — CI wait (authoritative)

Poll `github(operation="workflow_list", limit=3)` every 60s (`sleep`
tool) until the run reports `status="completed"`. `workflow_view` returns
single-line JSON that overflows on big matrix runs — only for a completed
run's job-level verdict; failures via `workflow_logs` with a failure
pattern. Filter cookbook (shared with release-manager persona):

```
pytest:   ^FAILED|^ERROR|^E |short test summary|no tests ran
collect:  ERROR collecting|^ERRORS|evaluation failed
make:     Error [12]|make: \*\*\*|^make\[1\]: \*\*\*
CI:       ##\[error\]
```

Substring pitfalls: "passed" matches "bypassed"; `.` matches everything;
anchors can fail on decorated output (Yoker #58). Two size-failures on
one command → stop, report from captured lines.

CI strictly precedes ready-for-review and any tagging. Red → report logs,
halt, fix, push, wait again.

### 6 — Build and verify the package

Clean `dist/`/`build//*.egg-info`, then `uv build`. Verify before any
upload: wheel contents show real source files (not just `.dist-info/`),
correct structure, no local paths. Empty wheel → fix hatch `packages`
(conflicting `sources` + `packages = ["src/..."]` is the classic cause —
never combine `[tool.hatch.build] sources` with `packages = ["src/..."]`;
with `sources = ["src"]`, packages must be relative: `["package_name"]`),
rebuild.

**Pre-upload content checks (all before gate 2):**

- **README image paths are absolute** — PyPI does not serve relative
  paths from the package; use `raw.githubusercontent.com` URLs:
  `![Alt](https://raw.githubusercontent.com/owner/repo/main/media/image.svg)`.
  Relative paths (`media/image.svg`, `docs/image.png`) silently render
  broken on PyPI.
- **No local-path references in pyproject.toml** — `[tool.uv.sources]`
  and `[tool.uv.workspace]` reference paths that don't exist on PyPI and
  make uploads fail with "Invalid URL": remove before publishing.
- **Version synced across files** — `pyproject.toml` `version` and any
  `__version__` in `src/**/__init__.py` match exactly.
- **Entry point sanity** — `[project.scripts]` targets an existing module.

### 7 — Tag and GitHub release

After CI green: annotated tag `vX.Y.Z` pushed; GitHub release via
`github_tool release_create` with notes extracted from the changelog
(Summary, Changes, Installation). The tag push is not itself release
gated beyond CI green — the owner's version decision (gate 1) already
covered it.

### 8 — PyPI upload — after gate 2

`uv run twine upload dist/*` (or the project's `make upload` — the
granular target, never a full `make publish` re-run).

**If upload fails (e.g. HTTP 400):**
1. Check PyPI first — the upload may have partially succeeded (one file
   in, one rejected). Verify on pypi.org before retrying.
2. Retry the upload only (`make upload` / twine), never the full publish
   pipeline.
3. Max 3 retries, then stop and ask the owner.

**Verify publication:** the PyPI project page shows the new version; test
install `uv pip install package==X.Y.Z`.

# Deliverables

- Bumped, tagged, GitHub-released, and published package; verification
  evidence (CI run, wheel listing, PyPI page) reported in one block.

# Related

- `c3:release-manager` — the delegate that executes git/GitHub operations
  and CI polling during a release
- `c3:commit` — commit discipline
- `c3:github` — PR/CI/release operations vocabulary
- `c3:project-manage` — the managed-mode caller after PR merge

## Never

- Upload to PyPI without the owner's final confirmation (gate 2).
- Tag, release, or declare ready-for-review while CI is red.
- Re-run the full publish pipeline to retry an upload.
- Propose a changelog section the commits don't support — flag anomalies
  for the owner instead.

## Common failures

| Issue | Action |
|-------|--------|
| CI fails after push | Fix, commit, push, wait again |
| Empty wheel (module not found after install) | Fix hatch `packages` config (see step 6), rebuild |
| Version already on PyPI | Cannot overwrite — bump the version |
| Upload HTTP 400 | May have partially succeeded — check pypi.org before retrying; retry upload-only; max 3 attempts |
| Upload fails with "Invalid URL" | `[tool.uv.sources]` / `[tool.uv.workspace]` still present — remove them |
| Broken images on PyPI page | README uses relative image paths — switch to `raw.githubusercontent.com` URLs |