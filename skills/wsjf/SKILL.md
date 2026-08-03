---
name: wsjf
description: |
  Interactive WSJF (Weighted Shortest Job First) scoring for MBI prioritization. Use when user wants to prioritize MBIs using economic decision-making. WSJF calculates priority based on Business Value, Time Criticality, Risk Reduction, and Job Size. Examples: "/wsjf", "score MBIs", "prioritize using WSJF".
---

# WSJF Scoring

Interactive WSJF (Weighted Shortest Job First) scoring for MBI prioritization. This skill facilitates relative scoring sessions to prioritize work based on economic factors.

## Usage

```
/wsjf
/wsjf <project-path>
```

## Purpose

WSJF is a prioritization method from SAFe that sequences work based on economic outcomes:

```
WSJF = Cost of Delay / Job Size
Cost of Delay = Business Value + Time Criticality + Risk Reduction/Opportunity Enablement
```

**Higher WSJF scores = Higher priority** (high value, time-critical work that's small in size)

## Workflow

```
/wsjf invoked
      │
      ▼
Find PLAN.md
      │
      ▼
Extract MBIs from PLAN.md
      │
      ▼
Establish reference item
(medium complexity)
      │
      ▼
For each MBI, ask user to score
relative to reference:
  - Business Value
  - Time Criticality
  - Risk Reduction
  - Job Size
      │
      ▼
Calculate WSJF for each MBI
      │
      ▼
Display results in table
      │
      ▼
Ask to update PLAN.md?
      │
   ┌──┴──┐
   Yes   No
   │     │
   ▼     ▼
Update Exit
PLAN.md
```

## Behavior

### Step 1: Find PLAN.md

Look for PLAN.md in:
1. Current directory
2. Parent directories (up to 3 levels)
3. User-specified path (if provided)

If not found, ask user if they want to create one from template.

### Step 2: Extract MBIs

Parse PLAN.md and extract all MBIs from:
- **Active MBI** section (if any)
- **Backlog** section

For each MBI, extract:
- MBI ID (e.g., MBI-001)
- Name/Goal
- Current status (if Active)

### Step 3: Establish Reference

Select a **reference item** for relative comparison:
- Preferably a medium-complexity MBI from the backlog
- If only one MBI exists, use it as reference with score of 3 (medium)

Tell the user:
> "I'll use **MBI-XXX: [Name]** as the reference item (medium complexity). All other MBIs will be scored relative to this one."

### Step 4: Interactive Scoring

For each MBI (except the reference), ask the user to score **relative to the reference**:

**Business Value**: "Compared to [reference MBI], this MBI's value to users/business is..."

| Score | Label |
|-------|-------|
| 1 | Much lower |
| 2 | Lower |
| 3 | Same |
| 5 | Higher |
| 8 | Much higher |
| 13 | Extremely higher |

**Time Criticality**: "Compared to [reference MBI], this MBI's urgency is..."

| Score | Label |
|-------|-------|
| 1 | Much lower |
| 2 | Lower |
| 3 | Same |
| 5 | Higher |
| 8 | Much higher |
| 13 | Extremely critical |

**Risk Reduction/Opportunity Enablement**: "Compared to [reference MBI], this MBI's ability to reduce risk or enable future opportunities is..."

| Score | Label |
|-------|-------|
| 1 | Much lower |
| 2 | Lower |
| 3 | Same |
| 5 | Higher |
| 8 | Much higher |
| 13 | Extremely high |

**Job Size**: "Compared to [reference MBI], this MBI's effort/complexity is..."

| Score | Label |
|-------|-------|
| 1 | Much smaller |
| 2 | Smaller |
| 3 | Same |
| 5 | Larger |
| 8 | Much larger |
| 13 | Extremely large |

**Note**: For Job Size, LOWER scores are better (smaller jobs get higher priority).

### Step 5: Calculate WSJF

For each MBI:

```
Cost of Delay = Business Value + Time Criticality + Risk Reduction
WSJF = Cost of Delay / Job Size
```

### Step 6: Display Results

Show results in a table, sorted by WSJF (highest first):

```markdown
## WSJF Scoring Results

| MBI | Name | BV | TC | RR | Size | CoD | WSJF | Priority |
|-----|------|----|----|----|------|-----|------|----------|
| MBI-002 | Analytics Dashboard | 8 | 5 | 3 | 5 | 16 | 3.2 | 1st |
| MBI-001 | Bootstrap & API | 5 | 8 | 5 | 8 | 18 | 2.25 | 2nd |
| MBI-003 | Reporting | 5 | 2 | 5 | 3 | 12 | 4.0 | 1st |

**Recommendation**: Order by WSJF: MBI-003 → MBI-002 → MBI-001
```

### Step 7: Ask to Update PLAN.md

> "Would you like me to reorder the MBIs in PLAN.md based on WSJF scores?"

| Option | Action |
|--------|--------|
| "Yes" | Update PLAN.md Backlog section with WSJF order, add WSJF score to each MBI |
| "No" | Display results only, exit |

If "Yes":
1. Read PLAN.md
2. Reorder MBIs in Backlog section by WSJF (highest first)
3. Add `**WSJF:** X.XX` line to each MBI
4. Write updated PLAN.md
5. Confirm to user

## WSJF Score Storage

When updating PLAN.md, add WSJF score to each MBI:

```markdown
### MBI-002: Analytics Dashboard

**Goal:** Users can view analytics dashboard

**Value:** Provides insights for decision-making

**WSJF:** 3.2 (Calculated: 2026-06-12)

**Status:** Ready
```

## Example Session

```
User: /wsjf

Agent: Found 3 MBIs in PLAN.md:
- MBI-001: Bootstrap & API (Active)
- MBI-002: Analytics Dashboard (Backlog)
- MBI-003: Reporting (Backlog)

Using MBI-002 as reference (medium complexity).

Scoring MBI-001: Bootstrap & API

Business Value: Compared to MBI-002, this MBI's value is...
[1: Much lower] [2: Lower] [3: Same] [5: Higher] [8: Much higher]

User: 5

Time Criticality: Compared to MBI-002, this MBI's urgency is...
[1: Much lower] [2: Lower] [3: Same] [5: Higher] [8: Much higher]

User: 8

Risk Reduction: Compared to MBI-002, this MBI's risk reduction is...
[1: Much lower] [2: Lower] [3: Same] [5: Higher] [8: Much higher]

User: 5

Job Size: Compared to MBI-002, this MBI's effort is...
[1: Much smaller] [2: Smaller] [3: Same] [5: Larger] [8: Much larger]

User: 8

[Continue for remaining MBIs...]

WSJF Results:

| MBI | Name | BV | TC | RR | Size | CoD | WSJF |
|-----|------|----|----|----|------|-----|------|
| MBI-003 | Reporting | 5 | 2 | 5 | 3 | 12 | 4.0 |
| MBI-002 | Analytics | 3 | 3 | 3 | 3 | 9 | 3.0 |
| MBI-001 | Bootstrap | 5 | 8 | 5 | 8 | 18 | 2.25 |

Recommendation: MBI-003 → MBI-002 → MBI-001

Would you like me to reorder PLAN.md?

User: Yes

Agent: Updated PLAN.md. MBIs reordered by WSJF score.
```

## Notes

- WSJF uses **relative scoring**, not absolute values
- Fibonacci sequence (1, 2, 3, 5, 8, 13) prevents false precision
- Reference item should be "medium" complexity for balanced comparison
- This is **interactive only** — scores are calculated on-demand, not automatically
- WSJF scores should be recalibrated every 8-12 weeks or when priorities change
- Job Size is in the denominator — smaller jobs get higher WSJF scores
