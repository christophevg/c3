---
name: release
description: |
  Standardize release preparation and publishing workflow. Use when preparing a release, publishing to PyPI, or release-manager starts the release process. Covers release readiness audit, content & documentation sync (incl. functional-analysis consolidation), version bump decision, changelog updates, CI verification, tagging, GitHub release, PyPI upload, and post-publication ecosystem sync (satellite projects, website, announcement post). Two owner gates: version decision and final pre-PyPI confirmation.
type: workflow
---

# Release

Standardized release workflow for Python packages, from readiness audit to
ecosystem sync. Two standing owner gates; everything between them runs
autonomously (plus two owner touchpoints: demos visual check, ecosystem-sync
review).

## Triggering

- owner asks to "prepare release" or "publish"
- release-manager starts the release process
- post-merge, ready to release

# Inputs

A repository at release readiness (PR merged, CI green), the owner's
version decision (Gate 1), and — before upload — the owner's final
confirmation (Gate 2). For ecosystem sync: the project's list of satellite
projects and website (documented in the project's AGENTS.md or release
runbook).

## Owner gates (authoritative)

1. **Version decision** — propose the semver bump with commit-based
   evidence; the owner decides the target version. Do not start file
   changes before approval.
2. **Final confirmation before PyPI upload** — after CI green, build and
   verification, present the state (version, changelog entry, tag, wheel
   contents) and wait for explicit approval. PyPI publishes are
   irreversible; no upload without it.

Owner touchpoints (review, not gates): demos visual check (R1) and
ecosystem-sync review (R8). Everything from readiness audit through GitHub
release runs autonomously once the version is approved. CI green is the
**authoritative** quality gate — local checks prepare, CI decides; a local
`make check` pass never substitutes for a pending CI run.

## Workflow

### R0 — Release readiness audit (before Gate 1)

Verify the repository is actually ready to release — do not assume the
merge means it:

1. **Working tree clean** — all changes committed and pushed; the local
   default branch is identical to `origin/<default>` (zero commits either
   side). Uncommitted cleanup or unsynced default branch → stop, report,
   owner decides.
2. **CI green on the default branch** — the latest run on the default
   branch reports success.
3. **Issue reconciliation** — every issue fixed by commits since the last
   tag is closed (or label-swapped) with an evidence comment; remaining
   open issues are accurately labeled. A commit claiming `(#N)` with the
   issue still open is an anomaly to resolve here, not at publication.
4. **TODO.md clean** — the release-target section is fully resolved;
   completed items are removed (git history is the record); the backlog
   reflects reality.
5. **PLAN.md clean** — `## Unsorted MBIs` and `## Active MBI` empty or
   accurately reflecting state.

### R1 — Content & documentation sync (before Gate 1)

All shipped artifacts must describe the release, verified against the code —
not assumed current:

| Artifact | Verification |
|----------|--------------|
| `docs/` (readthedocs) | builds cleanly (`make docs`); content matches current behavior |
| `demos/` | regenerated (`make demos`); **presented to the owner for visual check** — owner touchpoint, proceed on approval |
| `examples/` | run/verify against the current API; update where broken |
| `README.md` | current; absolute image paths (extended by the pre-upload check in R6) |
| `PACKAGE.md` | regenerated (pkgq skill: analyze/update) |
| `AGENTS.md` | matches current code (module tree, conventions); de-duplicated against the global instructions |
| `CHANGELOG.md` | complete for the release (Added / Fixed / Changed extracted from commits since the last tag) |

**Functional-analysis consolidation (every release).** Merge every
`analysis/*.md` newer than the last consolidation into
`analysis/functional.md` — the single authoritative functional picture —
then the merged documents are removed from `analysis/` (their content lives
on in `functional.md`; git history is the archive). New `research/`
documents are consolidated into the functional analysis the same way and
**deleted after consolidation** — research is transient working material;
never delete without consolidating first. For a first full run over a large
legacy corpus, this step may be scheduled separately (owner decision) — but
every release afterwards consolidates only what is new.

### R2 — Determine the bump

Read `version` from `pyproject.toml`; list commits since the last tag via
the `git` tool (`git(operation="log", args={ref: "vX.Y.Z..HEAD", oneline:
true})`). Decision rules: `feat:` present → minor; only `fix:` → patch;
breaking API → major; unclear → ask (that IS gate 1 if no version
decision was given).

### R3 — Update version artifacts

- `pyproject.toml` `version`
- any `__version__` in `src/**/__init__.py`
- `CHANGELOG.md` release section (Added / Fixed / Changed), extracted
  from commits since the last tag
- Verify sync: both locations match exactly; `uv.lock` self-updates.

### R4 — Pre-publish checks (local)

`make(operation="check")` — the standard all-gate (covers test, lint,
typecheck; env setup is handled by the target itself; `check-all` when
multiple Python versions matter). All green before committing. Fix
failures, don't route around them.

### R5 — Commit and push

Version files + changelog in one commit:
`chore: bump version to X.Y.Z` (attribution line per `c3:commit`), push;

### R6 — CI wait (authoritative)

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

### R6b — Build and verify the package

Remove `dist/` via the `file` tool (`operation="delete"`, recursive);
build via `make(operation="build")` — the standard target wraps
`uv build`. Verify before any upload: wheel contents show real source
files (not just `.dist-info/`), correct structure, no local paths. Empty
wheel → fix hatch `packages`
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

### R7a — Tag and GitHub release

After CI green: annotated tag `vX.Y.Z` pushed; GitHub release via
`github_tool release_create` with notes extracted from the changelog
(Summary, Changes, Installation). The tag push is not itself release
gated beyond CI green — the owner's version decision (gate 1) already
covered it.

### R7b — PyPI upload — after gate 2

`make(operation="publish")` — the full pipeline (**all** pre-publish
checks included). The granular retry path is the existing per-target
recipe below; never re-run the full pipeline just to retry an upload.

**If upload fails (e.g. HTTP 400):**
1. Check PyPI first — the upload may have partially succeeded (one file
   in, one rejected). Verify on pypi.org before retrying.
2. Retry the upload only, never the full publish pipeline: if the
   project defines a granular upload target, use
   `make(operation="<target>")`; **otherwise report to the owner to run
   `uv run twine upload dist/*` — do not invent a Makefile target.**
3. Max 3 retries, then stop and ask the owner.

**Verify publication:** `webfetch` the PyPI project page
(`https://pypi.org/project/<name>/`) and confirm the new version
appears; a test install is the owner's terminal call:
`uv pip install package==X.Y.Z`.

### R8 — Ecosystem sync (after publication verified)

The release is only done when everything that depends on it is in sync.
Consult the project's AGENTS.md / release runbook for its satellite list
(projects that consume the published package, project website, announcement
channel):

1. **Satellite/consumer projects** — for each: upgrade to the new version,
   run their checks/tests. Still working → record the evidence (version,
   check result). Broken → open an update task/issue in that project with
   what broke; the owner decides scheduling. Do not silently leave a
   consumer broken.
2. **Project website** — version references and feature mentions updated.
3. **Release announcement post** — a draft post exists (or is created) on
   the website: blog-voice, fun but informative, with examples of the most
   user-impacting/visible changes. Update the existing draft with this
   release's highlights; **present it to the owner for review** — owner
   touchpoint; publishing is the owner's call.

### R9 — First full functional-analysis consolidation (one-time, scheduled)

If `analysis/` still holds a legacy corpus never consolidated into
`analysis/functional.md` (skipped in R1 by owner decision): run the full
consolidation as a dedicated backlog task after the release, then the
per-release consolidation in R1 stays lightweight forever after.

# Deliverables

- Readiness audit evidence (clean tree, CI green, issues reconciled,
  TODO/PLAN clean)
- Synced documentation set (docs, demos, examples, README, PACKAGE.md,
  AGENTS.md, changelog) + consolidated functional analysis
- Bumped, tagged, GitHub-released, and published package; verification
  evidence (CI run, wheel listing, PyPI page) reported in one block
- Ecosystem sync evidence: satellite projects verified or flagged with
  update tasks, website updated, announcement draft posted for owner review

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
- Delete `analysis/` or `research/` documents without consolidating their
  content first (git history is the archive, consolidation is the record).
- Leave a satellite project silently broken after a release — flag it.

## Common failures

| Issue | Action |
|-------|--------|
| CI fails after push | Fix, commit, push, wait again |
| Empty wheel (module not found after install) | Fix hatch `packages` config (see R6b), rebuild |
| Version already on PyPI | Cannot overwrite — bump the version |
| Upload HTTP 400 | May have partially succeeded — check pypi.org before retrying; retry upload-only; max 3 attempts |
| Upload fails with "Invalid URL" | `[tool.uv.sources]` / `[tool.uv.workspace]` still present — remove them |
| Broken images on PyPI page | README uses relative image paths — switch to `raw.githubusercontent.com` URLs |
| Issue fixed by a commit but still open | Reconcile in R0 — close with evidence comment before proceeding |