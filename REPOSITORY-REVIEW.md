# Repository Review: Outdated Documentation

**Review Date**: 2026-06-29
**Status**: Needs Attention

This document identifies outdated documentation, TODOs, plans, and ideas that need updating after recent changes.

---

## Summary of Recent Changes

### Skills Added/Updated (Since Last Changelog)
- `tight-python` → merged into `python` skill
- `bug-hunting` → NEW skill for systematic debugging
- `plan` → NEW skill for structured feature planning
- `wsjf` → NEW skill for WSJF scoring
- `research` → RESTORED (was incorrectly removed)
- `markdown-to-pdf` → enhanced
- `prepare-for-exam` → enhanced
- `project-feature` → enhanced with MBI workflow
- `project-manage` → enhanced with MBI support

### Agents Updated
- `python-developer` → tight code philosophy, library-first check
- `code-reviewer` → tight code philosophy as primary checklist
- `testing-engineer` → tight tests philosophy, test anti-patterns
- `researcher` → fixed to reference `c3:research` skill
- `functional-analyst` → MBI intake workflow
- `end-user-documenter` → formatting improvements
- `project-manager` → minor improvements
- `release-manager` → minor improvements
- `security-engineer` → minor improvements

### Infrastructure Changes
- `.mcp.json` → updated email-gw version
- `settings.json` → added timeout settings, disabled auto-memory
- `Makefile.claude` → improved refine target
- `scripts/templates/default.css` → NEW

---

## Items Needing Update

### 1. README.md — Skills/Agents Count Outdated

**Issue**: Shows "Skills (42)" but there are now more.

**Current Skills**: Let me count...
- Plugin & MCP Development: 2
- Project Management: 6
- Personal Assistant: 4
- Domain Expertise: 9
- Development: 2
- Utility: Count listed but need to verify

**Action**: Recount skills and agents, update README.md

### 2. CHANGELOG.md — Missing Recent Changes

**Issue**: Last entry is 2026-04-21, but many changes since then.

**Missing Changes**:
- MBI Intake Layer implementation
- Bug-hunting skill added
- Plan skill added
- WSJF skill added
- Research skill restored
- Tight-python merged into python skill
- Agent improvements (python-developer, code-reviewer, testing-engineer, researcher)

**Action**: Add changelog entries for all recent changes

### 3. TODO.md — Outdated Items

**Completed Items Still Listed**:
- ✅ MBI Intake Layer Implementation — still marked as P2 High, should be in Done
- ✅ Email MCP auto-save — completed, should be in Done

**Outdated References**:
- "Set up MkDocs Material documentation site for C3" — still in P4 Low, may need status update
- "Researcher agent improvement" — partially done (research skill restored)

**Needs Review**:
- "AI Overview skill" — depends on PlayWright research
- "PlayWright research" — not started
- "Brainstorming agent research" — https://mcpmarket.com/tools/skills/brainstorming-design-specifier
- "C3 agents async communication pattern" — complex feature, needs evaluation
- "CronCreate, ScheduleWakeup tools" — needs evaluation
- "Personal Assistant Agent design" — needs evaluation
- "Document scripts centralization pattern" — may be outdated
- "Improve README skill" — needs evaluation
- "Python style guidelines enhancement" — now addressed by tight-python integration
- "Create plugin-script skill" — low priority
- Various research items — may need prioritization

**Action**: Clean up TODO.md, move completed items to Done, update priorities

### 4. research/INDEX.md — Missing Recent Research

**Issue**: Missing entry for MBI Intake Backlog research (2026-06-12).

**Action**: Add entry for `2026-06-12-mbi-intake-backlog/` research

### 5. PLAN.md (project-feature) — Template Only

**Issue**: Contains only template structure, no actual MBIs.

**Note**: This is expected — it's a template for projects to use.

**Action**: No change needed, this is intentional.

### 6. Agent/Skill Documentation Consistency

**Potential Issues**:
- Some skills may reference other skills that no longer exist or have changed
- Agent descriptions may not match current capabilities
- Color assignments should be unique and descriptive

**Action**: Audit cross-references between skills and agents

---

## Documentation Quality Review

### Skills (by size, largest first)

| File | Lines | Review Needed |
|------|-------|---------------|
| project-manage/SKILL.md | 1433 | May need MBI workflow updates verified |
| api-architect/SKILL.md | (agent) | Verify MBI references |
| functional-analyst/SKILL.md | (agent) | MBI workflow added ✓ |
| python-project/SKILL.md | 761 | Verify consistency with python skill |
| code-reviewer.md | 735 | Tight code philosophy added ✓ |
| vuetify-v3/SKILL.md | 688 | No changes needed |
| project-migrate/SKILL.md | 560 | Verify workflow consistency |
| testing-engineer.md | 529 | Tight tests philosophy added ✓ |
| develop-skill/SKILL.md | 506 | No changes needed |
| quart-webapp/SKILL.md | 499 | Verify consistency |
| spec2mod/SKILL.md | 486 | No changes needed |
| python/SKILL.md | 467 | Tight-python merged ✓ |
| commit/SKILL.md | 439 | No changes needed |
| vuetify-v1/SKILL.md | 435 | No changes needed |
| copy-writer/SKILL.md | 427 | No changes needed |
| develop-agent/SKILL.md | 399 | No changes needed |
| pymongo/SKILL.md | 400 | No changes needed |
| ollama/SKILL.md | 399 | No changes needed |

### New Skills (not in README)

| Skill | Status | Action |
|-------|--------|--------|
| bug-hunting | Added, not in README | Add to README |
| plan | Added, not in README | Add to README |
| wsjf | Added, not in README | Add to README |
| research | Restored, not in README | Add to README |

---

## Recommended Actions

### Priority 1: Update Core Documentation

1. **Update README.md**
   - Recount skills (now ~46)
   - Recount agents (now 13+, verify)
   - Add new skills: bug-hunting, plan, wsjf, research

2. **Update CHANGELOG.md**
   - Add all changes since 2026-04-21
   - Include skill additions/changes
   - Include agent improvements
   - Include infrastructure changes

3. **Clean up TODO.md**
   - Move completed items to Done section
   - Update priorities for remaining items
   - Mark stale items for removal

### Priority 2: Update Research Index

4. **Update research/INDEX.md**
   - Add entry for MBI Intake Backlog research
   - Verify all research folders have entries

### Priority 3: Verify Cross-References

5. **Audit skill/agent cross-references**
   - Verify all skill references exist
   - Verify all agent references are correct
   - Check for outdated "c3:" prefixes

---

## Files to Update

```
README.md            # Skills/agents count, add new skills
CHANGELOG.md         # Add recent changes
TODO.md              # Move completed items, update priorities
research/INDEX.md    # Add missing research entry
```

---

## Questions for User

1. **MkDocs Material documentation site** — Still wanted? Or remove from backlog?
2. **AI Overview skill + PlayWright research** — Still relevant? Or deprioritize?
3. **C3 agents async communication pattern** — Complex feature, still needed?
4. **Personal Assistant Agent design** — Should this be a separate task or part of assistant agent improvements?
5. **Python style guidelines enhancement** — Now addressed by tight-python integration. Close as complete?
6. **Brainstorming agent research** — Still needed? Or close?
7. **Markitdown research** — Still needed? Or close?