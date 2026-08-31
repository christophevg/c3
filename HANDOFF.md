# C3 Overhaul — Session Handoff

*Written 2026-08-31 for a fresh session of the default agent continuing the
C3 overhaul (restart due to context size). Read this file first, then
BLUEPRINT.md (§7 decision log is authoritative — 37 entries), then
`git log --oneline -12`. This file replaces the previous HANDOFF entirely;
it is current as of commit `f735da6`.*

## Mission (from MISSION.md — owner's brief)

Full overhaul of C3 (agents + skills for the Yoker harness, ported from
Claude Code): consistency, cleanup, docs, backlog — done **interactively,
in small approved steps**, with BLUEPRINT.md as the shared foundation.
Yoker = Python-first harness (no Bash tool, no MCP, no sub-agent
hierarchy); C3 is Yoker-only. Owner = Christophe. Working style: proposals
before action, owner answers precisely and reads every diff.

## Where we are (validator: 13/13 agents, 20/9+ skills strict, 0 errors)

| Phase | Status |
|---|---|
| Blueprint, inventory, pilot, Batch A (+2 dogfood rounds) | ✅ done |
| Batch B — validator + 10 skills + c3:release + deletion pass | ✅ `961481f`, `44108cd`, `4e8d23b`, `437895b` |
| **Batch C — all 13 agent personas** | ✅ complete (`d8bd4a8` C1, `98f4ffb` C2, `ca86606` C3, `14eb341` C4) |
| PM orchestration-restoration fix (dogfood regression) | ✅ `1b85a5a` — see below |
| Edit/Deletion Discipline in AGENTS.global.md | ✅ `4a22c5b`, `f735da6` |
| **Batch D (knowledge skills `type:` pass, ~15 skills)** | **NEXT** |
| Batch E (root & docs) | queued |
| `backup-pre-batch-A/` deletion | **awaiting owner decision** |

## Standing rules — read these first

1. **Propose before applying any definition change.** Analyze → present →
   owner approves → write. Decision log records approved decisions only.
2. **Never delete knowledge — relocate it**, verify it landed (search the
   destination per item), then remove the source. Deletion only via owner
   decision on an exact list.
3. **Audit each batch before presenting** (old-vs-new disposition tables;
   owner vetoed nothing silently).
4. **BLUEPRINT log: append-only** (`append` operation, never
   replace-as-append — three clobber incidents taught this). Verify entry
   count after every log write (currently **37**).
5. **Agent = persona + agent-interactions; skill = workflow** (decision
   #36). Orchestration doctrine (delegation maps, engagement modes,
   cross-agent rules) lives in personas; procedures live in skills.
6. **TODO.md has exactly one maintainer: functional-analyst** (#35).
   Everyone else reports changes to their caller; PM delegates to FA;
   direct engagement = owner's responsibility.
7. Edit Discipline (AGENTS.global.md, `f735da6`): **one write-call per
   message per file** (fresh read between same-file edits — the hard
   rule); append via `append`/`insert`, never replace-as-append; anchors
   >3 lines → line-based insert or whole-file rewrite; two-strike rule
   covers repairs (restart from fresh read, never chain); verification
   patterns themselves must be verified.

## Current state facts (verified this session)

- `make validate`: **13/13 agents, 0 errors**. All 13 personas strict:
  api-architect, bug-fixer, business-analyst, code-reviewer,
  end-user-documenter, functional-analyst, project-manager,
  python-developer, release-manager, researcher, security-engineer,
  testing-engineer, ui-ux-designer. 20 skills have `type:` frontmatter
  (all workflow-class migrated); ~15 knowledge skills await Batch D.
- Branch `yoker`; local-only commits (two-mode model; no GitHub from C3
  sessions without explicit owner request).
- Project-manager persona recently restored to **team orchestrator**
  (commit `1b85a5a`): delegation map (12 agents × mode), lifecycle rules,
  post-and-poll atomic, Simplicity Gate, testability check,
  **session = managed mode** routing (any project ask → Phase 0; PM never
  executes git/make directly even outside the playbook — delegate or
  report). `c3:project-manage`: Phase 0 unconditional + post-and-poll
  recipe block. This came from a real dogfood regression (PM ran project
  work solo) — root-caused to Batch A stripping orchestration doctrine
  from the persona (git archaeology vs pilot `114fc9c`).
- Yoker issues **#62–#65** filed (editing ergonomics: #62 diff-out
  response — owner's idea; #63 ambiguous anchor must error + `occurrence:`
  selector (bug class — silent line-drop / repo corruption); #64 `write`
  overwrite flag; #65 anchored `insert_after`). Earlier: #56–#61. Owner
  declined B7/B9 ideas earlier.

## Locked-in specifics (do not re-derive)

- Release workflow: two owner gates (version; final pre-PyPI). CI green
  strictly precedes ready-for-review. Poll via `workflow_list` (never
  `workflow_view` — overflow, #56). State report is read-only (no pull).
- bug-fixer: authorized brief IS approval (A2); exact-failing-gate
  verification (A1); agents never propose Makefile targets (A3); filter
  cookbook in release-manager persona + c3:release (A5).
- TODO.md canonical: `## Unsorted` → `## Backlog` P1–P4, **no `## Done`**
  (completed tasks removed; git + REQUIREMENTS.md hold the record).
- Attribution: "🤖 Implemented together with Yoker." (commits; PRs
  optional; never in comments). Agent `color` values are free-form rich
  colors (validator checks presence only — #35).
- `business-analyst` stays (owner trials it). `api2mod`/`spec2mod`
  deleted. `yoker.toml` C3-local (`issue_create` allowed).
- github tool has **no issue comment/edit/close** — documented limitation
  in c3:github + website-manage (FA composes, caller posts).

## Batch D — next (light)

~15 knowledge skills need: `type: knowledge` frontmatter, trigger-surface
check, link hygiene, then validator promotion (KNOWN_YOKER in
`bin/validate.py` grows per file). Candidates (verified by `^name:` search):
python, python-project, python-testing, pymongo, baseweb, readme,
documentation, textual, vue, vuetify-v1..v4, vue-form-generator, naming,
ollama, wsjf, plan, transcribe-session, api-design (verify),
analysis-integration. Note vuetify ×4 merge review is owner-deferred until
real use — do not merge in this batch. `naming` + `markdown-to-pdf`
dispositions are owner questions — ask, don't decide.

## Batch E — root & docs (after D)

- AGENTS.md condensed (pointer + two-mode model); README skill table
  regenerated from frontmatter (stale pypi/release rows); CHANGELOG;
  CONTRIBUTING.
- TODO.md restructured to canonical model.
- Gated deletions, each with its own approval: `HANDOFF.md` (after the
  restart renders it obsolete), `MISSION.md`, `log.txt` — never swept.
- HANDOFF.md staleness note: this rewrite fixes the stale phase table and
  commit list (was: "Batch C NEXT" + old commit hashes).

## Gated deletion — awaiting owner

`backup-pre-batch-A/` — 13 untracked files (pre-Batch-A safety copies).
Superseded by git history (pilot/batch-A states retrievable via `git show`
from `fb31a36`/earlier). Deletion is disk-only + irreversible → owner
explicitly decides: "delete it" or "keep + gitignore". Do NOT `git add
--all` around it (explicit staging only — see near-miss in B-2).

## Dogfood & deferred (owner-tracked)

- **Dogfood round 3** wanted: real project restart with full transcript →
  feedback loop. Validates the PM orchestration fix (`1b85a5a`) in
  particular — a casually-phrased PM-session ask must trigger Phase 0 via
  release-manager, not solo action.
- c3:release + release-manager recipe split needs one real release to
  validate.
- Deferred: markdown-to-pdf tool-vs-skill, PR-feedback roundtrip (TODO
  P2), memory system, vuetify merge review post-real-use.
- Upstream: #57–#61, #62–#65 with the Yoker team; C3-side re-validation
  when tools land (diff-out would retire several manual verification
  rounds).

## Session mechanics

- Whole-file rewrites: `write` refuses overwrite → delete + write; verify
  with a read; `make validate` after each write batch (0 errors expected).
- Commit checkpoints per phase (direct mode, c3:commit conventions);
  explicit staging only — never `git add --all` (Deletion Discipline #5).
- The owner answers precisely — one question at a time, proposals before
  action, and he reads every diff. That's the working style. Don't bulk.