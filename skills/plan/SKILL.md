---
name: plan
description: |
  Manage PLAN.md (Intake Backlog with Minimal Business Increments). Use when user asks about MBIs, wants to create/analyze/score MBIs, or says "/plan". Examples: "/plan", "analyze MBI", "create MBI", "score MBIs with WSJF".
---

# Plan Management

Manage PLAN.md files containing the Intake Backlog with Minimal Business Increments (MBIs).

## When to Use

Use this skill when the user asks to manage PLAN.md — creating, analyzing, or WSJF-scoring Minimal Business Increments (MBIs), or says `/plan`.

## Usage

```
/plan
/plan analyze
/plan create <mbi-name>
```

## Purpose

This skill manages PLAN.md files and MBI workflows:
- Creating and analyzing MBIs
- WSJF prioritization scoring
- Moving MBIs between states (Unsorted → Backlog → Active → Done)
- Scheduling MBI tasks in TODO.md

## What is an MBI?

An MBI (Minimal Business Increment) is the smallest piece of value that can be delivered to end-users. It describes what users can do after a release that they couldn't do before.

**MBI Criteria:**
- Provides end-user value (not just internal refactoring)
- Delivers complete functionality (not partial)
- Can be independently released
- Has clear acceptance criteria

**NOT an MBI:**
- Internal refactoring without user-facing changes
- Technical debt cleanup
- Architecture improvements without new capabilities

## PLAN.md Structure

```markdown
# Plan

## Unsorted MBIs

- [ ] [Raw MBI idea - needs analysis]

## Active MBI

### MBI-XXX: [Name]

**Goal:** [What users can do]

**Value:** [Why this matters]

**Status:** [In Progress | Ready | Blocked]

**Components:**
- [ ] DEV: [Implementation task]
- [ ] TEST: [Testing task]
- [ ] DOCS: [Documentation task]

**Tasks:**
- [ ] [TASK-ID from TODO.md]

**Acceptance Criteria:**
- [ ] [Measurable criterion]

**Dependencies:** [None | List blocking MBIs]

---

## Backlog

### MBI-XXX: [Name]

**Goal:** [Brief description]
**Value:** [Brief value statement]
**Status:** [Ready | Blocked]

---

## Done

### MBI-XXX: [Name] (Completed: YYYY-MM-DD)

**Goal:** [What was delivered]
**Value:** [Value realized]
```

## MBI Workflow

### Creating a New MBI

1. **Identify Value**: What can users do after this release?
2. **Define Goal**: Clear, user-focused capability statement
3. **List Components**: DEV, TEST, DOCS, OPS tasks
4. **Set Acceptance Criteria**: Measurable conditions for completion
5. **Check Dependencies**: What must be completed first?

### MBI Lifecycle

```
Unsorted → Backlog → Active → Done
              ↑         ↑
         (analyzed)  (pulled)
```

### MBI States

| State | Meaning | Location |
|-------|---------|----------|
| **Unsorted** | Raw idea, needs analysis | Unsorted MBIs section |
| **Backlog** | Analyzed, ready to schedule | Backlog section |
| **Active** | Currently being implemented | Active MBI section (only one) |
| **Done** | Completed and delivered | Done section |

### Task Scheduling

When an MBI becomes **Active**:
1. Mark tasks in TODO.md with `[MBI-XXX]` prefix
2. Move MBI tasks to top of TODO.md (above other tasks)
3. Non-MBI tasks remain in original order below MBI tasks

## Behavior

### Step 1: Find PLAN.md

Look for PLAN.md in:
1. Current directory
2. Parent directories (up to 3 levels)

If not found, ask user if they want to create one from template.

### Step 2: Read Current State

Parse PLAN.md and identify:
- Unsorted MBIs (need analysis)
- Active MBI (if any)
- Backlog MBIs (ordered by priority)
- Done MBIs

### Step 3: Determine Action

Based on current state and user request:

| Command | Action |
|---------|--------|
| `/plan` | Show current state, propose next action |
| `/plan analyze` | Process unsorted MBIs |
| `/plan create <name>` | Create new MBI from description |
| `/plan activate <id>` | Move MBI from Backlog to Active |
| `/plan complete <id>` | Move MBI from Active to Done |
| `/wsjf` | Interactive WSJF scoring |

### Step 4: Analyze Unsorted MBI

For each unsorted MBI:

1. **Ask about scope:**
   ```
   Ask the user:
   
   Question: "I found '{mbi_name}' in Unsorted MBIs. Would you like to analyze it now, or leave it for later?"
   
   Options:
   - "Analyze now" — Gather Goal, Value, Components, Acceptance Criteria
   - "Leave for later" — Keep in Unsorted MBIs
   - "Delete" — Remove from Unsorted MBIs
   ```

2. **If analyzing, gather:**
   - Name: Short identifier
   - Goal: What users can do after release
   - Value: Why this matters
   - Components: DEV, TEST, DOCS tasks
   - Acceptance Criteria: Measurable conditions
   - Dependencies: Blocking MBIs or external dependencies

3. **Ask about activation:**
   ```
   Question: "Should this MBI be active immediately, or added to the backlog?"
   
   Options:
   - "Active now" — Move to Active MBI, schedule tasks in TODO.md
   - "Backlog" — Add to Backlog section for later
   ```

4. **Update PLAN.md:**
   - Move from Unsorted to Backlog or Active
   - Mark tasks in TODO.md if Active

### Step 5: Create New MBI

When creating a new MBI from user description:

1. **Ask if MBI or linear task:**
   ```
   Question: "Is this an MBI (delivers user-facing value) or a linear task (internal improvement)?"
   
   Options:
   - "MBI — Delivers user value"
   - "Linear task — Internal improvement"
   ```

2. **If MBI, ask about capture:**
   ```
   Question: "Would you like to analyze this MBI now, or just capture it for later?"
   
   Options:
   - "Analyze now" — Gather Goal, Value, Components, Acceptance Criteria
   - "Just capture" — Add to Unsorted MBIs
   ```

3. **If Just Capture:**
   - Add to Unsorted MBIs in PLAN.md
   - Confirm to user

4. **If Analyze Now:**
   - Gather all MBI information
   - Ask if Active or Backlog
   - Update PLAN.md accordingly

### Step 6: Activate MBI

When moving MBI from Backlog to Active:

1. Verify only one Active MBI exists (move previous to Done if needed)
2. Update status to "In Progress"
3. Mark tasks in TODO.md with `[MBI-XXX]` prefix
4. Move MBI tasks to top of TODO.md
5. Confirm to user

### Step 7: Complete MBI

When marking MBI as Done:

1. Move from Active to Done section
2. Record completion date
3. Remove `[MBI-XXX]` prefixes from TODO.md (or mark tasks as done)
4. Confirm to user

## WSJF Scoring

Use `/wsjf` skill for interactive WSJF prioritization:

```
WSJF = (Business Value + Time Criticality + Risk Reduction) / Job Size
```

Higher scores indicate higher priority. See `c3/skills/wsjf/SKILL.md` for details.

## File Locations

| File | Purpose |
|------|---------|
| `PLAN.md` | Project-level MBI tracking |
| `TODO.md` | Task-level backlog |
| `c3/skills/plan/SKILL.md` | This skill definition — includes the PLAN.md template |

## Integration with Other Skills

| Skill | Relationship |
|-------|--------------|
| `/project-feature` | Can create MBIs via MBI workflow |
| `/project-manage` | Checks for Active MBI and prioritizes its tasks |
| `/wsjf` | Interactive prioritization scoring |
| `functional-analyst` | Analyzes and scopes MBIs |

## Examples

### Example 1: Show Current State

```
User: /plan

Agent: I found PLAN.md with:

**Active MBI:** MBI-001 - Package Plugin System (In Progress)

**Backlog:** None

**Unsorted MBIs:** 1
- Bootstrap & Python API

**Next Actions:**
- Continue MBI-001 (UI Separation Phase 2)
- Analyze unsorted MBI: Bootstrap & Python API

What would you like to do?
```

### Example 2: Analyze Unsorted MBI

```
User: /plan analyze

Agent: Found 1 unsorted MBI: "Bootstrap & Python API"

Would you like to analyze it now?

User: Yes

Agent: Let me gather the information...

What can users do after the Bootstrap & Python API release?
[... interactive interview ...]

Should this MBI be active immediately or added to the backlog?
```

### Example 3: Create New MBI

```
User: /plan create "Analytics Dashboard"

Agent: Is this an MBI (delivers user-facing value) or a linear task?

User: MBI

Agent: Would you like to analyze it now, or just capture it?

User: Just capture

Agent: Added to Unsorted MBIs in PLAN.md.
```

## Notes

- Only one Active MBI at a time (focus principle)
- Unsorted MBIs are raw ideas — functional-analyst processes them
- Active MBI tasks are prioritized at top of TODO.md
- WSJF scoring is optional but recommended for backlog prioritization
