---
name: project-manage
description: |
  The managed-mode playbook: drive a project through the full workflow —
  state detection, analysis, task selection, design review, consensus,
  implementation, review, PR and CI — with GitHub as the communication
  channel to the owner. Use only on explicit invocation: a project-manager
  session start or an explicit owner request (handover from a direct
  session). Never triggers on conversational phrases.
type: workflow
---

# Managed Project Workflow

## Mode

Managed mode is one of the two operating modes (see BLUEPRINT §1.3). In
managed mode, GitHub is the communication channel to the owner: plans,
approvals, and review feedback happen in PR comments. The workflow proposes;
only the owner merges.

**Handover from a direct session.** When the owner explicitly invokes this
playbook from a direct session: acknowledge the mode change in one line
("Entering managed mode — communication moves to GitHub"), carry any
conversational decisions into the relevant artifact (TODO.md, analysis/),
then start at Phase 0. Phase 0 is state-driven and resumes from any point.

## Invocation Style

All engagements use Yoker's agent tool:

```
agent(agent_name="<role>", prompt="<task>", ephemeral=<true|false>)
```

- `ephemeral: true` — one-shot engagement, auto-released. Default for
  single-step requests (a state report, one commit sequence).
- `ephemeral: false` — ongoing collaboration via `send_message`; use when
  follow-up rounds are expected (polling, iterative fixes); release when done.

Skills are invoked with the skill tool: `skill(skill_name="c3:...")`.

### Post-and-poll recipes (procedure record)

Every PR interaction that expects an owner response is ONE release-manager
instruction that posts AND polls — never split into a post call plus a
user hand-off:

```
agent(agent_name="c3:release-manager",
      prompt="Post <content> as a comment on PR #{n}. Then poll for owner
             response — check PR comments and reviews every 60 seconds for
             up to 15 minutes. Report the owner's response or timeout.")
```

Applies to: implementation plans, revised plans, implementation questions,
mark-ready + review request, responses to review feedback — any comment
expecting a response. Never split post and poll into two calls; never
hand back to the owner with "say 'follow up on PR #N'" except after a
polling timeout (the push model is a timeout fallback only).

Anti-pattern (splits the atomic operation, strands the workflow):
posting the plan in one call, then reporting "I've posted the plan, say
'follow up' when ready".

## Phase 0 — Session Start & Triage

**Phase 0 is unconditional.** Whatever the owner's first request in this
session — however phrased ("manage this project", "investigate X",
"there's a bug", "what's the status") — any request concerning the project
routes through this phase first: state detection, then the ask. Starting a
session with the project-manager IS entering managed mode; the playbook
does not require magic words.

**0.1 Project state (release-manager, ephemeral).** Engage c3:release-manager
with "Report project state". Its report is the session's single source of
truth: working directory (the project root), project type, branch, uncommitted
changes, open PRs (with content classification and owner-direction timeline),
open issues, last tag, recent commits.

**0.2 State matrix.** From the report, pick the resume point:

| Finding | Action |
|---------|--------|
| Analysis-only PR, no approval | poll for plan approval (5.3) |
| Analysis-only PR, approved | go directly to implementation (5.4) |
| Analysis-only PR, changes requested | revise plan (5.2) |
| Implementation PR, no feedback, CI green | poll for review (5.10) |
| Implementation PR, CI red | fix CI |
| Implementation PR, changes requested | `c3:project-handle-pr` |
| Merged PR, still on feature branch | `c3:project-post-merge` |
| Clean default branch | next: open issues (0.3) or Phase 1 |
| Open issues without status labels | triage (0.3) |

Approval already present in PR comments is final: never re-post the plan,
never re-wait, never re-ask. Read the comment timeline and act.

**0.3 Issue triage.** Only issues without status labels are new.

| Type | Route |
|------|-------|
| Bug | Bug flow (below) — immediate, no confirmation ask |
| Feature | functional-analyst reviews; clarifies in issue comments; owner accepts → `status:backlog` + TODO.md entry |
| Question | researcher evaluates or close |
| Dependency | researcher → backlog |

Labels: `status:backlog` / `status:in-progress` / `status:needs-research` /
`status:wont-do` (closed with reason) / `status:blocked`. All labeling,
commenting, and closing go through c3:release-manager. Only the repository
owner's comments decide; verify ownership before treating feedback as
authoritative. Full protocol:
[references/issue-review-workflow.md](references/issue-review-workflow.md).
Commit TODO.md updates promptly (via release-manager) — never let triage
accumulate uncommitted changes. After issues, continue to Phase 1 or the
next item; do not pause for feedback.

---

## Phase 1 — Analysis (conditional)

| State | functional.md | TODO.md | Action |
|-------|---------------|---------|--------|
| New project | missing | missing | 1A |
| Unanalyzed backlog | exists | missing | 1B |
| Ready | exists | exists | Phase 2 |

**1A/1B — functional-analyst**: review project state (1B: existing
analysis first), interview the owner, (re)build `analysis/functional.md`
and a prioritized `TODO.md`. Create `PLAN.md` with MBIs via `c3:plan` when
the project benefits from MBI slicing — otherwise skip it.

A Ready project skips Phase 1 by design — the full interview-style analysis
runs only when artifacts are missing or the owner requests fresh analysis.
The functional-analyst's involvement then continues **per task** at Phases
2–4: preparing each task, guarding its functionality through design and
consensus, and reviewing the implementation (5.6). It is the most-engaged
agent in the workflow, not a one-time Phase 1 role.

**researcher, conditional:** only for identified gaps, tech choices, or on
owner request; findings in `research/`.

---

## Phase 2 — Task Selection

**2.1 Unsorted items** (TODO.md `## Unsorted`, PLAN.md `## Unsorted MBIs`):
ask — sort into backlog / analyze now / start next task.

**2.2 Priority:** 1) Active MBI tasks ([MBI-xxx] in TODO.md),
2) critical bugs, 3) linear backlog.

**2.3 Verify first (functional-analyst).** The functional-analyst confirms
the chosen task's acceptance criteria are not already satisfied by the
codebase and the task is still accurately described; if implemented or
stale, it updates TODO.md and the orchestrator moves to the next task.

**2.4 Propose next task to the owner in chat — do not pause.** State the
selection (task id, title, one-line why) as a report and continue
immediately into the workflow. The owner interjects when they want
 something different: "manage the project" IS the instruction to proceed
autonomously. On request, show all backlog items or run fresh analysis.

**2.5 Scope classification → design agents:**

| Scope | Domain agents |
|-------|---------------|
| backend | api-architect (+ security-engineer if security-adjacent) |
| frontend | ui-ux-designer |
| full | api-architect, ui-ux-designer (+ security-engineer) |
| docs | end-user-documenter |
| research | researcher |

Include security-engineer when the task touches auth, sensitive data,
external APIs, user input, files, or security-relevant configuration.

**2.6 Bundling (owner-directed).** Enumerate all incomplete tasks, propose
groupings (implementation vs docs; open-ended evaluations excluded), present
before proceeding. A bundle = one branch, one PR, one review cycle; the
implementation plan maps every task to its acceptance criteria.

---

## Phase 3 — Cross-Domain Design Review

Engage the scope's domain agents (Phase 2.5 table) **and the
functional-analyst** to review the task against the functional analysis.
The functional-analyst prepares the task for the domain agents: restates
the acceptance criteria, supplies the functional context from
`analysis/functional.md`, and frames the open functional questions. Domain
agents own their domain's design doctrine — api-architect alone applies
API/architecture principles (RESTful, simplicity, wrapper check); never
restate them here.

Each domain agent writes `analysis/<domain>-<topic>.md` and returns its
findings. The functional-analyst incorporates them into TODO.md (scope,
criteria, dependencies) and reports the integrated result.

## Phase 4 — Consensus

- Collect findings from all engaged agents (functional-analyst always
  included); coordinate resolution.
- Write `reporting/<task>/consensus.md`.
- Proceed only on consent of every engaged agent.

## Phase 5 — Implementation

**5.1 Branch + draft PR (release-manager).** Feature branch from the
default branch; commit analysis docs (skip gitignored paths — never force-add);
open a draft PR referencing the task/issue.

**5.2 Implementation plan as PR comment** (release-manager): approach,
files, steps, acceptance criteria — ending "Waiting for owner approval
before proceeding." When conversational decisions exist (handover, 2.6
bundles), the plan must explicitly incorporate them.

**5.3 Plan Approval Gate (blocking).** Poll via release-manager: check PR
comments every 60s, max 15 minutes, only newer comments count, non-owner
comments are informational.

| Outcome | Action |
|---------|--------|
| Approved | 5.4 |
| Changes requested | revise (functional-analyst) → re-post → poll again |
| Timeout | report PR URL + "Say 'follow up on PR #N' to check again", pause |

Implementation never starts without this approval in PR comments.

**5.4 Domain skills.** Invoke matching knowledge skills before coding
(`python` for anything Python; `textual`/`rich`/`pymongo`/`fire`/
`baseweb`/`vuetify` for their domains; `readme` + `documentation` for
docs-touching tasks). Their patterns are the implementation vocabulary.

**5.5 Implement** (python-developer or fitting specialist): follow the
approved plan and the domain skills; incremental — one change, verify,
next; `make check` green before reporting done.

**5.6 Review cycle.** Invoke `c3:project-review` (round 0, task, scope,
files). `approved` → 5.7 · `rejected: <feedback>` → back to 5.5 with the
consolidated feedback, round++ · `escalate` → owner decides.

**5.7 Mark pending-review + summary.** Update TODO.md (pending review, PR
ref); write `reporting/<task>/summary.md` (what, decisions, files, PR).
Workflow-local `reporting/` is never committed when gitignored.

**5.8 Push + PR + CI** (release-manager): commit (conventional format),
push, non-draft PR with task/issue references. Then CI until green:
developer fixes → release-manager re-pushes.

**Phased completion — CI gate before review request.** The PR lifecycle
is strictly ordered: 5.8 commit/push → CI green (fix-and-repush until it
passes) → and only then 5.9 (mark ready, request owner review) and any PR
comment announcing readiness. Never request review, mark ready, or post
completion comments while CI is red or unknown.

**5.9 Ready + request review** (release-manager): mark ready, request the
owner's review, comment "Ready for review."

**5.10 Poll for review** (release-manager): owner approves → wait for the
merge; PR state MERGED (owner merged/rebased directly) → treat as positive
response and go to `c3:project-post-merge`; changes requested →
`c3:project-handle-pr`; timeout (15 min) → report + pause
("follow up on PR #N" resumes).

---

## Bug Flow

Bugs skip the Plan Approval Gate (owner-reported, urgent); everything else
funnels identically:

1. Branch + `status:in-progress` label (release-manager)
2. c3:bug-fixer (ephemeral): diagnose → test first → fix → `make check`; reports diagnosis + files
3. `c3:project-review` scoped to the fix
4. Commit (`fix: ... (#N)`), push, PR, CI (release-manager)
5. Mark ready, request owner review, poll (5.9–5.10)

Feature issues and dependency upgrades:
- Feature issue → Phase 0.3 route → backlog (no immediate build).
- Dependency: researcher first; simple upgrade → developer; goal-bearing
  upgrade → functional-analyst.

## Sub-skills

| Trigger | Sub-skill | Purpose |
|---------|-----------|---------|
| "follow up on PR #N" | `c3:project-handle-pr` | feedback round, review re-entry, push |
| owner reports merge | `c3:project-post-merge` | default-branch cleanup (switch/pull BEFORE any TODO.md edit), then return here for the next task |
| during 5.6 / 6.4 | `c3:project-review` | shared review cycle, `make check` gate, escalation |

## Release

On owner request, delegate to release-manager → `c3:release`
(version decision, changelog, checks, build, tag, GitHub release, PyPI).

## Conventions

Artifacts: `TODO.md`, `PLAN.md`, `analysis/`, `research/`;
`reporting/` is workflow-local and uncommitted when gitignored.
TODO.md structure is canonical (BLUEPRINT §1.4): `## Unsorted` →
`## Backlog` (P1–P4). Completed tasks are removed — git history is the record — all project-* skills use this.

## After Each Task / PR

Process the next item without re-checking feedback on processed ones
(new issues; PRs awaiting feedback). When nothing is pending, report a
summary and pause; "follow up" resumes.