# C3 Blueprint

**Normative reference** for all C3 agent and skill definitions.
Created 2026-08-31 · Status: approved by owner · Governs the C3 overhaul (see `MISSION.md`) and all future definition work. Enforced mechanically by `bin/validate.py` (to be extended, §6).

## 1 — The Model

### 1.1 Precedence

Conflicts resolve top-down. A rule lives at exactly one layer — the highest layer that owns it:

1. Owner's live instruction
2. `AGENTS.global.md`
3. Project `AGENTS.md`
4. Agent persona (`agents/*.md`)
5. Skill workflow (`skills/*/SKILL.md`)

### 1.2 Owner authority

The owner is the only decision-maker. Agents propose; the owner approves. Only the owner merges PRs and approves gates.

### 1.3 The two modes

| | **Direct** (default) | **Managed** (opt-in) |
|---|---|---|
| Communication | one-to-one chat | GitHub (PRs, issues, comments) |
| Committing | local only, working branch | feature branch → PR → owner merges |
| Gates | owner approval in chat | owner approval in PR comments |
| Workflow | none prescribed | `project-manage` playbook |

**Entry:** direct = every default session. Managed = launching a `project-manager` session, or an explicit request in a direct session (e.g. `/project`), which hands the session over to the `project-manage` playbook.

**Mode rules:**

1. **No cross-triggering.** Workflow skills fire only on explicit invocation — never on conversational keywords.
2. **Mode is chosen by the owner only.** Agents never propose a mode, never question a mode choice, and never question an assignment in either mode.
3. **Direct mode never touches GitHub.** No PRs, issues, or comments. Managed mode routes all owner communication through GitHub exclusively.

**Handover:** on an explicit upgrade to managed, acknowledge the mode change, capture conversational decisions into the workflow entry artifact, and run `project-manage` Phase 0 — it is state-driven and resumes from any point.

### 1.4 Shared artifacts (mode-agnostic)

- `TODO.md` — prioritized backlog: `## Unsorted` → `## Backlog` (P1–P4). There is no `## Done` section: completed tasks are removed; git history and `reporting/` are the record.
- `PLAN.md` — optional MBIs, for larger projects (`c3:plan`)
- `analysis/` — functional, domain, security and bug analyses
- `reporting/` — workflow-local (consensus, plans, summaries); never committed when gitignored
- `research/` — research findings and recommendations

### 1.5 The team

No main-agent/sub-agent hierarchy. Agents are peers in a team, engaged by the owner or by each other:

- **Ephemeral** — one-shot engagement, auto-released after responding.
- **Persistent** — ongoing collaboration via `send_message`; release explicitly when no longer needed.

Parallel tool calls are supported syntactically but executed sequentially. Definitions never rely on, or promise, parallel execution.

### 1.6 Context hygiene

Delegate to a peer when performing a task yourself would fill your context with details you will never need again. Request summaries, not transcripts. Canonical case: `release-manager` owns all git/GitHub detail so an orchestrator's context stays clean. The principle — not any particular tool split — is the rule; it survives future dynamic context management.

### 1.7 Instruction style (the Flash rules)

GLM 5.3 adheres literally; imprecision becomes deadlock. Therefore:

1. Every rule exists exactly once, at its owning layer. No restatement in related definitions.
2. State positive intent ("do X"). No scar-tissue patches ("STOP: previous models did Y").
3. Only capabilities that exist in Yoker. Forbidden legacy vocabulary: `Bash`, `subagent_type`, `Task({})`, `CLAUDE.md`, `.claude`, MCP.
4. No implicit forks ("if in doubt X, otherwise Y") where a single behavior suffices.
5. Approval etiquette follows the mode: chat in direct, PR comments in managed. Never mixed.
6. Skill descriptions are the trigger surface: knowledge skills may auto-trigger on domain mention; workflow skills require explicit invocation.

## 2 — Agent Template

File: `agents/<name>.md` — frontmatter: `name`, `description` (when to engage; explicit and precise — this is the trigger surface for owner and peers), `color`, and `tools:` — with Yoker tool names only: per-agent grants ARE the static-permission model (base read set, write set, specialist tools, engagement/sleep as needed).

```markdown
---
name: <name>
description: <when to engage — explicit, precise>
color: <color>
tools:
  - <Yoker tool names only>
---

# Persona
Who I am. Three to five sentences. No procedure.

# Engaged when
By whom, with what input.

# How I work
The skills I invoke (procedures live THERE, not here).
The agents I engage, and why.

# I deliver
Outputs, reports, artifacts.

# I never
Few, absolute boundaries.
```

Persona stays brief and holds **zero procedure**. Discriminating instructions (choosing among workflows) appear only if the persona can run more than one workflow.

## 3 — Skill Template

File: `skills/<name>/SKILL.md` — frontmatter: `name`, `description` (trigger surface), `type: workflow|knowledge`.

**Workflow skills** — the actual procedures; invoked by an agent persona or explicitly by the owner. Never auto-trigger.

**Knowledge skills** — domain packs; may auto-trigger when their domain is touched. The only auto-triggering skills.

```markdown
---
name: <name>
description: <trigger surface — precision here IS trigger control>
type: workflow | knowledge
---

# When        — triggering conditions (respecting the class rules above)
# Inputs      — what is expected
# Procedure   — numbered, decisive steps
# Deliverables— outputs and artifacts
# Related     — skills/agents this connects to
```

**Base pattern:** agent = persona + minimal discriminating choice; skill = the actual workflow. Each rule in one place.

## 4 — Target Roster (working sketch — confirmed by inventory)

- **Agents (13):** all restated as personas per template. `project-manager` persona points to the `project-manage` playbook (one place defines managed behavior). `business-analyst` is **retained** (business-value pre-analysis feeding PLAN/TODO; owner will trial it, re-evaluate later).
- **Skills, three families:**
  - *Workflow:* `project*` suite, `plan`, `wsjf`, `github`, `commit`, `release`, `git-scripting`, `git-activity-report`, `bug-fixing`, `bug-hunting`, `pypi-publish`
  - *Knowledge:* `python*`, `baseweb`, `vue`, `vuetify` (merged from v1–v4), `textual`, `rich`, `fire`, `pymongo`, `ollama`, `quart-webapp`, `readme`, `documentation`, `naming`, `api-design` (restored reference pack from slimmed api-architect), `prepare-for-exam`, `markdown-to-pdf` (deferred — see decision log), `project-migrate`, `website-manage`
  - *Meta:* `develop-agent`, `develop-skill`, `lessons-learned`, `transcribe-session`
- **Doctrine relocation:** Wrapper Check, owner-proposal-default, simplicity gate move from `project-manage` into the design-review agents (api-architect, security-engineer), collapsed to their own voice.
- **Overlap resolution** (e.g. `bug-fixer` ↔ `bug-fixing`, `testing-engineer` ↔ `python-testing`): persona invokes the skill's procedure; decided per file at inventory sign-off.

## 5 — Execution Plan

1. ✅ This blueprint — agreed with owner
2. **Inventory** — every agent, skill, doc, script classified keep / rewrite / merge / delete → owner sign-off (`REPOSITORY-REVIEW.md` as inspiration, not truth)
2b. **Validation first** — extend `bin/validate.py` (§6) right after the pilot, so every migration batch is mechanically checked
3. **Pilot** — rewrite `project-manage`, `release-manager` + one domain agent against the blueprint → owner review
4. **Batch migration** — small approved batches; blueprint is the reference; definition changes are activatable by session restart (self-test)
5. **Docs & backlog** — README / CHANGELOG / CONTRIBUTING / `docs/` refreshed; `TODO.md` cleaned to the standard structure
6. **Dogfood** — external project runs the post-pilot definitions with full transcript; lessons flow back here

## 6 — Validation Tooling

Extend `bin/validate.py` to enforce this blueprint mechanically:

- All cross-references resolvable (skills ↔ agents ↔ docs)
- Forbidden vocabulary absent (§1.7.3)
- Required template sections present (§2, §3)
- Trigger-surface lint: workflow skills without keyword-only triggers; knowledge skills with precise domain triggers

## 7 — Decision Log

- 2026-08-31 — Two-mode model adopted (direct default, managed opt-in); both named in the instruction layer.
- 2026-08-31 — `release-manager` retained as git/GitHub delegate **for context hygiene**, not permissions; merge-back into the orchestrator deferred until Yoker gains dynamic context management.
- 2026-08-31 — Design doctrine moves out of orchestration skill into design-review agents.
- 2026-08-31 — `PLAN.md` (MBI) and `TODO.md` both remain, as optional and standard layer respectively.
- 2026-08-31 — `/project` upgrade path provided minimally: explicit invocation only, handover via state-driven Phase 0; no rich dispatcher router.
- 2026-08-31 — Direct mode commits locally only; zero GitHub interaction.
- 2026-08-31 — Agents never question assignments; mode and heft are the owner's call.
- 2026-08-31 — Infrastructure note: `Makefile` is C3-local; `Makefile.yoker` is symlinked as `~/.yoker/Makefile` and included by all project Makefiles.
- 2026-08-31 — Agent engagement vocabulary: ephemeral (one-shot) / persistent (ongoing) — no sub-agent hierarchy language.
- 2026-08-31 — Bugfix dogfood (release-log-3, 14 findings via researcher) → C3 fixes applied after owner approval: A1 exact-failing-gate verification (bug-fixing skill Phase 5.4); A2 engagement rule (authorized plan IS approval for one-shot agents; engagers choose persistent + send_message when approval loops are plausible — release-manager guidance + bug-fixer guardrail); A3 per-version testing: pointer to project make targets only (owner-driven Makefile growth; agents do NOT propose targets as a missing-Bash workaround — owner decision); A5 filter cookbook (pytest/collection/make/CI patterns + substring pitfalls + two-strikes rule) in release-manager persona, to be shared by c3:release; A4 authoritative-gate instruction deferred to c3:release rewrite (project actively fixing its local gate). Yoker tool findings B6–B14 queued as issues by owner decision.
- 2026-08-31 — F1–F6 approved and applied: F1 explicit-staging recipe + F3 CI-wait recipe → release-manager persona (F6 formalizes in c3:rewrite in Batch B); F2 commit-skill attribution template fix → Batch B; F4 (protected-path read prompts) and F5 (anchored post_filter) filed as Yoker issues #57/#58; F6 CI-wait cadence now also in persona. Release gates formalized: version decision + final pre-PyPI confirmation are the two standing owner gates.
- 2026-08-31 — Release gates formalized (owner decision after release dogfood): two standing owner gates in c3:release — (a) target version decision, (b) final confirmation before PyPI publish. Everything from changelog through GitHub release runs autonomously once the version is approved.
- 2026-08-31 — Release-readiness dogfood #2, part 1: clean run, workflow held (pr_list single-line-JSON lesson applied, no size errors; semver proposed at owner gate; self-flagged changelog anomaly). Fixes proposed-to-owner stage: (1) state-report strictly read-only (`pull` removed from recipe — sync is an explicit workflow step); (2) post_filter discipline recipe. Applied after owner approval. Yoker issues filed: #56 workflow_view payload, #57 read-only git ops on protected paths, #58 anchored post_filter vs decorated output.
- 2026-08-31 — TODO.md drops the `## Done` section: completed tasks are removed on completion; the merged PR, reporting/summary.md and git history are the record. All owning definitions updated.
- 2026-08-31 — Batch A audit with owner: stripped content was duplication except two items (project-status detection heuristics; todo-refine documentation-update ordering) — both restored in place. Verified relocated content landed: review tests in code-reviewer persona, MBI creation in c3:plan.
- 2026-08-31 — Functional-analyst clarified as the per-task functional guardian (most-engaged agent): verifies/prepares each task (2.3), supplies functional context in design review and integrates domain findings (3), sits in consensus (4), reviews implementation (5.6). Full Phase-1 analysis remains conditional on missing/stale artifacts only.
- 2026-08-31 — Task selection is autonomous (Phase 2.4): "manage the project" is the instruction to proceed; the selection is reported, not gated. Owner interjects to change course.
- 2026-08-31 — Full-workflow dogfood #1 (yoker-test): workflow followed correctly; fixes: (1) MERGED PR state = terminal polling signal (release-manager + playbook 5.10 + handle-pr 6.6); (2) CI green strictly precedes ready-for-review request (5.8 + persona I-never); (3) make-run flag-injection pitfall documented in release-manager. Enhancement deferred to TODO.md: PR-feedback roundtrip shortening.
- 2026-08-31 — Batch A completion audit with owner: stripped content was duplication except two items (project-status detection heuristics; todo-refine documentation-update ordering) — both restored in place. Verified relocated items landed: review tests in code-reviewer persona, MBI creation in c3:plan.
- 2026-08-31 (inventory round) — `business-analyst` retained: business-value pre-analysis feeding PLAN/TODO; re-evaluate after real-world use.
- 2026-08-31 — `api2mod` deleted outright (experimental, unused, phantom sub-skill); no salvage — `spec2mod` only drops cross-references to it.
- 2026-08-31 — `develop-agent` retained; rewritten blueprint-aware (drafts initial new agent definitions).
- 2026-08-31 — C3 is Yoker-only: all Claude Code support removed (tooling, docs, vocabulary); agent frontmatter `tools:` lists migrated to actual Yoker tool names.
- 2026-08-31 — Agent frontmatter keeps `color` + `tools:` (Yoker tool names only): per-agent grants ARE the static-permission model; base-read/write sets + specialist tools. Reverses the earlier "drop them as Claude-Code legacy" decision after owner review.
- 2026-08-31 — `spec2mod` deleted alongside `api2mod` (same paused experiment; both restorable from git history when the experiment resumes).
- 2026-08-31 — Duplicate-pattern skill refactors deferred to a later phase — notably markdown-to-pdf (Bash() reliance → future Yoker tool or shared Makefile target) and the root `scripts/` copies tied to it.
- 2026-08-31 — Polling is a real capability: sub-agents busy-wait via the `sleep` tool between GitHub checks (proven in live transcripts); release-manager keeps ~60s-interval polling in managed mode.
- 2026-08-31 — Design-doctrine consolidation to api-architect/security-engineer approved (explicit invocations stay covered because skills route design questions through those agents).
- 2026-08-31 — All `pkgq` references removed (tool retired).
- 2026-08-31 — All `memory/` references removed from agents/skills; valuable memory content incorporated into skills/backlog first; dedicated memory system deferred.
- 2026-08-31 — Reference material is relocated, never deleted: api-architect's encyclopedic API-design appendix became the `api-design` knowledge skill (persona loads it); observe usage before ever considering removal. This is the standing rule for all slimming: knowledge moves to a knowledge skill, redundancy moves to the one owning place — deletion only via owner decision. Verified against release-manager after owner challenge: operational recipes (PR-status gathering, PR creation, release API, date/attribution recipes, error table) belong IN the persona — they are its daily vocabulary. Slimming may remove scar tissue and duplication, never operative procedure or reference knowledge.
- 2026-08-31 — Validations: Makefile `version-*`/`release-*`/`tag` targets and `bin/version.py` are referenced by no agent/skill → delete in Batch B; publish path confirmed as release-manager → `c3:release` (pypi-publish referenced only as related material) → merge loses nothing.
- 2026-08-31 — B-1 validator built and green: global checks (forbidden vocabulary §1.7.3, duplicate headings with fenced-code stripping, cross-reference resolution for c3:/agents//skills/ paths) run on every definition file; strict blueprint template checks apply only to files in the KNOWN_YOKER promotion ledger (inverse of the proposed LEGACY_EXEMPT — self-maintaining, coverage line is the progress ledger). Related-section rule accepts Related/Reference/Sub-skills (verified against the Batch A suite). `make validate` at 0 errors / 0 warnings. Batch B deletions executed same commit (plugin-development, bin scripts, docs remnants, stray PLAN.md; Makefile version/release/tag targets); dangling PLAN.md-template references healed by pointing at the template inside c3:plan.
- 2026-08-31 — TODO.md has exactly one maintainer: the functional-analyst. Other agents (e.g. ui-ux-designer, code-reviewer) **report** needed backlog changes to their caller — a project-manager delegates them to the functional-analyst; when an agent is engaged directly by the owner, backlog follow-up is the owner's responsibility. Resolves the ui-ux-designer TODO-edit conflict found in the Batch C audit.
- 2026-08-31 — Agent frontmatter colors are free-form rich background colors (the restrictive Claude-Code palette list is retired); validator checks `color` presence, not values. `magenta3` and similar stay valid.
- 2026-08-31 — Live-test lesson (release-manager state report): github list operations return single-line JSON — post_filter cannot recover oversized responses; instructions must prescribe the narrowest query (`state="open"`, small `limit`, classify from list fields, `pr_view` only for depth). Standing recipe rule: **exact tool-call recipes belong in definitions for every repeated tool pattern; the payload model (what's big, what filters can/cannot do) is part of the recipe.** Yoker bug reported by owner: `repo_view` + `repo` param fails (`--repo` unknown flag in gh CLI).