---
name: project
description: |
  Handover entry to the managed project workflow. Explicit invocation only:
  "/project" from an interactive (direct) session, optionally followed by an
  intent. Never triggers on conversational phrases; the owner decides when
  to enter managed mode.
type: workflow
---

# Project — Mode Handover

Single purpose: hand a direct-mode session over to the managed workflow.
This skill does no work itself and contains no routing logic.

## Behavior

1. **Acknowledge the mode change** in one line: "Entering managed mode —
   communication moves to GitHub."
2. **Carry conversational decisions over** into the corresponding artifact:
   ideas discussed → TODO.md `## Unsorted`; agreed approaches → a task's
   notes; anything pending → named explicitly so nothing is lost.
3. **Invoke `c3:project-manage`.** Its Phase 0 is state-driven: the
   release-manager state report determines where the workflow resumes,
   regardless of how far the direct session got.

## Intent pass-through

If the owner's input names a specific target, pass it as context to
project-manage rather than routing elsewhere:

| Input mentions | Context passed |
|----------------|----------------|
| a PR number / "follow up on PR #N" | open `c3:project-handle-pr` — but ONLY after the project-manage Phase 0 state check confirmed the PR's state, so re-entry is safe |
| "PR #N was merged" | open `c3:project-post-merge` on the same condition |
| nothing specific | plain handover — plain Phase 0 |

An explicit PR reference still validates against the state report first:
sub-skills may only be entered after Phase 0 confirms their precondition
(e.g. the PR actually has changes requested). This keeps one state model.

## Related

- `project-manage` — the managed-mode playbook this handover enters
- BLUEPRINT §1.3 — the two-mode model defining when handover is allowed