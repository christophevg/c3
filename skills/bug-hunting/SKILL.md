---
name: bug-hunting
description: |
  Systematic bug hunting workflow for finding edge cases and hidden bugs. Use after implementing features, before releases, or when asked to find bugs, probe for holes, or stress-test code. Examples: "hunt for edge cases", "what could go wrong", "stress-test config parsing".
type: workflow
---

# Bug Hunting

Systematic hunt for edge cases and hidden bugs before they reach
production. Verification tool between "implemented" and "released".

## Triggering

- "find bugs", "hunt for edge cases", "probe for holes", "what could go
  wrong", "stress-test X"
- after implementing a feature (verification hunting)
- before a release (pre-release hunting)

# Inputs

A codebase, module, or configuration surface to hunt in, plus context:
README, architecture docs, project conventions. Real project schemas beat
synthetic examples — validate against them in Phase 5.

## Hunting workflow

### Phase 1 — Understand the architecture

1. Review context: project conventions, README usage examples, design docs.
2. Map data flows: entry points → transformations → exits/stores;
   component boundaries.
3. Map critical paths: happy path, alternative valid paths, error paths,
   boundary paths.
4. Document assumptions: input contracts, implicit invariants, assumed
   dependencies.

### Phase 2 — Core bug identification

For each critical operation, trace what it assumes and what could go
wrong. Check error handling: exceptions caught, errors logged with context,
actionable messages, cleanup on failure. Challenge assumptions: None?
wrong type? empty? huge? unexpected structure? Probe boundaries: empty vs
None, single vs many, min/max, unicode vs ASCII, nested vs flat.

### Phase 3 — Test-driven fixing

Write the failing test BEFORE fixing — it passes only while the bug
exists, then flips to assert the fixed behavior and must stay green.
Minimal fix, no refactoring while fixing. Per-bug docs: title, severity,
reproduction, expected/actual, root cause, fix, test coverage. Gates:
`make test`, `make lint`, `make typecheck`.

Stub workflow with `c3:testing-engineer`: it creates failing test stubs →
read the stubs for intended behavior → implement → replace stubs with real
assertions → FAIL transitions to PASS.

### Phase 4 — Edge-case hunting

Categories, in hunting order: input boundaries (empty/None/single/max/
special chars/encodings) · configuration (missing keys, empty files, wrong
types, cycles, deep nesting, duplicate keys) · concurrency (races, TOCTOU,
deadlocks) · security (injection, traversal, privilege escalation,
resource exhaustion) · integration (missing deps, version mismatch,
network failure, timeouts, partial failure) · performance (large inputs,
deep nesting, concurrency, resource limits).

Generation techniques: equivalence partitioning, boundary-value analysis,
decision tables, state-transition testing, error guessing. Full catalogs
in `patterns/edge-case-categories.md`, techniques in
`patterns/advanced-techniques.md` (property-based testing, fuzzing,
mutation testing), severity guide in `patterns/bug-severity.md`.

### Phase 5 — Prioritize and fix

| Severity | Criteria | Action |
|----------|----------|--------|
| Critical | data loss, security hole, crash | fix immediately |
| High | feature broken, no workaround | fix before release |
| Medium | impaired, workaround exists | fix soon |
| Low | minor/cosmetic | document as known issue |

Fix order: severity first. Each bug gets the Phase-3 treatment (test
first), a regression test, and real-world validation against actual
project schemas / production-like data. Full gates green before reporting.

# Deliverables

- A bug report per finding (severity, reproduction, root cause, fix, tests)
  in the structure of Phase 5 — handed to the caller for triage/fixing.
- Fixed bugs land through `c3:bug-fixing`'s discipline (failing test first,
  exact-gate verification).

# Related

- `c3:bug-fixing` — the per-bug fix workflow this skill feeds
- `c3:testing-engineer` — test stubs and coverage collaboration
- `c3:security-engineer` — security-adjacent findings need its review

## Never

- Fix without a failing test first.
- Refactor while fixing; keep the change minimal.
- Claim verified without the project's full gates passing.