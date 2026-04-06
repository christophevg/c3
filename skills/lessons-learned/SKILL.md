---
name: lessons-learned
description: Use this skill any time when reviewing a session to improve existing skills, agents and/or create additional skills/agents.
---

# Lessons Learned

Review everything you have done and learned in this session. Propose improvements to skills, agents, `CLAUDE.md`, `AGENTS.md` and/or propose the creation of any new skills/agents to better support you in the future.

## When to Use This Skill

**Automatic triggers:**
- After completing a multi-step task
- After user corrects your approach
- After making mistakes that required rework
- After discovering a better approach halfway through
- After session involving skill usage

**Manual invocation:**
- User asks to "review this session"
- User asks to "learn from this session"
- User asks to "improve skills based on mistakes"

## Review Checklist

### Skill Usage Review

1. **Skill Selection** — Did you use the right skill for the task?
   - Could a different skill have been better suited?
   - Was there ambiguity about which skill to use?
   - Did skill descriptions make selection clear?

2. **Skill Completeness** — Did the skill provide adequate guidance?
   - Were there missing clarifying questions?
   - Were there missing implementation patterns?
   - Were there common mistakes not covered?
   - Did the workflow match the actual task needs?

3. **Skill Workflow** — Did you follow the skill's workflow?
   - Did you skip any steps?
   - Did you need to improvise beyond the skill?
   - Were any steps unnecessary or confusing?

### Implementation Review

4. **Repetitive patterns** — Did you repeat the same action multiple times? Could a skill automate or guide it?
5. **Missing guidance** — Was there a situation where you lacked clear instructions? Should a skill or agent be updated?
6. **Error corrections** — Did the user correct your approach? Save this as feedback memory.
7. **Documentation gaps** — Did you need to reference something that wasn't documented?
8. **Tool improvements** — Could existing skills be clearer, more comprehensive, or better structured?

### Common Mistake Patterns

9. **Skill Selection Mistakes** — Did you use skill X when skill Y would have been better?
   - Why did you choose the wrong skill?
   - What could have made you choose the right one?
   - Should skills have clearer "when to use" sections?

10. **Clarifying Question Gaps** — Did you miss asking important questions?
    - What questions did you fail to ask?
    - When should you have asked them?
    - What impact did missing questions have?

11. **Implementation Mistakes** — Did you make mistakes the skill could have prevented?
    - Were there patterns/examples in the skill you didn't follow?
    - Were there "common mistakes" you fell into?
    - Should new patterns be added to the skill?

12. **Validation Gaps** — Did you deliver incomplete or incorrect output?
    - What validation should you have done?
    - Would a checklist have helped?
    - Should the skill include validation steps?

## Output Format

After reviewing:

### 1. Summary of Session
Brief overview of what was accomplished, including:
- What task was requested
- What skills were used (or should have been used)
- What was delivered
- What mistakes were made
- What corrections were needed

### 2. Skill Improvements

For each skill used (or should have been used):

**Skill:** [skill-name]

**Issue:** [What went wrong or could be better]

**Root Cause:** [Why did this happen? Missing guidance? Unclear description?]

**Proposed Improvement:**
- Add "Skill Selection Guide" with decision tree
- Add "Common Mistakes to Avoid" section with examples
- Add must-ask clarifying questions to Step X
- Add validation checklist to Step Y
- Add pattern/example for [specific case]

**Expected Impact:** [How will this prevent future mistakes?]

### 3. New Skills/Agents

Proposals for new capabilities:
- **Skill Name:** [name]
- **Purpose:** [What problem does it solve?]
- **When to Use:** [Triggers]
- **Workflow:** [High-level steps]

### 4. Cross-Skill Learning

Are there learnings that apply to multiple skills?
- **Pattern:** [e.g., "Always ask about data validation in tracking spreadsheets"]
- **Skills to Update:** [List of skills that should include this pattern]
- **Implementation:** [How to add this to each skill]

### 5. Memories to Save

User corrections and preferences to remember:
- Save to feedback memory if user corrected approach
- Save to project memory if discovered new workflow preference
- Save to reference memory if found useful external resource

### 6. Validation Plan

How to validate improvements work:
- Test case: [What scenario would exercise this improvement?]
- Expected behavior: [What should happen with the improvement?]
- Success criteria: [How do we know it worked?]

---

## Implementation Step (CRITICAL)

After presenting the analysis above, you MUST:

### 7. Ask for Confirmation

Present the proposed changes and ask the user to confirm:

```
Based on this analysis, I propose to:
1. Update skill X: [description of change]
2. Update skill Y: [description of change]
3. Create new skill Z: [description]
4. Save memory A: [description]
5. Save memory B: [description]

Should I proceed with implementing these updates?
```

**DO NOT proceed without explicit user approval.**

Use the AskUserQuestion tool with options:
- "Yes, implement all proposed changes"
- "Yes, but let me select which changes to implement"
- "No, I want to modify the proposals first"

### 8. Implement Approved Changes

Only after user confirmation:

1. **Update existing skills**
   - Read current skill file
   - Apply improvements using Edit tool
   - Verify changes

2. **Create new skills**
   - Write skill file to appropriate location
   - Add to skill index if needed
   - Create symlink if following incubator workflow

3. **Save memories**
   - Write feedback memories for user corrections
   - Write project memories for workflow preferences
   - Write reference memories for external resources
   - Update MEMORY.md index

4. **Commit changes**
   - Stage all modified files
   - Commit with descriptive message

### 9. Report Completion

After implementing:
- List all changes made
- Confirm memories saved
- Confirm commits created
- Note any follow-up actions needed
