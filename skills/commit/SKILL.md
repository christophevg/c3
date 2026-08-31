---
name: commit
description: Guide git commit operations with atomic commits and conventional format. Use when committing changes, creating commits, or when user says "/commit", "commit these changes", "create a commit". Analyzes changes, groups by functionality, detects sensitive files, and waits for user verification.
type: workflow
---

# Commit

Guide git commit operations with atomic commits, functionality-based grouping,
and conventional commit format.

## When

- The user wants to commit changes, says `/commit`, "commit these changes",
  or "create a commit".
- Multiple changes need grouping analysis into atomic commits.

## Inputs

- A working tree with changes to commit (staged or unstaged).
- Mode: direct (local commits on the working branch) or managed (feature
  branch within the `project-manage` workflow).

# Procedure

1. **Gather context** — `git(operation="status", args={porcelain: true})`
   for the change set, `git(operation="diff")` for unstaged edits,
   `git(operation="log", args={oneline: true, n: 10})` for the repository's
   message style.
2. **Screen for sensitive files.** Block: `.env*`, `*.pem`, `*.key`,
   `secrets.*`, `credentials.*`. On detection: name the file, block the
   commit, suggest `git(operation="rm", args={cached: true, files: [...]})`
   and a `.gitignore` entry.
3. **Group atomically.** One logical change per commit — file type
   (backend / frontend / tests / docs), directory, and change type
   (`feat`, `fix`, `refactor`, `perf`, `test`, `docs`, `style`, `chore`).
   Atomic test: the message must be describable without "and".
   Multi-concern files: propose separate commits; if intertwined, one
   commit with a detailed body.
4. **Check repository style.** Follow the conventions of the last ten
   commits (types in use, scopes, language).
5. **Validate pre-conditions**, in order:
   a. Changes staged — the `git` tool's `commit` does not stage; stage
      explicitly with `git(operation="add", args={files: [...]})` and
      verify with `git(operation="status", args={porcelain: true})`.
      Committing with nothing staged fails on "no changes added" — that is
      a staging miss, not a message problem.
   2. Sensitive files absent.
   3. Trailing newlines present on edited files.
   4. Python projects formatted (`ruff format` via the project's make
      targets; the agent runs the project's own gate, never invents new
      Makefile targets).
6. **Present the analysis** — groupings, sensitive-file warnings, proposed
   messages — and wait for the owner's confirmation. In direct mode the
   confirmation is plain chat; in managed mode it is PR feedback. Never
   mix. Validation of tests/lint/types is the caller's gate, not this
   skill's.
7. **Create the commit** with a multi-line message argument:
   `git(operation="commit", args={message: "type(scope): summary\n\nbody\n\n🤖
   Implemented together with Yoker."})` — multi-line messages pass as one
   argument. Pre-conditions verified in step 3.
8. **Verify.** `git(operation="status")` clean &&
   `git(operation="show", args={format: "%B"})` shows the message with the
   attribution line. On missing attribution: `git commit --amend` to add it,
   then re-verify. Report the hash; push only on explicit request.

## Commit message rules

Format: `type(scope): description` + blank line + optional body +
attribution.

- Every commit ends with: `🤖 Implemented together with Yoker.`
- Core types: `feat fix refactor perf test docs style chore`.
- Subject ≤ 50 chars, capitalized, imperative, no trailing period;
  body wrapped at 72 explaining what and why, never how; blank line
  between subject and body.
- Attribution is for commits only — never in PR/issue comments or bodies.

## Safety protocol

| Rule | Reason |
|------|--------|
| Never commit directly to master/main in managed mode | acceptance happens on PRs |
| Never update git config | preserves the owner's configuration |
| Never skip hooks (`--no-verify`, `--no-gpg-sign`) | hooks are safety |
| Amend only to add missing attribution | otherwise previous commit history is rewritten |
| Never force-push the default branch | protects shared history |
| Stage specific files, not `-A`/`.` | avoids sensitive files and binaries |
| Never create empty commits | state the problem instead |

Destructive operations (`push --force`, `reset --hard`, `checkout .`,
`restore .`, `clean -f`, `branch -D`) only when the owner explicitly
requests them. When hooks fail, fix and create a NEW commit — never amend
after hook failure (that would modify the previous commit).

## Project-management mode

When invoked from `c3:project-manage`:

1. Verify the current branch is a feature branch, never master/main
   (`git(operation="branch", args={show_current: true})`).
2. Commit to the feature branch; do not push — `c3:project-manage` handles
   push and PR creation.
3. Return control with the commit summary for PR creation.

# Deliverables

- Owner-verified, conventional-format commits with mandatory attribution.
- A short report: groupings, hashes, and any files left uncommitted with
  the reason.

## Related

- `patterns/atomic-commits.md`, `patterns/conventional-commits.md` —
  reference patterns bundled with this skill
- `c3:project-manage` — the managed-mode caller; commits land on feature
  branches, push/PR stay there
- `c3:release` — where commits feed the release workflow

## Never

- Commit without the owner's explicit verification of the changes.
- Commit to master/main in managed mode, skip hooks, or update git config.
- Auto-push after committing; push is a separate, confirmed step.
- Add the attribution line to PR or issue comments.